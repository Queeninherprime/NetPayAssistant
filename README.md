# NetPayAssistant 💳🤖

**NetPayAssistant** is an AI-powered developer toolkit and payment middleware designed to streamline the PayPal checkout lifecycle. Built for modern e-commerce and developer workflows, it automates the **Create-Approve-Capture** state machine, offers local transaction state persistence, and integrates custom AI analytics to detect fraud risks and provide human-readable API diagnostics.

---

## 🌟 Importance to Users & to PayPal

### **To Users (Shoppers & Merchants)**
* **Seamless Checkout Experience:** Customers enjoy frictionless online payments through PayPal’s trusted checkout environment.
* **Pre-Transaction AI Protection:** Merchants are protected from fraud *before* chargebacks happen, thanks to automated AI risk analysis on transaction details (cart value, buyer email, location).
* **Faster Problem Resolution:** Clear error reporting reduces abandoned carts caused by payment glitches.

### **To PayPal (Ecosystem & Platform)**
* **Lower Support Burden:** Instead of vague HTTP errors (`400 Bad Request` or `422 Unprocessable Entity`), developers receive plain-English diagnostics, cutting down on integration support tickets.
* **Enhanced Fraud Shielding:** Intelligent pre-validation ensures fewer high-risk or malicious transactions hit PayPal's main payment processing channels.
* **Developer Adoption:** Clean, open middleware makes integrating PayPal APIs accessible to engineers of all skill levels.

---

## ⚡ Key Advantages & Benefits for the Public

* **🤖 AI-Driven Error Diagnostic Engine:** Converts cryptic API response payloads into clear, actionable troubleshooting steps for developers in real time.
* **🛡️ Smart Risk Analysis:** Calculates a real-time risk score (`LOW`, `MEDIUM`, or `HIGH`) before interacting with payment endpoints.
* **🔄 Zero-Database State Machine:** Uses local file-piping (`order_id.txt`) to hand off active transaction states smoothly between `create_order.py` and `capture_order.py`.
* **⚡ Lightweight & Dependency-Free:** Relies only on Python's native `requests` library without heavy framework overhead.

---

## 📁 Repository Structure

```text
NetPayAssistant/
│
├── create_order.py     # Requests OAuth 2.0 token, runs AI fraud check, & creates PayPal order
├── capture_order.py    # Reads order ID & completes payment capture with AI error handling
├── ai_assistant.py     # AI module: NetPayAIAnalyzer (Fraud Scoring & Error Translation)
├── test_paypal.py      # Environment & sandbox credential validation script
├── order_id.txt        # Local state storage for piping active order IDs between scripts
├── .gitignore          # Excludes environment files, caches, and local tracking files
└── README.md           # Project documentation
