import os
import requests
from requests.auth import HTTPBasicAuth

# Securely retrieve PayPal Sandbox API Credentials from environment variables
CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET")

# Validation check to ensure variables are set
if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: PAYPAL_CLIENT_ID or PAYPAL_CLIENT_SECRET environment variables are missing!")
    exit(1)

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
