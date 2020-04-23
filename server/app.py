from flask import Flask
from flask_restful import Resource, Api

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'google_api_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world'}

# Authorize the request and store autorization credentials.
def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def find_videos(youtube, ingredients):
  pass

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')