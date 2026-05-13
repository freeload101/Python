import requests
import zipfile
import os
import json
import uuid
import time
import io
import logging

# Configure logging with debug level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_extract_to_json(url, target_filename, target_folder):
    logger.debug(f"Starting download and extraction from URL: {url}")
    response = requests.get(url)
    logger.debug(f"Download completed. Response status code: {response.status_code}")
    json_array = []
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        logger.debug(f"Processing zip file with {len(z.infolist())} files")
        for file_info in z.infolist():
            logger.debug(f"Processing file: {file_info.filename}")
            if file_info.filename.endswith(target_filename):
                extracted_path = os.path.join(target_folder, file_info.filename)
                logger.debug(f"Extracting to path: {extracted_path}")
                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                with z.open(file_info) as f:
                    md_content = f.read().decode('utf-8')
                logger.debug(f"Content extracted, length: {len(md_content)} characters")
                # Create JSON object matching the new format
                json_array.append(create_json_object(md_content, extracted_path.split("/")[-2].replace("_", "-")))
                logger.debug("JSON object created successfully")
    logger.debug(f"Completed processing. Total JSON objects: {len(json_array)}")
    save_json_array(json_array)

def create_json_object(content, path):
    logger.debug(f"Creating JSON object for path: {path}")
    # Generate a unique ID for this prompt
    prompt_id = str(uuid.uuid4())
    version_id = str(uuid.uuid4())
    
    # Extract the name from the path (last part of the path)
    name = path
    
    # Get current timestamp
    current_timestamp = int(time.time())
    
    json_obj = {
        "id": prompt_id,
        "command": f"Fab-{path}",
        "user_id": str(uuid.uuid4()),
        "name": name,
        "content": content,
        "data": {},
        "meta": {},
        "tags": [],
        "is_active": True,
        "version_id": version_id,
        "created_at": current_timestamp,
        "updated_at": current_timestamp,
        "access_grants": [],
        "user": {
            "id": str(uuid.uuid4()),
            "name": "freeload103@yahoo.com",
            "role": "admin",
            "email": "freeload103@yahoo.com"
        },
        "write_access": True
    }
    logger.debug(f"JSON object created successfully with ID: {prompt_id}")
    return json_obj

def save_json_array(json_array):
    logger.debug(f"Saving JSON array with {len(json_array)} objects")
    # Use current timestamp in filename
    current_timestamp = int(time.time())
    filename = f"Fabric_Prompts_Open_WebUI_OpenWebUI_{current_timestamp}.json"
    logger.debug(f"Saving to filename: {filename}")
    with open(filename, 'w') as file:
        json.dump(json_array, file, indent=4)
    logger.debug(f"File saved successfully")
    print(f"Exported to {filename}")

url = "https://github.com/danielmiessler/fabric/archive/refs/heads/main.zip"
target_filename = "system.md"
target_folder = "patterns"

logger.debug(f"Script execution started")
logger.debug(f"URL: {url}")
logger.debug(f"Target filename: {target_filename}")
logger.debug(f"Target folder: {target_folder}")

download_and_extract_to_json(url, target_filename, target_folder)

logger.debug(f"Script execution completed")
