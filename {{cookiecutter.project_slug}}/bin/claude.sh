#!/bin/bash

# Combined Claude script with start and restart functionality

# Stable files for inter-process coordination
PID_FILE="/tmp/claude_pid"
RESTART_MODE_FILE="/tmp/claude_restart_mode"
RESTART_PROMPT_FILE="/tmp/claude_restart_prompt"

# Print the command about to run with safe shell escaping
print_cmd() {
    local args=("$@")
    local out="+ "
    local a
    for a in "${args[@]}"; do
        # If arg has spaces or tabs, wrap in double-quotes and escape backslashes and quotes
        if [[ "$a" =~ [[:space:]] ]]; then
            local escaped=${a//\\/\\\\}
            escaped=${escaped//\"/\\\"}
            out+="\"${escaped}\" "
        else
            out+="${a} "
        fi
    done
    echo "${out% }"
}

show_help() {
    echo "Usage: $0 [OPTIONS] [CLAUDE_ARGS...]"
    echo ""
    echo "Options:"
    echo "  --restart              Kill any running Claude process managed by this script and restart with -c"
    echo "  --restart-autonomous   Kill any running Claude process and restart with -p '<continuation-prompt>'"
    echo "  --prompt \"text\"         Custom prompt text for autonomous mode (default: \"You are now in autonomous mode. Continue from where you left off.\")"
    echo "  --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                           # Start Claude normally"
    echo "  $0 --some-claude-flag        # Start Claude with specific flags"
    echo "  $0 --restart                 # Restart running Claude with -c flag"
    echo "  $0 --restart-autonomous      # Restart running Claude with autonomous continuation"
    echo "  $0 --restart-autonomous --prompt \"Resume work\"  # Restart with custom prompt"
    echo ""
}

# Default autonomous prompt
DEFAULT_AUTONOMOUS_PROMPT="You are now in autonomous mode. Continue from where you left off. Do not stop until all user directives you have been given are completed/resolved."
AUTONOMOUS_PROMPT="$DEFAULT_AUTONOMOUS_PROMPT"

# Parse arguments to extract --prompt if present
ARGS=("$@")
FILTERED_ARGS=()
i=0
while [ $i -lt ${#ARGS[@]} ]; do
    if [[ "${ARGS[$i]}" == "--prompt" ]]; then
        # Next argument should be the prompt text
        if [ $((i+1)) -lt ${#ARGS[@]} ]; then
            AUTONOMOUS_PROMPT="${ARGS[$((i+1))]}"
            i=$((i+2))  # Skip both --prompt and its value
        else
            echo "Error: --prompt requires a value"
            exit 1
        fi
    else
        FILTERED_ARGS+=("${ARGS[$i]}")
        i=$((i+1))
    fi
done

# Update $@ to contain filtered arguments (without --prompt and its value)
set -- "${FILTERED_ARGS[@]}"

# Check for help flag
if [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Check for restart flags
if [[ "$1" == "--restart" ]] || [[ "$1" == "--restart-autonomous" ]]; then
    echo "Restart requested. Looking for running Claude process..."
    
    # Read the managed Claude PID from pidfile
    if [[ -f "$PID_FILE" ]]; then
        CLAUDE_PID=$(cat "$PID_FILE")
    else
        echo "No pidfile found at $PID_FILE. Is Claude running under this script?"
        exit 1
    fi
    
    if [[ -z "$CLAUDE_PID" ]] || ! kill -0 "$CLAUDE_PID" 2>/dev/null; then
        echo "No running Claude process found to restart (pid: $CLAUDE_PID)."
        exit 1
    fi
    
    echo "Found Claude process (PID: $CLAUDE_PID). Sending restart signal..."
    
    # Store restart mode and prompt for the monitoring loop (use stable file paths)
    if [[ "$1" == "--restart-autonomous" ]]; then
        echo "RESTART_AUTONOMOUS" > "$RESTART_MODE_FILE"
        echo "$AUTONOMOUS_PROMPT" > "$RESTART_PROMPT_FILE"
    else
        echo "RESTART_NORMAL" > "$RESTART_MODE_FILE"
        rm -f "$RESTART_PROMPT_FILE" 2>/dev/null || true
    fi
    
    # Kill the Claude process - the monitoring loop will handle the restart
    kill "$CLAUDE_PID"
    
    # Wait for the process to die
    TIMEOUT=10
    COUNTER=0
    
    while kill -0 "$CLAUDE_PID" 2>/dev/null; do
        sleep 0.5
        COUNTER=$((COUNTER + 1))
        
        if [ $COUNTER -ge $TIMEOUT ]; then
            echo "Process still alive after 5 seconds. Force killing..."
            kill -9 "$CLAUDE_PID" 2>/dev/null
            break
        fi
    done
    
    echo "Restart signal sent successfully."
    exit 0
fi

# Start Claude with monitoring
echo "Starting Claude..."

# Track whether we should use -c flag or autonomous restart
USE_C_FLAG=false
USE_AUTONOMOUS=false
RESTART_PROMPT="$DEFAULT_AUTONOMOUS_PROMPT"

# Set Claude Code's max bash command timeout so agents can await longer-running processes
BASH_MAX_TIMEOUT_MS=600000

# Check if there's a restart mode file (stable path)
if [ -f "$RESTART_MODE_FILE" ]; then
    RESTART_MODE=$(cat "$RESTART_MODE_FILE")
    if [[ "$RESTART_MODE" == "RESTART_AUTONOMOUS" ]]; then
        USE_AUTONOMOUS=true
        # Read custom prompt if available
        if [ -f "$RESTART_PROMPT_FILE" ]; then
            RESTART_PROMPT=$(cat "$RESTART_PROMPT_FILE")
            rm -f "$RESTART_PROMPT_FILE"
        fi
    else
        USE_C_FLAG=true
    fi
    rm -f "$RESTART_MODE_FILE"
fi

while true; do
    # Start Claude based on restart mode
    if [ "$USE_AUTONOMOUS" = true ]; then
        # Use autonomous restart with -p, -c, and --dangerously-skip-permissions flags
        AUTONOMOUS_ARGS=()
        
        # Add -p first (non-interactive mode)
        AUTONOMOUS_ARGS+=("-p")
        
        # Add -c for continuation (we need continuation for autonomous to work)
        AUTONOMOUS_ARGS+=("-c")
        
        # Add --dangerously-skip-permissions if not already present
        if [[ "$*" != *"--dangerously-skip-permissions"* ]]; then
            AUTONOMOUS_ARGS+=("--dangerously-skip-permissions")
        fi
        
        # Add the prompt as the final argument
        # Launch in background to capture PID, then wait
        cmd=(claude "${AUTONOMOUS_ARGS[@]}" "$@" "$RESTART_PROMPT")
        print_cmd "${cmd[@]}"
        "${cmd[@]}" &
        CHILD_PID=$!
        echo "$CHILD_PID" > "$PID_FILE"
        wait "$CHILD_PID"
        EXIT_CODE=$?
    elif [ "$USE_C_FLAG" = true ]; then
        # Ensure -c is present but avoid duplicates
        if [[ "$*" == *"-c"* ]]; then
            cmd=(claude "$@")
        else
            cmd=(claude -c "$@")
        fi
        print_cmd "${cmd[@]}"
        "${cmd[@]}" &
        CHILD_PID=$!
        echo "$CHILD_PID" > "$PID_FILE"
        wait "$CHILD_PID"
        EXIT_CODE=$?
    else
        cmd=(claude "$@")
        print_cmd "${cmd[@]}"
        "${cmd[@]}" &
        CHILD_PID=$!
        echo "$CHILD_PID" > "$PID_FILE"
        wait "$CHILD_PID"
        EXIT_CODE=$?
    fi

    # Cleanup pidfile after process exits
    rm -f "$PID_FILE" 2>/dev/null || true
    
    echo "Claude exited with code: $EXIT_CODE"
    
    # Check if Claude was killed by SIGTERM (15) -> exit code 143
    # This indicates it was killed by our restart functionality
    if [ $EXIT_CODE -eq 143 ]; then
        # Check if there's a restart mode file to determine how to restart
        if [ -f "$RESTART_MODE_FILE" ]; then
            RESTART_MODE=$(cat "$RESTART_MODE_FILE")
            if [[ "$RESTART_MODE" == "RESTART_AUTONOMOUS" ]]; then
                echo "Claude was terminated by autonomous restart. Setting autonomous mode for restart..."
                USE_AUTONOMOUS=true
                USE_C_FLAG=false
                # Read custom prompt if available
                if [ -f "$RESTART_PROMPT_FILE" ]; then
                    RESTART_PROMPT=$(cat "$RESTART_PROMPT_FILE")
                    rm -f "$RESTART_PROMPT_FILE"
                fi
            else
                echo "Claude was terminated by restart. Setting -c flag for restart..."
                USE_C_FLAG=true
                USE_AUTONOMOUS=false
            fi
            rm -f "$RESTART_MODE_FILE"
        else
            echo "Claude was terminated by restart. Setting -c flag for future restarts..."
            USE_C_FLAG=true
            USE_AUTONOMOUS=false
        fi
        # Continue the loop to restart Claude
        continue
    fi
    
    # Check if Claude was killed by SIGKILL (9) -> exit code 137
    # This also indicates it was killed by our restart functionality (after SIGTERM failed)
    if [ $EXIT_CODE -eq 137 ]; then
        # Check if there's a restart mode file to determine how to restart
        if [ -f "$RESTART_MODE_FILE" ]; then
            RESTART_MODE=$(cat "$RESTART_MODE_FILE")
            if [[ "$RESTART_MODE" == "RESTART_AUTONOMOUS" ]]; then
                echo "Claude was force-killed by autonomous restart. Setting autonomous mode for restart..."
                USE_AUTONOMOUS=true
                USE_C_FLAG=false
                # Read custom prompt if available
                if [ -f "$RESTART_PROMPT_FILE" ]; then
                    RESTART_PROMPT=$(cat "$RESTART_PROMPT_FILE")
                    rm -f "$RESTART_PROMPT_FILE"
                fi
            else
                echo "Claude was force-killed by restart. Setting -c flag for restart..."
                USE_C_FLAG=true
                USE_AUTONOMOUS=false
            fi
            rm -f "$RESTART_MODE_FILE"
        else
            echo "Claude was force-killed by restart. Setting -c flag for future restarts..."
            USE_C_FLAG=true
            USE_AUTONOMOUS=false
        fi
        # Continue the loop to restart Claude
        continue
    fi
    
    # If Claude exited normally (0) or with any other error code, stop the loop
    if [ $EXIT_CODE -eq 0 ]; then
        echo "Claude exited normally. Goodbye!"
        break
    elif [ $EXIT_CODE -ne 143 ] && [ $EXIT_CODE -ne 137 ]; then
        echo "Claude exited with error code $EXIT_CODE. Stopping."
        break
    fi
    
    echo "Restarting Claude in 2 seconds..."
    sleep 2
done