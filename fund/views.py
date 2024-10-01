from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RequestData
import json
from django.utils import timezone
from datetime import timedelta
from django.db import models  # Import models for Q objects
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Now you can access the environment variables like this:
INFURA_URL = os.getenv('INFURA_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Ensure the connection is successful
if not web3.is_connected():
    raise Exception("Unable to connect to the Ethereum network.")

@csrf_exempt
def fund(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ethereum_address = data.get('ethereum_address')
        
        # Extract IP address from the request
        ip_address = request.META.get('REMOTE_ADDR')

        # Get the current time
        current_time = timezone.now()

        # Check if a request from the same IP or Ethereum address was made in the last 1 minute
        one_minute_ago = current_time - timedelta(minutes=1)
        recent_requests = RequestData.objects.filter(
            created_at__gte=one_minute_ago
        ).filter(
            models.Q(ip_address=ip_address) | models.Q(ethereum_address=ethereum_address)
        )

        if recent_requests.exists():
            return JsonResponse({"error": "Request already received from this IP or Ethereum address within the last minute"}, status=400)

        # Transfer 0.0001 ETH to the provided Ethereum address
        try:
            # Build the transaction
            transaction = {
                'to': ethereum_address,
                'value': web3.to_wei(0.0001, 'ether'),  # 0.0001 ETH
                'gas': 2000000,
                'gasPrice': web3.to_wei('50', 'gwei'),  # Adjust gas price accordingly
                'nonce': web3.eth.get_transaction_count(SENDER_ADDRESS),
                'chainId': 11155111  # Sepolia chain ID
            }

            # Sign the transaction with the sender's private key
            signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

            # Send the transaction to the network
            txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

            # Wait for the transaction receipt
            txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

            # Save the new request to the database
            request_data = RequestData.objects.create(ip_address=ip_address, ethereum_address=ethereum_address)

            return JsonResponse({
                "message": "Data saved and 0.0001 ETH sent",
                "transaction_hash": txn_hash.hex(),
                "request_id": request_data.id
            })
        except Exception as e:
            return JsonResponse({"error": f"Failed to send ETH: {str(e)}"}, status=500)

    
    return JsonResponse({"error": "Invalid request method"}, status=400)

def transaction_stats(request):
    # Get the current time
    now = timezone.now()
    
    # Calculate 24 hours ago
    last_24_hours = now - timedelta(hours=24)

    # Filter transactions from the last 24 hours
    successful_transactions = RequestData.objects.filter(
        transaction_status='success',
        created_at__gte=last_24_hours
    ).count()

    failed_transactions = RequestData.objects.filter(
        transaction_status='failed',
        created_at__gte=last_24_hours
    ).count()

    return JsonResponse({
        "successful_transactions": successful_transactions,
        "failed_transactions": failed_transactions
    })