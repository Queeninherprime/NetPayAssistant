import requests
from requests.auth import HTTPBasicAuth

# Your PayPal Sandbox API Credentials
CLIENT_ID = "BAAhSEw3XOTadnz1QpRNaHPqbUEwsuxjTCZEFXgParHwf-F9Kki-mSHczkT_XVPnUmEB8vz8h48W2Bqg70"
CLIENT_SECRET = "EMY1pR6YyB4WPr1LnC2rtbcT3ifimdV21HhRoW0UXIx5pCiGUvJ_X_ycGWq8NBK8y7LH1iFe7PpADhlH"

# PayPal Sandbox API URL for getting an Access Token
url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

# Request an OAuth 2.0 access token using Client Credentials flow
response = requests.post(
    url,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    headers={"Accept": "application/json", "Accept-Language": "en_US"},
    data={"grant_type": "client_credentials"}
)

# Print the result
if response.status_code == 200:
    print("SUCCESS! Connected to PayPal Sandbox.")
    token_data = response.json()
    print("Access Token received:", token_data.get("access_token")[:20] + "...")
else:
    print("FAILED to connect:", response.status_code, response.text)