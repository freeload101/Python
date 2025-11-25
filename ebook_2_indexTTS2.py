import os
import time
import subprocess
import json
import requests
from pathlib import Path

def get_gpu_usage():
    """Get current GPU usage percentage using nvidia-smi."""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
            capture_output=True,
            text=True,
            check=True
        )
        usage = float(result.stdout.strip().split('\n')[0])
        return usage
    except Exception as e:
        print(f"Error getting GPU usage: {e}")
        return 0

def send_post_request(file_content):
    """Send POST request with file content."""
    url = "http://localhost:7860/gradio_api/queue/join?__theme=dark"

    headers = {
        "Content-Type": "application/json",
        "sec-ch-ua-platform": "Windows",
        "Accept-Language": "en-US,en;q=0.9",
        "sec-ch-ua": '"Not=A?Brand";v="24", "Chromium";v="140"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "http://localhost:7860",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "http://localhost:7860/?__theme=dark",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    payload = {
        "data": [
            "Same as the voice reference",
            {
                "path": "C:\\Users\\internet\\AppData\\Local\\Temp\\gradio\\e54872aa69203832a30b4526d84f599a077e35e8675bdd35933d23cf32b220e7\\1_10SEC_Shohreh Aghdashloo.wav",
                "url": "http://localhost:7860/gradio_api/file=C:\\Users\\internet\\AppData\\Local\\Temp\\gradio\\e54872aa69203832a30b4526d84f599a077e35e8675bdd35933d23cf32b220e7\\1_10SEC_Shohreh Aghdashloo.wav",
                "orig_name": "1_10SEC_Shohreh Aghdashloo.wav",
                "size": 2835418,
                "mime_type": "audio/wav",
                "meta": {"_type": "gradio.FileData"}
            },
            file_content,  # Replace with file content
            None, 0.65, 0, 0, 0, 0, 0, 0, 0, 0, "", False, 120, True, 0.8, 30, 0.8, 0, 3, 10, 1500
        ],
        "event_data": None,
        "fn_index": 6,
        "trigger_id": 7,
        "session_hash": "z05g341a3af"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response

def process_ebook_chunks(directory="."):
    """Process all ebook_chunk files when GPU usage is under 50%."""
    chunk_files = sorted(Path(directory).glob("ebook_chunk*"))

    if not chunk_files:
        print("No ebook_chunk files found")
        return

    for chunk_file in chunk_files:
        # Wait until GPU usage is under 50%
        while True:
            print("waiting 20 seconds for GPU check .....")
            time.sleep(20)
            gpu_usage = get_gpu_usage()
            print(f"GPU Usage: {gpu_usage}%")

            if gpu_usage < 20:
                break
            else:
                print("GPU usage above 50%, waiting 60 seconds...")
                time.sleep(60)

        # Read file content
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"Processing {chunk_file.name}...")
            response = send_post_request(content)
            print(f"Response status: {response.status_code}")

        except Exception as e:
            print(f"Error processing {chunk_file.name}: {e}")

if __name__ == "__main__":
    process_ebook_chunks()
