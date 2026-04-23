import stripe

stripe.api_key = "sk_test_xxx"

def create_checkout(tenant_id):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": "price_xxx",
            "quantity": 1
        }],
        success_url="https://app.com/success",
        cancel_url="https://app.com/cancel"
    )

    return session.url
