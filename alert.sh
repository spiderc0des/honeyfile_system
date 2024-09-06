#!/bin/bash

base_dir="$PWD/filesystem"

# Array of decoy file paths
DECOY_FILES=(
    "${base_dir}/Finance/Invoices/invoice_Q3_2024.pdf"
    "${base_dir}/Finance/Reports/financial_analysis_2024.xlsx"
    "${base_dir}/HR/EmployeeRecords/john_doe_record.pdf"
    "${base_dir}/HR/Payrolls/payroll_august_2024.csv"
    "${base_dir}/Operations/MeetingNotes/meeting_08292024.txt"
    "${base_dir}/Operations/AnnualReports/2024_annual_report.docx"
    "${base_dir}/IT/NetworkLogs/network_log_08292024.log"
    "${base_dir}/IT/SystemBackups/backup_08292024.zip"
    "${base_dir}/Marketing/Campaigns/Q4_campaign_plans.pptx"
    "${base_dir}/Marketing/SocialMedia/social_media_schedule.xls"
)

# Function to monitor a single file
monitor_file() {
    local file=$1
    inotifywait -m -e open "$file" | while read path action f; do
        echo "Decoy file accessed: $f"
        # Get the current time in ISO 8601 format, adjust format as needed to match Python's log
        current_time=$(date --iso-8601=seconds)
        echo "Current time: $current_time"
        # Use grep to find a close match in the access.log based on time
        # This requires careful handling of time format and synchronization
        message=$(grep "$f" access.log | tail -n 1)
        python email_sender.py "$message"
    done
}

# Loop over each file and monitor it in the background
for file in "${DECOY_FILES[@]}"; do
    monitor_file "$file" &
done

# Wait for all background processes to finish
wait
