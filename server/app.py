from flask import Flask
from flask_restful import Resource, Api
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account

from server.text_normalize import normalize

GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_FILE = '/home/joonh/dev/FridgeScraper/server/google_service_account_private_key.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = Flask(__name__)


@app.route('/search/<ingredients>')
def search_videos(ingredients):
    youtube = get_authenticated_service()
    return find_videos(youtube, ingredients.split(","))

ALLOWED_MISSING_INGREDIENTS_RATIO = 0.3


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_FILE)
    scoped_credentials = credentials.with_scopes(SCOPES)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def find_videos(youtube, ingredients):
    # 1. search videos using list of ingredients
    # 2. for each response (=video), look into title & shortened description
    #    and count # of ingredients that each video has
    # 3. pick best 3 or 5 videos and extract video title, url, match count
    # 4. if need further analysis, do 'video' request and do 2) again in video.description
    search_query = ",".join(ingredients + ["recipe"])

    # TODO: remove this after developing
    # search_result = {}
    # with open("/home/joonh/dev/FridgeScraper/server/sample_search_result.json") as f_in:
    #     search_result = json.load(f_in)

    search_result = youtube.search().list(
        q=search_query,
        part='id,snippet',
        type="video",
        videoDuration="medium",
        videoDimension="2d",
        videoDefinition="high",
    ).execute()

    selected, candidates = [], []
    for video in search_result.get("items"):
        ingredients_checklist = Checklist(ingredients)
        # TODO: normalize these when everything works
        normalized_title = normalize(video["snippet"]["title"])
        normalized_desc = normalize(video["snippet"]["description"])

        ingredients_checklist.parse(normalized_title)
        ingredients_checklist.parse(normalized_desc)

        if ingredients_checklist.count_unchecked() / len(ingredients_checklist) < ALLOWED_MISSING_INGREDIENTS_RATIO:
            selected.append((video, ingredients_checklist))
        else:
            candidates.append((video, ingredients_checklist))

    for video, ingredients_checklist in candidates:
        if len(selected) >= 5:
            break

        video_search_result = youtube.videos().list(
            part="snippet",
            id=video["id"]["videoId"]
        ).execute()
        video_detail = video_search_result["items"][0]
        normalized_desc = normalize(video_detail["snippet"]["description"])

        ingredients_checklist.parse(normalized_desc)

        if ingredients_checklist.count_unchecked() / len(ingredients_checklist) < ALLOWED_MISSING_INGREDIENTS_RATIO:
            selected.append((video, ingredients_checklist))

    response = [{'id': video["id"], 'snippet': video["snippet"], 'checklist': checklist.checklist} for video, checklist in selected]
    return json.dumps(response)


class Checklist:
    def __init__(self, items):
        self.items = items
        self.checklist = {item.lower(): False for item in items}

    def __len__(self):
        return len(self.checklist)

    def checkoff(self, item):
        if item in self.checklist:
            self.checklist[item] = True

    def count_unchecked(self):
        count = 0
        for item in self.checklist:
            if not self.checklist[item]:
                count += 1
        return count

    def count_checked(self):
        count = 0
        for item in self.checklist:
            if self.checklist[item]:
                count += 1
        return count

    def is_all_checked(self):
        return self.count_checked() == len(self)

    def unchecked_items(self):
        return {item: checked for item, checked in self.checklist if checked}

    def parse(self, text):
        """
        set value to True if ingredient is found
        sample ingredients_checklist: {"onion": False, "beef brisket": True}
        """
        items = set(self.items)
        for word in self.items:
            if word in text:
                self.checkoff(word)
