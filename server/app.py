from flask import Flask
from flask_restful import Resource, Api

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from .text_normalize import normalize

CLIENT_SECRETS_FILE = 'google_api_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = Flask(__name__)
api = Api(app)

ALLOWED_NUM_MISSING_INGREDIENT = 2


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

    selected, candidates = [], []
    for video in response.items:
        ingredients_checklist = Checklist(ingredients)
        normalized_title = normalize(video.snippet.title)
        normalized_desc = normalize(video.snippet.description)

        ingredients_checklist.parse(normalized_title)
        ingredients_checklist.parse(normalized_desc)

        if len(ingredients_checklist) - ingredients_checklist.count_checked() <= ALLOWED_NUM_MISSING_INGREDIENT:
            selected.append((video, ingredients_checklist))
        else:
            candidates.append((video, ingredients_checklist))

    for video, ingredients_checklist in candidates:
        if len(selected) < 5:
            break

        response = youtube.videos().list(
            part="snippet",
            id=video.id.videoId
        ).execute()
        video_detail = response.items[0]
        normalized_desc = normalize(video_detail.snipet.description)

        ingredients_checklist.parse(normalized_desc)

        if len(ingredients_checklist) - ingredients_checklist.count_checked() <= ALLOWED_NUM_MISSING_INGREDIENT:
            selected.append((video, ingredients_checklist))

    response = [{'id': video.id, 'snippet': video.snippet, 'checklist': checklist} for video, checklist in selected]
    return response


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
        for word in text:
            if word in items:
                self.checkoff(word)


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
