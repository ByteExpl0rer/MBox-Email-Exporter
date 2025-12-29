import mailbox
from collections import defaultdict
import sys
from email.header import decode_header
import csv
import os
from datetime import datetime

def decode_mime_header(header):
    """
    Decode a MIME email header into readable text.
    Handles unknown encodings and returns "(Unknown)" if empty.
    """
    if not header:
        return "(Unknown)"
    
    decoded_parts = decode_header(header)
    parts = []

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                part = part.decode(
                    encoding if encoding and encoding.lower() not in ['unknown-8bit','x-unknown'] else 'utf-8',
                    errors='replace'
                )
            except (LookupError, TypeError):
                part = part.decode('utf-8', errors='replace')
        parts.append(part)
    return ''.join(parts)

def export_to_csv(data, base_folder, filename):
    """
    Export the email summary into a dated subfolder.
    Creates all necessary folders automatically.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if not base_folder:
        base_folder = "export"

    base_folder_path = os.path.join(script_dir, base_folder)
    os.makedirs(base_folder_path, exist_ok=True)

    # Create a dated subfolder
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join(base_folder_path, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    path = os.path.join(folder_path, filename)

    # Write CSV
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Sender', 'Email Count'])
        for sender, count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([sender, count])

    print(f"\nExport completed: {path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py file.mbox [export_folder] [csv_filename]")
        sys.exit(1)

    mbox_file = sys.argv[1]

    export_folder = None
    export_file = "emails_summary.csv"

    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        if arg.lower().endswith(".csv"):
            export_file = arg
        else:
            export_folder = arg

    if len(sys.argv) >= 4:
        export_file = sys.argv[3]

    # Count emails per sender
    emails_per_sender = defaultdict(int)
    try:
        mbox = mailbox.mbox(mbox_file)
    except FileNotFoundError:
        print(f"Error: file '{mbox_file}' not found.")
        sys.exit(1)

    for message in mbox:
        sender = decode_mime_header(message['From'])
        emails_per_sender[sender] += 1

    # Compact terminal output
    print("Email senders summary:\n")
    for sender, count in sorted(emails_per_sender.items(), key=lambda x: x[1], reverse=True):
        print(f"{sender} : {count} email(s)")

    # Export CSV
    export_to_csv(emails_per_sender, export_folder, export_file)

if __name__ == "__main__":
    main()
