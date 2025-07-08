from flask import Flask, render_template
import requests
import json
from urllib.parse import quote

app = Flask(__name__)

# Backup meme URLs in case API fails
DEFAULT_MEMES = [
    "https://i.imgflip.com/4/1bij.jpg",  # One Does Not Simply
    "https://i.imgflip.com/4/1bgw.jpg",  # Distracted Boyfriend
    "https://i.imgflip.com/4/1bh8.jpg"   # Batman Slapping Robin
]

def get_meme():
    try:
        url = "https://meme-api.herokuapp.com/gimme"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        # Check if response is valid JSON        try:
            data = response.json()
        except ValueError:
            raise Exception("Invalid JSON response from API")
            
        # Safely extract values with fallbacks
        meme_url = data.get("url", DEFAULT_MEMES[0])
        if "preview" in data and len(data["preview"]) >= 2:
            meme_url = data["preview"][-2]
            
        subreddit = data.get("subreddit", "unknown")
        return meme_url, subreddit
        
    except Exception as e:
        print(f"Error fetching meme: {e}")
        # Return a default meme and error message
        import random
        return random.choice(DEFAULT_MEMES), "api-error"

@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)#! /bin/python 

from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

def get_meme(): 
        url = "https://meme-api.herokuapp.com/gimme"
        response = json.loads(requests.request("GET", url).text)
        meme_large = response["preview"][-2]
        subreddit = response["subreddit"]
        return meme_large, subreddit
@app.route("/")
def index(): 
        meme_pic, subreddit = get_meme()
        return render_template("meme_index.html", meme_pic = meme_pic, subreddit = subreddit)

app.run(host ="0.0.0.0", port = 5000)
