from flask import session
import os

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError

from dotenv import load_dotenv
load_dotenv()

class GoogleLogin:
    def __init__(self):
        
        self.google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.google_client_secret = os.getenv('GOOGLE_SECRET_KEY')
        self.google_redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        
        self.flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.google_client_id, 
                    "project_id":"visapro-423107",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": self.google_client_secret,
                    "redirect_uris":["http://localhost:8080/callback","https://visapro.azurewebsites.net/callback"]
                }
            },
            scopes=["https://www.googleapis.com/auth/userinfo.email",
                    "openid", "https://www.googleapis.com/auth/userinfo.profile"],
            redirect_uri=self.google_redirect_uri
        )
        
    def login(self):
        try:
            auth_uri, state = self.flow.authorization_url(access_type='offline')
            session['state'] = state
            return auth_uri, state
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500
    
    def callback(self, request):
        try:
            if 'state' not in session or 'state' not in request.args:
                return 'State parameter missing', 400

            if session.get('state') != request.args['state']:
                return 'State does not match!', 400

            self.flow.fetch_token(authorization_response=request.url)
            credentials = self.flow.credentials
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()

            session["email"] = user_info.get('email')
            session["name"] = user_info.get('name')
            session["picture"] = user_info.get('picture')
            session["google_id"] = user_info.get('id')
            session["threads"] = [] 
            
            return True, 200
        
        except GoogleAuthError as e:
            return f"An error occurred during the OAuth flow: {str(e)}", 500
        
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500
        
    def logout(self):
        try:
            session.clear()
            return True, 200
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500