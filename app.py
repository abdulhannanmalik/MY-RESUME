# Python Flask Backend for Malik Ab Hannan's Online Dukaan
# Yeh aik bunyadi backend hai jo products data aur simple in-memory cart manage karta hai.
# Yeh aik mukammal e-commerce backend NAHI hai. Asli project mein database, user auth, etc. shamil honge.

from flask import Flask, jsonify, request
from flask_cors import CORS # CORS allow karta hai ke frontend is backend se data fetch kar sake

app = Flask(__name__)
CORS(app) # CORS enable karein

# Sample product data (Asal mein yeh data database se aata hai)
# Yeh hamara database simulation hai memory mein
products_db = [
    {"id": 1, "name": "Stylish Cotton Shirt", "price": 1200, "description": "Comfortable aur trendy shirt har mauqe ke liye.", "image_url": "https://placehold.co/400x300/4CAF50/ffffff?text=Stylish+Shirt"},
    {"id": 2, "name": "High-Quality Headphones", "price": 3500, "description": "Behtareen sound quality aur comfortable fit.", "image_url": "https://placehold.co/400x300/2196F3/ffffff?text=Modern+Headphones"},
    {"id": 3, "name": "Advanced Smartwatch", "price": 8000, "description": "Apni fitness aur notifications ko track karein.", "image_url": "https://placehold.co/400x300/FF9800/ffffff?text=Smartwatch"},
    {"id": 4, "name": "Genuine Leather Wallet", "price": 2500, "description": "Stylish aur durable wallet aapke card aur cash ke liye.", "image_url": "https://placehold.co/400x300/9C27B0/ffffff?text=Leather+Wallet"},
    {"id": 5, "name": "Comfortable Running Shoes", "price": 4500, "description": "Apni running aur workouts ke liye perfect shoes.", "image_url": "https://placehold.co/400x300/E91E63/ffffff?text=Trendy+Shoes"},
    {"id": 6, "name": "Spacious Backpack", "price": 3000, "description": "Apne saman ko aasani se carry karein.", "image_url": "https://placehold.co/400x300/00BCD4/ffffff?text=Backpack"}
]

# Simple in-memory cart (Yeh asal mein database ya session mein hona chahiye)
# Key product_id hai aur value quantity hai
cart = {}

# API endpoint jo saare products return karega
@app.route('/api/products', methods=['GET'])
def get_products():
    # Products list ko JSON format mein return karein
    print("Frontend ne products request kiye hain.") # Server console mein message
    return jsonify(products_db)

# API endpoint jo aik product ID ke zariye return karega (agar zaroorat ho)
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # products_db mein product ID search karein
    product = next((p for p in products_db if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    # Agar product na mile toh 404 Not Found error return karein
    return jsonify({"message": "Product nahi mila"}), 404

# API endpoint cart mein item add karne ke liye
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Check karein ke product database mein maujood hai ya nahi
    product = next((p for p in products_db if p['id'] == product_id), None)
    if not product:
        return jsonify({"message": "Invalid Product ID"}), 400 # Bad Request

    # Product ko in-memory cart mein add ya update karein
    if product_id in cart:
        cart[product_id] += 1 # Quantity badha dein
    else:
        cart[product_id] = 1 # Naya item add karein

    print(f"Product ID {product_id} cart mein add kiya gaya. Current cart: {cart}") # Server console mein message
    # Success message aur updated cart return karein (ya sirf count)
    return jsonify({"message": "Product cart mein shamil ho gaya", "cart": cart, "count": sum(cart.values())}), 200 # OK

# API endpoint cart se item remove karne ke liye (Optional, agar zaroorat ho)
# @app.route('/api/cart/remove/<int:product_id>', methods=['POST'])
# def remove_from_cart(product_id):
#     if product_id in cart:
#         cart[product_id] -= 1
#         if cart[product_id] <= 0:
#             del cart[product_id] # Agar quantity 0 ya negative ho toh item hata dein
#         print(f"Product ID {product_id} cart se remove kiya gaya. Current cart: {cart}")
#         return jsonify({"message": "Product cart se remove ho gaya", "cart": cart, "count": sum(cart.values())}), 200
#     return jsonify({"message": "Product cart mein maujood nahi hai"}), 400

# API endpoint poora cart dekhne ke liye (Optional, agar zaroorat ho)
@app.route('/api/cart', methods=['GET'])
def view_cart():
    # Cart ki current state return karein
    # Asal mein yahan aap cart items ki poori tafseel (naam, qeemat) bhi return kar sakte hain
    print(f"Frontend ne cart details request kiye hain. Current cart: {cart}")
    # Simple cart details: product ID aur quantity
    cart_details = [{"product_id": pid, "quantity": qty} for pid, qty in cart.items()]
    return jsonify({"cart_items": cart_details, "count": sum(cart.values())})

# API endpoint sirf cart mein items ka count return karne ke liye
@app.route('/api/cart/count', methods=['GET'])
def get_cart_count():
    count = sum(cart.values()) # Cart mein maujood items ki total tadaad
    print(f"Frontend ne cart count request kiya hai. Count: {count}")
    return jsonify({"count": count})


# Agar yeh script direct run ho rahi hai
if __name__ == '__main__':
    # Flask development server ko chalaein
    # debug=True se changes automatically load ho jayenge aur errors nazar aayenge
    # host='0.0.0.0' se server local network par bhi available ho sakta hai (caution: development only)
    # port=5000 default hai, agar change karna ho toh yahan karein
    app.run(debug=True, port=5000)
