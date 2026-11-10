import os
import requests
from requests.auth import HTTPBasicAuth
from ai_assistant import NetPayAIAnalyzer

# 1. Securely load credentials from environment variables
CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERROR: PAYPAL_CLIENT_ID or PAYPAL_CLIENT_SECRET environment variables are missing!")
    exit(1)

# 2. Request an OAuth 2.0 access token using client credentials flow
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
    print(f"❌ FAILED to get token: {token_response.status_code} {token_response.text}")
    exit(1)

# 3. Read the saved active transaction state from order_id.txt
try:
    with open("order_id.txt", "r") as f:
        ORDER_ID = f.read().strip()
    if not ORDER_ID:
        raise ValueError("order_id.txt is empty.")
    print(f"💾 Loaded Order ID state: {ORDER_ID}")
except (FileNotFoundError, ValueError):
    print("❌ ERROR: Active Order ID state missing. Run create_order.py and approve the checkout flow first!")
    exit(1)

# 4. Send the Capture Request to the PayPal Sandbox API
capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{ORDER_ID}/capture"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

print("🔄 Attempting to capture payment with PayPal API...")
capture_response = requests.post(capture_url, headers=headers)

# 5. Handle Response & AI Error Diagnostics
if capture_response.status_code in:
    capture_data = capture_response.json()
    print("\n🎉 Payment Captured Successfully!")
    print(f"💳 Status: {capture_data.get('status')}")
    print(f"🔑 Transaction ID: {capture_data.get('id')}")
else:
    print("\n❌ Capture Failed!")
    print(f"Raw Status Code: {capture_response.status_code}")
    print("🔄 Passing raw payload to NetPayAIAnalyzer diagnostic engine...")
    
    # AI Assistant extracts the schema and gives plain-English troubleshooting steps
    ai_diagnosis = NetPayAIAnalyzer.translate_api_error(capture_response.status_code, capture_response.text)
    print(f"\n🤖 AI Diagnostic Assistant Response:\n{ai_diagnosis}")


  
