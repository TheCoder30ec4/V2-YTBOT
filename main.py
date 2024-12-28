from download import download
from upload_YT import authenticate_youtube, upload_video
from video_descriptor import call_ai, save_json
import pandas as pd
import json
import os
import time
from tqdm import tqdm

def normalize_keys(data, expected_keys):
    """
    Normalize keys in the JSON data to match expected keys.

    :param data: Dictionary with original keys
    :param expected_keys: Dictionary mapping expected keys to possible variations
    :return: Dictionary with normalized keys
    """
    normalized_data = {}
    for expected_key, variations in expected_keys.items():
        for key in data.keys():
            if key.lower() in [v.lower() for v in variations]:
                normalized_data[expected_key] = data[key]
                break
    return normalized_data

def main():
    expected_keys = {
        "Title": ["title", "heading"],
        "Description": ["description", "desc"],
        "Hashtags": ["hashtags", "tags"],
        "categoryId": ["categoryid", "category"]
    }

    for i in tqdm(os.listdir('data'), desc="Processing CSV files"):
        if i.endswith('.csv') and os.path.isfile(os.path.join('data', i)):
            df = pd.read_csv(f'./data/{i}')

            for index, row in tqdm(df.iterrows(), desc="Processing rows in CSV", total=len(df), leave=False):
                try:
                    video_desc = row['video_desc']
                    video_link = row['video_link']
                    video_title = row['video_id']

                    # Download video
                    download(id=video_title, link=video_link)

                    # Generate AI metadata
                    response = call_ai(promt=video_desc, api="")
                    if response:
                        save_json(response)
                    else:
                        print("API call failed. Could not generate metadata.")
                        continue

                    # Read AI metadata
                    with open("desc.json", "r", encoding="utf-8") as json_file:
                        content = json_file.read()

                        if not content.strip():
                            raise ValueError("desc.json is empty or invalid.")

                        raw_data = json.loads(content)
                        data = normalize_keys(raw_data, expected_keys)

                    # Validate normalized data
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        raise ValueError(f"Missing keys in JSON data: {missing_keys}")

                    # Upload video to YouTube
                    upload_video(
                        youtube,
                        file_path=f"C:/Users/varun/Documents/V2-YTBOT/videos/{video_title}.mp4",
                        title=data['Title'],
                        desc=data['Description'],
                        hastags=data['Hashtags'],
                        id=data['categoryId']
                    )
                    if upload_video:
                        os.remove('./videos/{video_title}.mp4')

                except KeyError as e:
                    print(f"Missing key in CSV or JSON: {e}")
                except ValueError as e:
                    print(f"Validation error: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

                # Optional: Add a short delay between uploads
                time.sleep(900)

if __name__ == "__main__":
    youtube = authenticate_youtube()
    if youtube:
        main()
