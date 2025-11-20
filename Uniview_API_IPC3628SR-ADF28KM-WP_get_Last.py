import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime, timedelta
import urllib3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import subprocess

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Camera settings
IP = "192.168.1.147"
USERNAME = "admin"
PASSWORD = "__REDACTED__"

# Email settings
GMAIL_USER = "__REDACTED__@gmail.com"
GMAIL_APP_PASSWORD = "__REDACTED__"
RECIPIENT = "__REDACTED__@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

FLAG_FILE = "sent_events.txt"

def get_sent_events():
    if os.path.exists(FLAG_FILE):
        with open(FLAG_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def add_sent_event(event_id):
    with open(FLAG_FILE, 'a') as f:
        f.write(f"{event_id}\n")

def send_email_with_attachment(filepath, event_time):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT
        msg['Subject'] = f"Motion Detected - {event_time.strftime('%Y-%m-%d %I:%M:%S %p')}"

        body = f"Motion detected at: {event_time.strftime('%Y-%m-%d %I:%M:%S %p')}"
        msg.attach(MIMEText(body, 'plain'))

        with open(filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
        msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✓ Email sent")
        return True

    except Exception as e:
        print(f"✗ Email failed: {e}")
        return False

def download_recording(record_id, begin_time, end_time, output_dir="recordings"):
    """Download and compress recording to 420p for Gmail"""

    os.makedirs(output_dir, exist_ok=True)

    event_time = datetime.fromtimestamp(begin_time)
    duration = end_time - begin_time

    print(f"\nDownloading RecordID {record_id}")
    print(f"  Time: {event_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f"  Duration: {duration}s")

    filename_ts = f"cctvfn.localdomain_{begin_time}_{end_time}.ts"
    filename_compressed = f"motion_{record_id}_{event_time.strftime('%Y%m%d_%H%M%S')}_compressed.mp4"
    filepath_ts = os.path.join(output_dir, filename_ts)
    filepath_compressed = os.path.join(output_dir, filename_compressed)

    url = f"http://{IP}/LAPI/V1.0/Channel/0/Media/RecordDownload/{filename_ts}"

    try:
        # Download original file
        response = requests.get(
            url,
            auth=HTTPDigestAuth(USERNAME, PASSWORD),
            stream=True,
            timeout=300,
            verify=False
        )

        if response.status_code == 200:
            with open(filepath_ts, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            if os.path.exists(filepath_ts) and os.path.getsize(filepath_ts) > 10000:
                original_size = os.path.getsize(filepath_ts) / (1024 * 1024)
                print(f"✓ Downloaded: {original_size:.2f} MB")

                # Compress to 420p resolution
                print(f"  Compressing to 420p...")
                cmd = [
                    'ffmpeg',
                    '-i', filepath_ts,
                    '-vf', 'scale=-2:420',
                    '-c:v', 'libx264',
                    '-preset', 'fast',
                    '-crf', '28',
                    '-c:a', 'aac',
                    '-b:a', '64k',
                    '-movflags', '+faststart',
                    '-y',
                    filepath_compressed
                ]

                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=duration + 120
                )

                if result.returncode == 0 and os.path.exists(filepath_compressed):
                    compressed_size = os.path.getsize(filepath_compressed) / (1024 * 1024)
                    print(f"✓ Compressed: {compressed_size:.2f} MB (saved {original_size - compressed_size:.2f} MB)")

                    # Delete original file
                    os.remove(filepath_ts)
                    print(f"✓ Deleted original file")

                    return filepath_compressed
                else:
                    print(f"✗ Compression failed, using original")
                    return filepath_ts
            else:
                print(f"✗ Download failed or file too small")
                if os.path.exists(filepath_ts):
                    os.remove(filepath_ts)
                return None
        else:
            print(f"✗ Download failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def process_recordings_24h():
    """Process only new recordings from past 24 hours"""

    now = datetime.now()
    begin_time = int((now - timedelta(hours=24)).timestamp())
    end_time = int(now.timestamp())

    url = f"http://{IP}/LAPI/V1.0/Channel/0/Media/Video/Streams/0/Records"
    params = {
        'Begin': begin_time,
        'End': end_time,
        'Limit': 100,
        'Offset': 0,
        'Types': 0
    }

    response = requests.get(
        url,
        params=params,
        auth=HTTPDigestAuth(USERNAME, PASSWORD),
        timeout=10,
        verify=False
    )

    if response.status_code != 200:
        print(f"Failed to get recordings: {response.status_code}")
        return

    data = response.json()
    recordings = data['Response']['Data'].get('RecordInfos', [])

    if not recordings:
        print("No recordings found in past 24 hours")
        return

    print(f"Found {len(recordings)} recordings in past 24 hours")

    # Get already sent events
    sent_events = get_sent_events()
    recordings.sort(key=lambda x: x['Begin'])

    # Filter out already sent recordings
    new_recordings = [r for r in recordings if str(r['RecordID']) not in sent_events]

    if not new_recordings:
        print("No new recordings to process")
        return

    print(f"Processing {len(new_recordings)} new recording(s)")

    new_count = 0
    for recording in new_recordings:
        record_id = str(recording['RecordID'])
        begin_ts = recording['Begin']
        end_ts = recording['End']
        event_time = datetime.fromtimestamp(begin_ts)

        filepath = download_recording(record_id, begin_ts, end_ts)

        if filepath and send_email_with_attachment(filepath, event_time):
            add_sent_event(record_id)
            new_count += 1

    print(f"\n{'='*50}")
    print(f"Successfully processed {new_count} new recording(s)")

# Run
process_recordings_24h()

