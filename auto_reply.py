import requests
import openai
import time
import os
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Instagram API credentials
instagram_access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
instagram_post_id = os.getenv("INSTAGRAM_POST_ID")
ig_user_id = os.getenv("IG_USER_ID")

def reply_comment(comments):
    for comment in comments:
        media_id = comment['value']['media']['id']
        from_id = comment['value']['from']['id']
        if media_id != instagram_post_id:
            continue
        if from_id == ig_user_id:
            continue
        
        comment_text = comment['value']['text']
        comment_id = comment['value']['id']
        auto_reply = generate_auto_reply(comment_text)

        # Post the auto-reply as a comment on Instagram
        post_comment(comment_id, auto_reply)


# Generate auto-reply using GPT-3.5 model
def generate_auto_reply(comment_text):
    prompt = f"Reply to the comment: {comment_text}\n\nAuto-reply:"
    messages = {
        "role": "user",
        "content": comment_text
    }
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # Specify GPT-3.5 model
        messages=[messages],
        # max_tokens=50,  # Adjust the number of tokens for desired response length
        n=1,  # Generate a single response
        stop=None,  # Add custom stop conditions if desired
    )
    print("getting response for: " + comment_text)

    auto_reply = response.choices[0].message.content.strip()
    return auto_reply


# Post comment on Instagram
def post_comment(comment_id, comment_text):
    url = f"https://graph.facebook.com/{comment_id}/replies"
    params = {
        "access_token": instagram_access_token,
        "message": comment_text
    }

    response = requests.post(url, params=params)
    print(response.text)
    if response.status_code == 200:
        print("Comment posted successfully.")
    else:
        print("Failed to post comment.")
