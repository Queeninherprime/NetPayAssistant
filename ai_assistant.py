"""
NetPayAssistant - AI Capabilities Module
Provides intelligent transaction risk scoring and plain-English API error diagnostics.
"""

import json

class NetPayAIAnalyzer:
    
    @staticmethod
    def evaluate_checkout_fraud(cart_value: float, customer_email: str, ip_location: str) -> dict:
        """
        AI-Powered Checkout Fraud Detector:
        Analyzes transaction metadata to compute a pre-authorization risk score.
        """
        risk_score = 10.0  # Base risk score out of 100
        flags = []

        # Check for high-risk domains or patterns in sandbox/test emails
        if "test" in customer_email or "example.com" in customer_email:
            risk_score += 5.0
            flags.append("Sandbox/Test domain detected (Normal for testing).")

        # Check cart amount anomalies
        if cart_value > 5000.0:
            risk_score += 40.0
            flags.append("High-value transaction threshold exceeded.")
        elif cart_value <= 0:
            risk_score += 80.0
            flags.append("Invalid or zero-dollar transaction amount.")

        # Determine risk level category
        if risk_score < 30:
            risk_level = "LOW"
            recommendation = "Approve transaction automatically."
        elif risk_score < 70:
            risk_level = "MEDIUM"
            recommendation = "Proceed with standard 2-step verification."
        else:
            risk_level = "HIGH"
            recommendation = "Flag for manual merchant review or step-up authentication."

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "flags": flags,
            "action_recommendation": recommendation
        }

    @staticmethod
    def translate_api_error(status_code: int, error_response_text: str) -> str:
        """
        AI Transaction Assistant:
        Interprets raw, cryptic PayPal API error responses and translates them 
        into plain-English, actionable solutions for developers.
        """
        try:
            error_json = json.loads(error_response_text)
            error_name = error_json.get("name", "UNKNOWN_ERROR")
            error_desc = error_json.get("message", "No description provided.")
        except json.JSONDecodeError:
            error_name = "PARSE_ERROR"
            error_desc = error_response_text

        # Intelligent diagnosis mapping
        if status_code == 404 or "RESOURCE_NOT_FOUND" in error_name:
            return (
                f"🤖 [AI Assistant Diagnosis]: 404 Not Found ({error_name})\n"
                f"   - Why it happened: The Order ID referenced does not exist or has already been captured.\n"
                f"   - How to fix: Run 'python create_order.py' to generate a fresh order token, "
                f"or check if your 'order_id.txt' file is pointing to an old transaction."
            )
        elif status_code == 400 or "UNPROCESSABLE_ENTITY" in error_name:
            return (
                f"🤖 [AI Assistant Diagnosis]: 400 Bad Request ({error_name})\n"
                f"   - Why it happened: The payload structure or transaction state is invalid. "
                f"For example, you might be trying to capture an order that the buyer hasn't approved yet, "
                f"or you attempted a merchant self-purchase using identical business credentials.\n"
                f"   - How to fix: Ensure you completed the approval step in an Incognito window using your "
                f"Personal Buyer account, not your Business Merchant account."
            )
        elif status_code == 401 or "AUTHENTICATION_FAILURE" in error_name:
            return (
                f"🤖 [AI Assistant Diagnosis]: 401 Unauthorized ({error_name})\n"
                f"   - Why it happened: Your Client ID or Client Secret is invalid or expired.\n"
                f"   - How to fix: Check your PayPal Developer Dashboard credentials and update them in your scripts."
            )
        else:
            return (
                f"🤖 [AI Assistant Diagnosis]: HTTP {status_code} - {error_name}\n"
                f"   - Details: {error_desc}\n"
                f"   - Action: Review the PayPal REST API v2 documentation for this specific status code."
            )

# Quick local test execution
if __name__ == "__main__":
    print("--- Testing AI Fraud Detector ---")
    fraud_report = NetPayAIAnalyzer.evaluate_checkout_fraud(10.00, "sb-exi1a53715423@personal.example.com", "US")
    print(json.dumps(fraud_report, indent=2))

    print("\n--- Testing AI Error Assistant ---")
    mock_error = '{"name": "RESOURCE_NOT_FOUND", "message": "Specified resource ID does not exist."}'
    diagnosis = NetPayAIAnalyzer.translate_api_error(404, mock_error)
    print(diagnosis)
