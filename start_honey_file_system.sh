#!/bin/bash
# Master Script to run both HTTP server and file monitoring

# Function to terminate all child processes
cleanup() {
    echo "Terminating all child processes..."
    kill -SIGTERM "$pyserver_pid" "$monitor_pid"
    pkill -f 'inotifywait -m -e open'
    wait "$pyserver_pid" "$monitor_pid"
    echo "All processes terminated."
}

# Trap SIGINT (Ctrl+C) and SIGTERM (termination signal)
trap cleanup SIGINT SIGTERM

# Run HTTP Server in background
./pyserver.py &
pyserver_pid=$!

# Run File Monitoring in foreground
./alert.sh &
monitor_pid=$!

# Wait for all background processes to finish
wait
