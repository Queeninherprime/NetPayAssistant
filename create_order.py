import requests
from requests.auth import HTTPBasicAuth
from ai_assistant import NetPayAIAnalyzer

# Your PayPal Sandbox API Credentials
CLIENT_ID = "BAAhSEw3XOTadnz1QpRNaHPqbUEwsuxjTCZEFXgParHwf-F9Kki-mSHczkT_XVPnUmEB8vz8h48W2Bqg70"
CLIENT_SECRET = "EMY1pR6YyB4WPr1LnC2rtbcT3ifimdV21HhRoW0UXIx5pCiGUvJ_X_ycGWq8NBK8y7LH1iFe7PpADhlH"

# 1. Request an OAuth 2.0 access token using client credentials flow
token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
token_response = requests.post(
    token_url,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    headers={"Accept": "application/json", "Accept-Language": "en_US"},
    data={"grant_type": "client_credentials"}
)

    

# Run fraud check on order payload
fraud_check = NetPayAIAnalyzer.evaluate_checkout_fraud(10.00, "buyer@example.com", "US")
print(f"AI Fraud Risk Level: {fraud_check['risk_level']} (Score: {fraud_check['risk_score']})")


if token_response.status_code == 200:
    print("SUCCESS! Connected to PayPal Sandbox.")
    access_token = token_response.json().get("access_token")
else:
    print(f"FAILED to get token: {token_response.status_code} {token_response.text}")
    exit()

# 2. Create an Order
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
                "value": "10.00"
            }
        }
    ]
}

order_response = requests.post(order_url, headers=headers, json=payload)

if order_response.status_code == 201:
    order_data = order_response.json()
    order_id = order_data["id"]
    print(f"Order Created Successfully! Order ID: {order_id}")
    
    # Automatically save order ID to a local text file for capture_order.py
    with open("order_id.txt", "w") as f:
        f.write(order_id)
    print("Saved Order ID to order_id.txt")

    # Print the approval URL for the browser
    for link in order_data.get("links", []):
        if link["rel"] == "approve":
            print(f"\nCopy and paste this Approval URL into your Incognito browser:\n{link['href']}\n")
else:
    print(f"FAILED to create order: {order_response.status_code} {order_response.text}")