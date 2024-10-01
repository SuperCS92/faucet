from django.db import models

# Create your models here.
class RequestData(models.Model):
    ip_address = models.GenericIPAddressField()  # To store IP addresses (IPv4 or IPv6)
    ethereum_address = models.CharField(max_length=42)  # Ethereum address length is 42 characters
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the entry is created
    transaction_status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failed', 'Failed')],default='failed')
    transaction_hash = models.CharField(max_length=66, blank=True, null=True)  # Stores the transaction hash for successful transactions
    error_message = models.TextField(blank=True, null=True)  # Stores the error message for failed transactions


    def __str__(self):
        return f"{self.ip_address} - {self.ethereum_address} - {self.transaction_status}"
