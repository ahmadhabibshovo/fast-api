import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from jose import jwt

# TODO: Replace these with your actual Client IDs from Google Cloud Console and Apple Developer Portal
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
APPLE_CLIENT_ID = "com.yourcompany.yourapp"

def verify_google_token(token: str):
    try:
        # Verify the token against Google's servers
        # We pass the client ID to ensure the token was meant for our app
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        return {"email": idinfo.get("email"), "sub": idinfo.get("sub"), "name": idinfo.get("name")}
    except ValueError:
        # Invalid token
        return None

def get_apple_public_key(kid):
    try:
        response = requests.get("https://appleid.apple.com/auth/keys")
        keys = response.json().get("keys", [])
        for key in keys:
            if key["kid"] == kid:
                return key
    except Exception as e:
        print(f"Failed to fetch Apple public keys: {e}")
    return None

def verify_apple_token(token: str):
    try:
        # Get the unverified header to find out which key was used
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        
        # Fetch the corresponding public key from Apple
        key = get_apple_public_key(kid)
        if not key:
            return None
            
        # Verify the token
        payload = jwt.decode(
            token, 
            key, 
            algorithms=["RS256"], 
            audience=APPLE_CLIENT_ID,
            # Apple tokens can be tricky with issuer depending on the exact flow, so we might need to adjust options
            options={"verify_iss": False} 
        )
        return {"email": payload.get("email"), "sub": payload.get("sub")}
    except Exception as e:
        print(f"Apple verification error: {e}")
        return None
