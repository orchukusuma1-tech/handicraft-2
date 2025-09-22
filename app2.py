from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "handicrafts-secret"

# -------------------------------
# Product Data
# -------------------------------
products = [
    {
        "id": 1,
        "name": "Handmade Bamboo Basket",
        "description": "A strong eco-friendly basket made with love by rural artisans.",
        "price": 299,
        "image": "https://5.imimg.com/data5/SELLER/Default/2024/10/462402160/XY/BE/IB/153079681/handicraft-basket-500x500.png",
        "owner": "Anitha Handicrafts",
        "manager": "Ravi Kumar"
    },
    {
        "id": 2,
        "name": "Terracotta Vase",
        "description": "Beautifully crafted terracotta vase, perfect for home decor.",
        "price": 599,
        "image": "https://5.imimg.com/data5/SELLER/Default/2023/4/300077453/GH/YS/YL/28816920/terracotta-flower-vase-1000x1000.jpg",
        "owner": "Sita Pottery Works",
        "manager": "Lakshmi Devi"
    }
]

# -------------------------------
# Seller Login Credentials
# -------------------------------
SELLER_USERNAME = "seller"
SELLER_PASSWORD = "1234"

# -------------------------------
# Base Template
# -------------------------------
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Handicrafts Store</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #fdf6f0; }
        header { background: #ff7f50; color: white; padding: 20px; text-align: center; }
        nav { background: #fff3f0; padding: 10px; text-align: center; }
        nav a { margin: 0 10px; padding: 10px 20px; background: #ff7f50; color: white; text-decoration: none; border-radius: 5px; }
        nav a:hover { background: #ff5722; }
        .container { max-width: 1000px; margin: auto; padding: 20px; }
        .product { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; background: white; display: flex; gap: 15px; }
        .product img { width: 150px; border-radius: 10px; }
        .cart-item { border-bottom: 1px solid #ddd; padding: 10px 0; }
        .cart-total { font-weight: bold; margin-top: 20px; }
        form input, form textarea { width: 100%; padding: 8px; margin: 5px 0; border: 1px solid #ccc; border-radius: 5px; }
        form button { background: #ff7f50; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; }
        form button:hover { background: #ff5722; }
    </style>
</head>
<body>
    <header>
        <h1>🛍️ Handicrafts Store</h1>
    </header>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('show_products') }}">Products</a>
        <a href="{{ url_for('show_cart') }}">Cart</a>
        <a href="{{ url_for('about') }}">About</a>
        <a href="{{ url_for('seller_login') }}">Seller</a>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def home():
    return render_template_string(base_html.replace("{% block content %}{% endblock %}", """
        <h2>Discover Authentic Handmade Products</h2>
        <p>Browse our collection of eco-friendly and traditional handicrafts.</p>
    """))

@app.route("/products")
def show_products():
    query = request.args.get("q", "").lower()
    if query:
        filtered = [p for p in products if query in p["name"].lower() or query in p["description"].lower()]
    else:
        filtered = products

    product_html = """
    <h2>Available Products</h2>
    <form method="get">
        <input type="text" name="q" placeholder="🔍 Search Products" value="{{ query }}">
        <button type="submit">Search</button>
    </form>
    """
    if filtered:
        for p in filtered:
            product_html += f"""
            <div class="product">
                <img src="{p['image']}" alt="{p['name']}">
                <div>
                    <h3>{p['name']}</h3>
                    <p>{p['description']}</p>
                    <p>💰 Price: ₹{p['price']}</p>
                    <p>Owner: {p['owner']} | Manager: {p['manager']}</p>
                    <a href="{url_for('add_to_cart', product_id=p['id'])}">Add to Cart 🛒</a>
                </div>
            </div>
            """
    else:
        product_html += "<p>No products found matching your search.</p>"

    return render_template_string(base_html.replace("{% block content %}{% endblock %}", product_html), query=query)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        session["cart"].append(product)
        session.modified = True
    return redirect(url_for("show_cart"))

@app.route("/cart")
def show_cart():
    cart = session.get("cart", [])
    total = sum(item["price"] for item in cart)
    cart_html = "<h2>🛒 Your Cart</h2>"
    if cart:
        for item in cart:
            cart_html += f"""
            <div class="cart-item">
                <strong>{item['name']}</strong> - ₹{item['price']}<br>
                {item['description']}<br>
                Owner: {item['owner']} | Manager: {item['manager']}
            </div>
            """
        cart_html += f"<div class='cart-total'>Total: ₹{total}</div>"
        cart_html += f"<a href='{url_for('checkout')}'>Proceed to Checkout ✅</a>"
    else:
        cart_html += "<p>Your cart is empty.</p>"
    return render_template_string(base_html.replace("{% block content %}{% endblock %}", cart_html))

@app.route("/checkout")
def checkout():
    session["cart"] = []
    session.modified = True
    checkout_html = """
    <h2>🛒 Your Cart</h2>
    <p>✅ Checkout complete! Thank you for supporting local artisans 🙏</p>
    """
    return render_template_string(base_html.replace("{% block content %}{% endblock %}", checkout_html))

@app.route("/about")
def about():
    return render_template_string(base_html.replace("{% block content %}{% endblock %}", """
        <h2>About Us</h2>
        <p>🌸 Our mission is to support rural artisans by bringing their handmade crafts online.<br>
        Every purchase directly helps local communities grow and sustain their traditions.</p>
    """))

# -------------------------------
# Seller Login & Dashboard
# -------------------------------
@app.route("/seller", methods=["GET", "POST"])
def seller_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == SELLER_USERNAME and password == SELLER_PASSWORD:
            session["seller"] = True
            return redirect(url_for("seller_dashboard"))
        else:
            error = "<p style='color:red;'>Invalid credentials</p>"
            return render_template_string(base_html.replace("{% block content %}{% endblock %}", error + login_form))
    return render_template_string(base_html.replace("{% block content %}{% endblock %}", login_form))

login_form = """
<h2>Seller Login</h2>
<form method="post">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>
"""

@app.route("/seller/dashboard", methods=["GET", "POST"])
def seller_dashboard():
    if not session.get("seller"):
        return redirect(url_for("seller_login"))

    message = ""
    if request.method == "POST":
        new_id = len(products) + 1
        name = request.form.get("name")
        description = request.form.get("description")
        price = int(request.form.get("price"))
        image = request.form.get("image")
        owner = request.form.get("owner")
        manager = request.form.get("manager")
        products.append({
            "id": new_id,
            "name": name,
            "description": description,
            "price": price,
            "image": image,
            "owner": owner,
            "manager": manager
        })
        message = "<p style='color:green;'>✅ Product added successfully!</p>"

    dashboard_html = f"""
    <h2>Seller Dashboard</h2>
    {message}
    <form method="post">
        <input type="text" name="name" placeholder="Product Name" required><br>
        <textarea name="description" placeholder="Product Description" required></textarea><br>
        <input type="number" name="price" placeholder="Price (₹)" required><br>
        <input type="text" name="image" placeholder="Image URL" required><br>
        <input type="text" name="owner" placeholder="Owner Name" required><br>
        <input type="text" name="manager" placeholder="Manager Name" required><br>
        <button type="submit">Add Product</button>
    </form>
    <p><a href='{url_for("show_products")}'>🔍 View Products</a></p>
    """
    return render_template_string(base_html.replace("{% block content %}{% endblock %}", dashboard_html))

@app.route("/seller/logout")
def seller_logout():
    session.pop("seller", None)
    return redirect(url_for("home"))

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
