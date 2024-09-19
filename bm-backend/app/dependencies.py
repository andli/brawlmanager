from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App

from app.config import settings

class CustomOAuth2App(StarletteOAuth2App):
    async def save_authorize_data(self, request, redirect_uri, state, **kwargs):
        # Store OAuth data in your custom session state
        request.state.session['state'] = state
        request.state.session['_state_google_' + state] = {
            'redirect_uri': redirect_uri,
            **kwargs
        }

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',  # Updated URL
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=settings.GOOGLE_REDIRECT_URI,  # Ensure this matches your Google Cloud Console setting
    client_kwargs={
        'scope': 'openid email profile',
        'issuer': 'https://accounts.google.com',
    },
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    app=CustomOAuth2App
)