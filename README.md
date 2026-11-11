# 💳🤖 NetPayAssistant

**AI-Powered Developer Toolkit & Payment Middleware for the PayPal Checkout Lifecycle**

NetPayAssistant streamlines PayPal sandbox and e-commerce integrations by automating the **Create → Approve → Capture** state machine, running pre-transaction AI fraud risk assessments, and translating cryptic PayPal API errors into plain-English troubleshooting steps.

---

## 🌟 Why NetPayAssistant Matters

### For Developers & Merchants
* **Plain-English API Diagnostics:** Replaces vague HTTP `400 Bad Request` and `422 Unprocessable Entity` JSON payloads with clear, actionable root-cause explanations in real time.
* **Pre-Transaction Fraud Shield:** Evaluates cart value, buyer email patterns, and IP/location signals *before* hitting payment endpoints, blocking high-risk orders before chargebacks occur.
* **Zero-Database State Machine:** Persists active order states locally (`order_id.txt`) between creation and capture scripts without heavy database or framework overhead.

### For the PayPal Ecosystem
* **Lower Developer Support Burden:** Self-diagnosing error logs reduce integration friction and support tickets for new and experienced builders.
* **Cleaner Transaction Traffic:** Pre-screening suspicious metadata prevents malicious requests from reaching PayPal's core payment channels.

---

## 🏗️ Architecture & Repository Structure

```text
NetPayAssistant/
│
├── create_order.py     # Authenticates via OAuth 2.0, runs AI fraud check, & creates PayPal order
├── capture_order.py    # Reads active order ID & captures payment with AI error diagnostics
├── ai_assistant.py     # NetPayAIAnalyzer: Pre-authorization risk scoring & error translation
├── test_paypal.py      # Validates PayPal Sandbox credentials & OAuth token generation
├── order_id.txt        # Local state persistence between order creation and capture
├── .gitignore          # Excludes .env secrets, caches, and IDE files
└── LICENSE             # MIT Open-Source License
```

---

## ⚡ Quickstart Guide (Run in 2 Minutes)

### 1. Prerequisites
* Python 3.8+
* A free [PayPal Developer Sandbox](https://paypal.com) account (`Client ID` and `Secret`)

### 2. Clone & Install Dependencies
NetPayAssistant is intentionally lightweight and relies only on Python's `requests` library:
```bash
git clone https://github.com
cd NetPayAssistant
pip install requests
```

### 3. Configure Environment Variables
Set your PayPal Sandbox credentials in your terminal (never hardcode secrets):

**Windows (PowerShell):**
```powershell
$env:PAYPAL_CLIENT_ID="your_sandbox_client_id"
$env:PAYPAL_CLIENT_SECRET="your_sandbox_client_secret"
```

**macOS / Linux:**
```bash
export PAYPAL_CLIENT_ID="your_sandbox_client_id"
export PAYPAL_CLIENT_SECRET="your_sandbox_client_secret"
```

### 4. Run the Workflow
```bash
# Step 1: Verify Sandbox credentials
python test_paypal.py

# Step 2: Run AI fraud check & create a PayPal order
python create_order.py

# Step 3: Approve the generated link in your browser, then capture payment
python capture_order.py
```

---

## 🖥️ Example Output

### Pre-Transaction AI Risk Check (`create_order.py`)
```text
[AI Risk Engine] Evaluating transaction metadata...
Risk Score: 15.0 / 100 | Status: LOW RISK
Flags: ['Sandbox/Test domain detected (Normal for testing).']
[PayPal API] Order Created Successfully! Order ID: 0Y506807S1955411D
```

### Plain-English Error Diagnostic (`capture_order.py`)
```text
[PayPal API Error] HTTP 422 - ORDER_NOT_APPROVED
[NetPayAssistant AI Diagnostic]:
  -> Cause: The buyer has not completed checkout approval yet.
  -> Fix: Open the 'approve' link from create_order.py in your browser, log in with a Sandbox Buyer account, and click 'Complete Purchase' before running capture_order.py.
```

---

## 🛠️ Tech Stack
* **Language:** Python 3
* **Payment API:** PayPal REST API v2 (OAuth 2.0, Orders API)
* **HTTP Client:** `requests`
* **AI Engine:** Custom `NetPayAIAnalyzer` heuristic & diagnostic engine

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).


