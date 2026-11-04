# 🚀 NetPayAssistant

**NetPayAssistant** is a Python-based backend integration project built for seamless payment processing using the PayPal Sandbox API. Designed with automated session handling and dynamic order tracking, it streamlines the creation and capture of secure payment transactions.

---

## 🛠️ Tech Stack & Environment
* **Language:** Python 3
* **Environment:** Windows / VS Code
* **API Integration:** PayPal REST API (`v1/oauth2/token`, `v2/checkout/orders`)[cite: 1]
* **Version Control:** Git & GitHub (`Queeninherprime/NetPayAssistant`)[cite: 1]

---

## 📂 Project Structure
```text
NetPayAssistant/
│
├── create_order.py     # Authenticates, creates a $10.00 order, and saves the Order ID
├── capture_order.py    # Automatically reads the saved Order ID and captures the payment
├── test_paypal.py      # Verifies sandbox connection and OAuth2 token retrieval
├── order_id.txt        # Dynamically stores the active transaction token (auto-generated)
├── .gitignore          # Secures credentials and temporary files
└── README.md           # Project documentation
