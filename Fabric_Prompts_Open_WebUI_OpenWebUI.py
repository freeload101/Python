import requests
import zipfile
import os
import json
import uuid
import time
import io

def download_and_extract_to_json(url, target_filename, target_folder):
    response = requests.get(url)
    json_array = []
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for file_info in z.infolist():
            if file_info.filename.endswith(target_filename):
                extracted_path = os.path.join(target_folder, file_info.filename)
                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                with z.open(file_info) as f:
                    md_content = f.read().decode('utf-8')
                #json_content = json.dumps({'content': md_content})
                json_array.append(create_json_object(md_content, extracted_path.split("/")[-2].replace("_", "-")))
    save_json_array(json_array)

def create_json_object(content, path):
    return {
        "content": content,
        "command": f"Fab-{path}",
        "title": f"Fab-{path}",
        "user_id": str(uuid.uuid4()),
        "timestamp": int(time.time())
    }

def save_json_array(json_array):
    with open("Fabric_Prompts_Open_WebUI_OpenWebUI_20241112.json", 'w') as file:
        json.dump(json_array, file, indent=4)

url = "https://github.com/danielmiessler/fabric/archive/refs/heads/main.zip"
target_filename = "system.md"
target_folder = "patterns"

download_and_extract_to_json(url, target_filename, target_folder)
