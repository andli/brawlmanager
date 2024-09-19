from httpx_oauth.clients.google import GoogleOAuth2

from app.config import settings

google_oauth_client = GoogleOAuth2(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET)

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