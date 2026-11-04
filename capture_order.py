
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
    
    # The new Order ID generated from your create script
    order_id = "8X315656D7591973J"

    # Step 2: Capture the Payment Order
    capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    capture_response = requests.post(capture_url, headers=headers)

    if capture_response.status_code in [200, 201]:
        capture_json = capture_response.json()
        print("SUCCESS! Payment Captured.")
        print("Transaction ID:", capture_json.get("id"))
        print("Status:", capture_json.get("status"))
    else:
        print("FAILED to capture order:", capture_response.status_code, capture_response.text)
else:
    print("FAILED to get token:", token_response.status_code, token_response.text)