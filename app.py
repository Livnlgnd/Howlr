from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

stripe.api_key = 'sk_test_51RXw8ABQDR1hq55lMxLZYCHXOsNrPb7Ykitohn1gcCqNnLyPKLGFmz30Z8TY1bRjO3nusl1lrRCnqAIcakJ0HE5o00zWx6ZfsE'  # Replace with your Stripe secret key

# Simulated user coin database
user_db = {
    "demo_user": 500
}

# Stripe product price mapping
coin_prices = {
    "100_coins": {"amount": 100, "coins": 100, "price_id": "price_123"},      # Replace with your Stripe Price IDs
    "1000_coins": {"amount": 500, "coins": 1000, "price_id": "price_456"},
    "10000_coins": {"amount": 1500, "coins": 10000, "price_id": "price_789"}
}

@app.route("/user-coins/<username>", methods=["GET"])
def get_user_coins(username):
    coins = user_db.get(username, 0)
    return jsonify({"username": username, "coins": coins})

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.json
    username = data.get("username")
    package = data.get("package")

    if not username or package not in coin_prices:
        return jsonify({"error": "Invalid data"}), 400

    price_id = coin_prices[package]["price_id"]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price": price_id,
            "quantity": 1
        }],
        success_url=f"http://localhost:5000/success?username={username}&package={package}",
        cancel_url="http://localhost:5000/cancel"
    )
    return jsonify({"checkout_url": session.url})

@app.route("/success")
def success():
    username = request.args.get("username")
    package = request.args.get("package")
    if username and package in coin_prices:
        user_db[username] = user_db.get(username, 0) + coin_prices[package]["coins"]
        return f"<h2>Payment successful! {coin_prices[package]['coins']} coins added to {username}.</h2>"
    return "<h2>Something went wrong.</h2>"
