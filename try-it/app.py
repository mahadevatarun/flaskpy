from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

products = [
    {"id": 1, "name": "Book",
     "sizes": {"Small": 150, "Medium": 250, "Large": 400}},
    {"id": 2, "name": "Pen",
     "sizes": {"Fine": 10, "Medium": 12, "Bold": 15}},
    {"id": 3, "name": "Paper",
     "sizes": {"A5": 3, "A4": 5, "A3": 9}},
]


@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id", type=int)
    size = request.form.get("size")

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product and size in product["sizes"]:
        cart = session.get("cart", {})
        key = f"{product_id}_{size}"

        if key in cart:
            cart[key]["quantity"] += 1
        else:
            cart[key] = {
                "product_id": product_id,
                "name": product["name"],
                "size": size,
                "price": product["sizes"][size],
                "quantity": 1
            }

        session["cart"] = cart

    return redirect(url_for("home"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    total = sum(
        item["price"] * item["quantity"]
        for item in cart.values()
    )
    return render_template("cart.html", cart=cart, total=total)


@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    key = request.form.get("key")
    cart = session.get("cart", {})
    cart.pop(key, None)
    session["cart"] = cart

    return redirect(url_for("view_cart"))


@app.route("/clear-cart", methods=["POST"])
def clear_cart():
    session["cart"] = {}
    return redirect(url_for("view_cart"))
 
@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5005)
