import os
import requests
import json
import random
from dotenv import load_dotenv
# Environment variables (replace with your actual values or os.environ.get)

app_key = os.getenv("APP_KEY", "your_app_key")
partner_id = os.getenv("PARTNER_ID", "your_partner_id")
partner_secret = os.getenv("PARTNER_SECRET", "your_partner_secret")
base_url = os.getenv("BASE_URL", "https://api.finicity.com")

# Step 1: Get App Token
token_url = f"{base_url}/aggregation/v2/partners/authentication"  # replace with your token endpoint
def end_to_end_url():
    token_payload = {
        "partnerId": partner_id,
        "partnerSecret": partner_secret
    }

    token_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Finicity-App-Key": app_key
    }

    response = requests.post(token_url, headers=token_headers, json=token_payload)
    response.raise_for_status()  # Raise exception on HTTP error
    app_token = response.json().get("token")
    print("App Token:", app_token)

    # Step 2: Create customer
    customer_url = f"{base_url}/aggregation/v2/customers/testing"

    customer_payload = {
        "username": f"customerusername{random.randint(100, 200)}"
    }

    customer_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Finicity-App-Key": app_key,
        "Finicity-App-Token": app_token
    }

    response = requests.post(customer_url, headers=customer_headers, json=customer_payload)
    response.raise_for_status()
    customer_id = response.json().get("id")
    print("Customer ID:", customer_id)

    # Step 3: Generate connect link
    connect_url = f"{base_url}/connect/v2/generate"

    connect_payload = {
        "partnerId": partner_id,
        "customerId": customer_id
    }

    connect_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Finicity-App-Key": app_key,
        "Finicity-App-Token": app_token
    }

    response = requests.post(connect_url, headers=connect_headers, json=connect_payload)
    response.raise_for_status()
    link = response.json().get("link")
    print("Generated Connect Link:", link)
    return link

if __name__ == "__main__":
    end_to_end_url()