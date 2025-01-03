import os
#import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http


def authenticate_youtube(scopes=["https://www.googleapis.com/auth/youtube.upload"],TOKEN_FILE = 'token.json' ):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

    # Load client secrets file, put the path of your file
    client_secrets_file = "client.json"

    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes
    )
    credentials = flow.run_local_server(port=8080)

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    return youtube

def upload_video(youtube, file_path,title,desc,hastags,id):
    request_body = {
        "snippet": {
            "categoryId": f"{id}",
            "title": f"{title}",
            "description":f"{desc} " + f"\n\n{hastags}",
            "tags": [],
        },
        "status":{
            "privacyStatus": "public"
        }
    }

    # put the path of the video that you want to upload
    media_file = f"{file_path}"

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
    )

    response = None 

    while response is None:
        status, response = request.next_chunk()
        # if status:
        #     print(f"Upload {int(status.progress()*100)}%")

        print(f"Video uploaded with ID: {response['id']}")

# if __name__ == "__main__":
#     youtube = authenticate_youtube()
    
    
#     upload_video(youtube)

