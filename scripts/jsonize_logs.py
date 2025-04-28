import json
import re
import os
import sys

def parse_log_errors(log_path):
    errors = []
    with open(log_path, 'r') as file:
        lines = file.readlines()

    error_entry = None
    collecting_traceback = False

    for line in lines:
        if 'ERROR' in line:
            if error_entry:
                errors.append(error_entry)
            timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})', line)
            timestamp = timestamp_match.group(1) if timestamp_match else "unknown"
            message = line.strip()
            error_entry = {
                "timestamp": timestamp,
                "message": message,
                "traceback": ""
            }
            collecting_traceback = True
        elif collecting_traceback and error_entry:
            if line.strip() == "":
                collecting_traceback = False
            else:
                error_entry["traceback"] += line

    if error_entry:
        errors.append(error_entry)

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python jsonize.py <log_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    if not os.path.isfile(log_file_path):
        print(f"Error: File '{log_file_path}' does not exist.")
        sys.exit(1)

    # Generate output file name based on input log filename
    base_name = os.path.splitext(os.path.basename(log_file_path))[0]
    output_file = f"parsed_errors_{base_name}.json"

    errors_json = parse_log_errors(log_file_path)

    with open(output_file, "w") as out:
        json.dump(errors_json, out, indent=4)

    print(f"Extracted {len(errors_json)} error entries. Saved to '{output_file}'.")