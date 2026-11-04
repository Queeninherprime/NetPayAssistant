import requests
from requests.auth import HTTPBasicAuth

# Your PayPal Sandbox API Credentials
CLIENT_ID = "BAAFJI9ugIeqEQrSHQcMv6T6fFJl-ob7ZzVhiTm_Hzjme34vMEULQuukyR88K3OxmcAfDCFZOi6nhJoCP0"
CLIENT_SECRET = "EHLaoLlF0ObIoBDZZZNn9XLzQqJ5OyNf7amz90Kcq70UgWG6vemS_nKnsguO9Pc4EpXgeBz_zNdlxnOJ"

# Step 1: Get the Access Token
token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
token_response = requests.post(
    token_url,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    headers={"Accept": "application/json", "Accept-Language": "en_US"},
    data={"grant_type": "client_credentials"}
)

if token_response.status_code == 200:
    access_token = token_response.json().get("access_token")

    # Step 2: Create a Test Order for $10.00 USD
    order_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    order_data = {
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

    order_response = requests.post(order_url, headers=headers, json=order_data)
    
    if order_response.status_code == 201:
        order_json = order_response.json()
        print("SUCCESS! Test Payment Order Created.")
        print("Order ID:", order_json.get("id"))
        
        # Look for the approval link in the PayPal response
        for link in order_json.get("links", []):
            if link.get("rel") == "approve":
                print("\n👉 Copy and open this link in your browser to approve the payment:")
                print(link.get("href"))
    else:
        print("FAILED to create order:", order_response.status_code, order_response.text)
else:
    print("FAILED to get token:", token_response.status_code, token_response.text)
        