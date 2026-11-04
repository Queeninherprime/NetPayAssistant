
import requests
from requests.auth import HTTPBasicAuth
from ai_assistant import NetPayAIAnalyzer

# Your PayPal Sandbox API Credentials
CLIENT_ID = "BAAhSEw3XOTadnz1QpRNaHPqbUEwsuxjTCZEFXgParHwf-F9Kki-mSHczkT_XVPnUmEB8vz8h48W2Bqg70"
CLIENT_SECRET = "EMY1pR6YyB4WPr1LnC2rtbcT3ifimdV21HhRoW0UXIx5pCiGUvJ_X_ycGWq8NBK8y7LH1iFe7PpADhlH"

# 1. Request an OAuth 2.0 access token
token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
token_response = requests.post(
    token_url,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    headers={"Accept": "application/json", "Accept-Language": "en_US"},
    data={"grant_type": "client_credentials"}
)

if token_response.status_code == 200:
    access_token = token_response.json().get("access_token")
else:
    print(f"FAILED to get token: {token_response.status_code} {token_response.text}")
    exit()

# 2. Read the saved Order ID from order_id.txt
try:
    with open("order_id.txt", "r") as f:
        ORDER_ID = f.read().strip()
    print(f"Loaded Order ID: {ORDER_ID} from order_id.txt")
except FileNotFoundError:
    print("Error: order_id.txt not found. Run create_order.py first!")
    exit()

# 3. Send Capture Request to PayPal
capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{ORDER_ID}/capture"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

capture_response = requests.post(capture_url, headers=headers)

# 4. Handle Response & AI Error Diagnostics
if capture_response.status_code in [200, 201]:
    capture_data = capture_response.json()
    print("\nPayment Captured Successfully!")
    print(f"Status: {capture_data.get('status')}")
    print(f"Transaction ID: {capture_data.get('id')}")
else:
    # AI Assistant catches the error and provides plain-English troubleshooting
    print("\nCapture Failed!")
    ai_diagnosis = NetPayAIAnalyzer.translate_api_error(capture_response.status_code, capture_response.text)
    print(ai_diagnosis)