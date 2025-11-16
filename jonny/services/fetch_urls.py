import os
import requests
import json
import random
import time
from dotenv import load_dotenv
# Environment variables (replace with your actual values or os.environ.get)
load_dotenv()
app_key = os.getenv("APP_KEY")
partner_id = os.getenv("PARTNER_ID")
partner_secret = os.getenv("PARTNER_SECRET")
base_url = os.getenv("FINANCE_BASE_URL")
# Step 1: Get App Token
token_url = f"{base_url}/aggregation/v2/partners/authentication"  # replace with your token endpoint

def find_customer(customer_id: int):
    """
    Calls Finicity to retrieve accounts for a customer.
    If API fails, load fallback account list from ./users.json.
    """
    url = f"{base_url}/aggregation/v1/customers/{customer_id}/accounts"
    app_token = get_id_token(customer_id)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Finicity-App-Token": app_token,
        "Finicity-App-Key": app_key,
    }

    try:
        resp = requests.post(url, headers=headers, json={})
        resp.raise_for_status()  # forces fallback on any API error
        return resp.json()

    except Exception as e:
        print("⚠️ API failed, using fallback users.json:", e)
        with open("./sampledata/users.json", mode="r") as f:
            data = json.load(f)

        # Ensure we return the same structure the real API would return
        return data





def refresh_customer(id):
    url = f"{base_url}/aggregation/v1/customers/{id}/accounts"
    # url ="https://api.finicity.com/aggregation/v1/customers/1005061234/accounts"
    app_token = get_id_token(id)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Finicity-App-Token": app_token,
        "Finicity-App-Key": app_key,
    }

    data = {}  
    try:
        response = requests.post(url, headers=headers, json=data)
        raise
        return response

    except Exception:
        data =''
        with open('./sampledata/message.json', mode='r') as f:
            data = json.load(f)
        for line in data.get("transactions", []):
            print(line.get("categorization").get('category')) 
        return data

def get_id_token(id:int):
    token_payload = {
        "partnerId": partner_id,
        "partnerSecret": partner_secret,
    }

    token_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Finicity-App-Key": app_key
    }

    response = requests.post(token_url, headers=token_headers, json=token_payload)
    response.raise_for_status()  # Raise exception on HTTP error
    token = response.json().get("token")
    return token

def get_customer_id(id, app_token):
    print("App Token:", app_token)

    # Step 2: Create customer
    customer_url = f"{base_url}/aggregation/v2/customers/testing"
    name = f"customerusername{id}"
    customer_payload = {
        "username": name
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
    return customer_id

def get_customer_transactions(customer_id: int, from_date: int = None, to_date: int = None, limit: int = 25):


    app_token = get_id_token(customer_id)

    # Default: last 90 days
    if not to_date:
        to_date = int(time.time())
    if not from_date:
        from_date = to_date - (90 * 24 * 60 * 60)  # 90 days ago

    url = f"{base_url}/aggregation/v3/customers/{customer_id}/transactions"
    params = {
        "fromDate": from_date,
        "toDate": to_date,
        "includePending": "true",
        "sort": "desc",
        "limit": limit
    }

    headers = {
        "Finicity-App-Key": app_key,
        "Finicity-App-Token": app_token,
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("transactions", [])

    except Exception as e:
        print("⚠️ API failed, using fallback message.json:", e)
        with open("./sampledata/message.json", "r") as f:
            data = json.load(f)
        return data.get("transactions", [])


def generate_link(customer_id, app_token):

    connect_url = f"{base_url}/connect/v2/generate"
    connect_payload = {
        "partnerId": partner_id,
        "customerId": customer_id,
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
def end_to_end_url(id:int):
    app_token = get_id_token(id)
    customer_id = get_customer_id(id, app_token)
    link = generate_link(customer_id, app_token)
    return app_token, customer_id, link

if __name__ == "__main__":
    end_to_end_url()