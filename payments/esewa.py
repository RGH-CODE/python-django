import hmac
import hashlib
import base64
import uuid

from django.conf import settings


def generate_signature(message, secret):

    secret = secret.encode("utf-8")
    message = message.encode("utf-8")

    hmac_sha256 = hmac.new(
        secret,
        message,
        hashlib.sha256
    )

    digest = hmac_sha256.digest()

    signature = base64.b64encode(
        digest
    ).decode()

    return signature


def generate_esewa_payload(order):

    # ✅ REAL ORDER TOTAL
    total_amount = str(order.cached_total_price)

    # ✅ UNIQUE TRANSACTION ID
    transaction_uuid = (
        f"ORDER-{order.id}-{uuid.uuid4().hex[:8]}"
    )

    # ✅ SAVE IN DATABASE
    order.transaction_id = transaction_uuid
    order.save(update_fields=["transaction_id"])

    # ✅ MESSAGE FOR SIGNATURE
    message = (
        f"total_amount={total_amount},"
        f"transaction_uuid={transaction_uuid},"
        f"product_code={settings.ESEWA_MERCHANT_ID}"
    )

    # ✅ CREATE SIGNATURE
    signature = generate_signature(
        message,
        settings.ESEWA_SECRET_KEY
    )

    return {
        "amount": total_amount,
        "tax_amount": "0",
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": settings.ESEWA_MERCHANT_ID,
        "product_service_charge": "0",
        "product_delivery_charge": "0",        
        "signed_field_names":
            "total_amount,transaction_uuid,product_code",

        "signature": signature,
        
    "success_url": f"{settings.FRONTEND_URL}/payment/success",
    "failure_url": f"{settings.FRONTEND_URL}/payment/failure",   
    }