from groq import Groq
import pandas as pd
import json
import io 

def call_ai(promt: str, api: str):
    try:
        client = Groq(api_key=api)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': "system",
                    "content": """You are a content creator on YouTube, producing engaging videos on interesting and lesser-known 
                    facts from a wide range of topics, including science, history, technology, pop culture, and nature. 
                    Your goal is to present these facts in a fun, accessible, and informative way, using storytelling techniques, visuals, and a dynamic presentation style that appeals to a broad audience. 
                    Your content is aimed at sparking curiosity and encouraging viewers to explore new ideas and perspectives."""
                },
                {
                    "role": "system",
                    "content": f"""You are a creative content generator for YouTube Shorts. Based on the provided: {promt}, 
                    create a JSON output containing the following:
                    
                    'Title': 'A catchy and intriguing title that captures the audience's attention.'
                    'Description': 'A concise, engaging description of the video, summarizing its content and inviting viewers to watch.'
                    'Hashtags': 'Relevant and trending hashtags to maximize the video's reach and engagement.'
                    'categoryId': 'According to the prompt given, provide the categoryId as a plain numerical value, Provide a numerical value without any comments or extra text (e.g., 22 for People & Blogs).: 
                        1 - Film & Animation, 2 - Autos & Vehicles, 10 - Music, 15 - Pets & Animals, 17 - Sports, 
                        19 - Travel & Events, 20 - Gaming, 22 - People & Blogs, 23 - Comedy, 24 - Entertainment, 
                        25 - News & Politics, 26 - How-to & Style, 27 - Education, 28 - Science & Technology.'

                    
                    Ensure the content is optimized for the platform and aligns with the tone and topic of the prompt. Make it attention-grabbing and share-worthy for YouTube Shorts."""
                },
            ],
            model="llama3-8b-8192"
        )
        response_content = chat_completion.choices[0].message.content
        #print("Raw API Response Content:", response_content)
        return response_content
    except Exception as e:
        #print(f"An error occurred during API call: {e}")
        return None


def save_json(input_string: str) -> None:
    try:
            
        
        clean_input_string = input_string[input_string.find('{'):input_string.rfind('}')+1]
        json_data_cleaned = json.dumps(clean_input_string, indent=4)
        json_data = json.loads(json_data_cleaned)
        with io.open("desc.json","w", encoding='utf-8') as json_file:
            json_file.write(json_data.strip())
                
        #print("Successfully Genrated the idea🌟")
            
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

# Load data and process the second video description
# df = pd.read_csv('./data/tiktok_collected_liked_videos.csv')
# video_description = df['video_desc'][2]
# print("Processing Video Description:", video_description)

# response = call_ai(promt=video_description, api="")
# if response:
#     save_json(response)
# else:
#     print("API call failed. Could not generate metadata.")
