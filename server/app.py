from flask import Flask
from flask_restful import Resource, Api

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from .text_normalize import normalize_corpus

CLIENT_SECRETS_FILE = 'google_api_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def find_videos(youtube, ingredients):
    # 1. search videos using list of ingredients
    # 2. for each response (=video), look into title & shortened description
    #    and count # of ingredients that each video has
    # 3. pick best 3 or 5 videos and extract video title, url, match count
    # 4. if need further analysis, do 'video' request and do 2) again in video.description
    # TODO: extract all ingredients and see if too many ingredients are missing
    search_query = " ".join(ingredients.append("recipe"))
    response = youtube.search().list(
        q=search_query,
        part='id,snippet(title,description,thumbnails)',
        eventType="completed"
    ).execute()

    checklists, candidates = dict(), dict()
    for video in response.items:
        # TODO: normalize video.snippet.title & video.snippet.description
        ingredients_checklist = Checklist(ingredients)
        video_id = video.id.videoId

        ingredients_checklist.parse(video.snippet.title)
        ingredients_checklist.parse(video.snippet.description)

        if ingredients_checklist.count_checked() > len(ingredients_checklist) - 2:
            candidates[video_id] = ingredients_checklist
        else:
            checklists[video_id] = ingredients_checklist

    if len(candidates) < 5:
        # TODO: go over checklists and select best ones
        pass

    # TODO: merge response.items and candidates and return


class Checklist:
    def __init__(self, items):
        self.items = items
        self.checklist = {item: False for item in items}

    def __len__(self):
        return len(self.checklist)

    def check(self, item):
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

    def parse(text):
        """
    sample ingredients_checklist: {"onion": False, "beef brisket": True}
    TODO: set value to True if ingredient is found
    """
        return {}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
