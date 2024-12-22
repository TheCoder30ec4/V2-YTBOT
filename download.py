import requests
from bs4 import BeautifulSoup
import time

def download(id, link):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'cmlkb203',
    }

    try:
        # Step 1: Post request to get the video download link
        response = requests.post('https://ssstik.io/abc', headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        #print(f"Post request successful for video {id}.")

        # Step 2: Extract the download link
        downloadSoup = BeautifulSoup(response.text, "html.parser")
        try:
            downloadLink = downloadSoup.a["href"]
            #print(f"Download link extracted for video {id}: {downloadLink}")
        except Exception as e:
            #print(f"Could not extract download link for video {id}: {e}")
            return

        # Step 3: Download the video
        video_response = requests.get(downloadLink, headers=headers, stream=True)
        video_response.raise_for_status()  # Ensure the video response is successful

        #print(f"Video response status code for video {id}: {video_response.status_code}")

        # Allow application/octet-stream as valid content type
        if video_response.headers.get("Content-Type") in ["video/mp4", "application/octet-stream"]:
            with open(f"C:/Users/varun/Documents/V2-YTBOT/videos/{id}.mp4", "wb") as output:
                for chunk in video_response.iter_content(chunk_size=4096):
                    if chunk:
                        output.write(chunk)
           # print(f"Video {id} downloaded successfully.")
        else:
            print(f"Invalid content type for video {id}. Expected video/mp4 but got {video_response.headers.get('Content-Type')}.")
            print("Final URL after redirect:", video_response.url)
            

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while processing video {id}: {e}")
