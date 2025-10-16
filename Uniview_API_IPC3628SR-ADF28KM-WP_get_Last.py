import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import subprocess
import urllib3
from urllib.parse import quote
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# this will grab the last video and email it ... like a BOSS I set it to cron every 2 min ... you will miss anthing in between and leep year or who knows I hate working with time ! 
# Camera settings
IP = "192.168.1.147"
USERNAME = "admin"
PASSWORD = "___YOURCCTVPASSWORDHERE__"
PASSWORD_ENCODED = quote(PASSWORD, safe='')

# Email settings
GMAIL_USER = "rmccurdywork@gmail.com"
GMAIL_APP_PASSWORD = "__YOURSMTPPASSWORD__"
RECIPIENT = "kmlindsey@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Flag file to track last sent video
FLAG_FILE = "last_sent_video.txt"

def get_last_sent_video():
    """Read the last sent video ID from flag file"""
    if os.path.exists(FLAG_FILE):
        with open(FLAG_FILE, 'r') as f:
            return f.read().strip()
    return None

def set_last_sent_video(record_id):
    """Write the video ID to flag file"""
    with open(FLAG_FILE, 'w') as f:
        f.write(str(record_id))

def send_email_with_attachment(filepath, record_id, start_dt):
    """Send email with video attachment via Gmail"""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT
        msg['Subject'] = f"Security Recording - {start_dt.strftime('%Y-%m-%d %H:%M:%S')}"

        body = f"Attached is the latest security camera recording.\n\nRecording ID: {record_id}\nTime: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}"
        msg.attach(MIMEText(body, 'plain'))

        # Attach file
        with open(filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
        msg.attach(part)

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✓ Email sent to {RECIPIENT}")
        return True

    except Exception as e:
        print(f"✗ Email failed: {e}")
        return False

def download_and_send_latest_recording(output_dir="recordings"):
    """Download, compress, and email the latest recording if not already sent"""

    os.makedirs(output_dir, exist_ok=True)

    # Get recordings - fetch more to ensure we get the latest
    now = datetime.now()
    begin_time = int(datetime(now.year, now.month, now.day, 0, 0, 0).timestamp())
    end_time = int(now.timestamp())

    url = f"http://{IP}/LAPI/V1.0/Channel/0/Media/Video/Streams/0/Records"
    params = {
        'Begin': begin_time,
        'End': end_time,
        'Limit': 100,  # Fetch more recordings
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
        return None

    data = response.json()
    recordings = data['Response']['Data'].get('RecordInfos', [])

    if not recordings:
        print("No recordings found")
        return None

    # Sort by Begin time descending to get the most recent
    recordings.sort(key=lambda x: x['Begin'], reverse=True)

    # Get latest recording
    recording = recordings[0]
    record_id = recording['RecordID']

    # Check if already sent
    last_sent = get_last_sent_video()
    if last_sent == str(record_id):
        print(f"Recording {record_id} already sent. Skipping.")
        return None

    begin_time = recording['Begin']
    end_time = recording['End']
    duration = end_time - begin_time

    rtsp_url = f"rtsp://{USERNAME}:{PASSWORD_ENCODED}@{IP}:554/media/video2?starttime={begin_time}"

    start_dt = datetime.fromtimestamp(begin_time)
    filename = f"recording_{record_id}_{start_dt.strftime('%Y%m%d_%H%M%S')}_compressed.mp4"
    filepath = os.path.join(output_dir, filename)

    print(f"Downloading latest recording (ID: {record_id})")
    print(f"  Time: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Duration: {duration}s")

    # FFmpeg command
    cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', rtsp_url,
        '-t', str(duration),
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '28',
        '-vf', 'scale=854:480',
        '-c:a', 'aac',
        '-b:a', '64k',
        '-movflags', '+faststart',
        '-y',
        filepath
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=duration + 120
        )

        if result.returncode == 0 and os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / (1024 * 1024)
            print(f"✓ Downloaded: {filepath} ({file_size:.2f} MB)")

            # Send email
            if send_email_with_attachment(filepath, record_id, start_dt):
                set_last_sent_video(record_id)
                print(f"✓ Flagged recording {record_id} as sent")

            return filepath
        else:
            print(f"✗ FFmpeg failed:")
            print(result.stderr[-1000:])
            return None

    except subprocess.TimeoutExpired:
        print(f"✗ Timeout after {duration + 120}s")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

# Run the download and send
download_and_send_latest_recording()

