import os
import requests
from requests.auth import HTTPBasicAuth
from ai_assistant import NetPayAIAnalyzer

# 1. Securely load credentials from environment variables
CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: PAYPAL_CLIENT_ID or PAYPAL_CLIENT_SECRET environment variables are missing!")
    exit(1)

# Mock order context data for the AI layer validation
ORDER_VALUE = 10.00
BUYER_EMAIL = "buyer@example.com"
BUYER_LOCATION = "US"

# 2. Run the AI pre-transaction fraud risk analysis
print("🔄 Running NetPayAIAnalyzer pre-checkout validation...")
fraud_check = NetPayAIAnalyzer.evaluate_checkout_fraud(ORDER_VALUE, BUYER_EMAIL, BUYER_LOCATION)
print(f"📊 AI Fraud Risk Level: {fraud_check['risk_level']} (Score: {fraud_check['risk_score']}/100)")

# Gatekeeper logic: Stop checkout if fraud risk level is explicitly flagged high
if fraud_check.get("risk_level") == "HIGH":
    print("❌ CHECKOUT BLOCKED: NetPayAIAnalyzer identified this request as high risk.")
    exit(1)

# 3. Request an OAuth 2.0 access token using client credentials flow
token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
token_response = requests.post(
    token_url,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    headers={"Accept": "application/json", "Accept-Language": "en_US"},
    data={"grant_type": "client_credentials"}
)

if token_response.status_code == 200:
    print("✅ SUCCESS! Connected to PayPal Sandbox.")
    access_token = token_response.json().get("access_token")
else:
    print(f"❌ FAILED to get token: {token_response.status_code} {token_response.text}")
    exit(1)

# 4. Create the PayPal Checkout Order
order_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}
payload = {
    "intent": "CAPTURE",
    "purchase_units": [
        {
            "amount": {
                "currency_code": "USD",
                "value": f"{ORDER_VALUE:.2f}"
            }
        }
    ]
}

order_response = requests.post(order_url, headers=headers, json=payload)

if order_response.status_code == 201:
    order_data = order_response.json()
    order_id = order_data["id"]
    print(f"🎉 Order Created Successfully! Order ID: {order_id}")
    
    # Securely handoff state via local text file for capture_order.py
    with open("order_id.txt", "w") as f:
        f.write(order_id)
    print("💾 Saved Order ID state to order_id.txt")

    # Print out user authorization flow URL 
    for link in order_data.get("links", []):
        if link["rel"] == "approve":
            print(f"\n🔗 Copy and paste this Approval URL into your browser:\n{link['href']}\n")
else:
    print("❌ FAILED to create order.")
    # Pass raw failure diagnostics through your AI assistant error parsing module
    if hasattr(NetPayAIAnalyzer, 'translate_api_error'):
        translated_err = NetPayAIAnalyzer.translate_api_error(order_response.status_code, order_response.text)
        print(f"🤖 AI Diagnostic Assistant Response: {translated_err}")
    else:
        print(f"Raw Status Code: {order_response.status_code} | Payload: {order_response.text}")
