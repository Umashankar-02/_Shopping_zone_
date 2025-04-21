from fastapi import FastAPI, Query

# 🧠 Step 1: Create the FastAPI app
app = FastAPI()

# 🛍️ Step 2: Product Dataset (20+ items)
products = {
    "fashion": [
        {"name": "Trendy Jacket", "brand": "Zara", "price": "₹1999", "rating": 4.5},
        {"name": "Classic Jeans", "brand": "Levi’s", "price": "₹1499", "rating": 4.2},
        {"name": "Summer Dress", "brand": "H&M", "price": "₹1799", "rating": 4.4},
        {"name": "Sneakers", "brand": "Nike", "price": "₹2999", "rating": 4.6},
        {"name": "Hoodie", "brand": "Puma", "price": "₹1899", "rating": 4.3},
        {"name": "Leather Belt", "brand": "Allen Solly", "price": "₹799", "rating": 4.1},
        {"name": "Floral Top", "brand": "ONLY", "price": "₹1099", "rating": 4.3}
    ],
    "electronics": [
        {"name": "Bluetooth Speaker", "brand": "JBL", "price": "₹2999", "rating": 4.7},
        {"name": "Smartphone", "brand": "Samsung", "price": "₹20999", "rating": 4.3},
        {"name": "Smartwatch", "brand": "boAt", "price": "₹1999", "rating": 4.5},
        {"name": "Earbuds", "brand": "Realme", "price": "₹999", "rating": 4.4},
        {"name": "Tablet", "brand": "Lenovo", "price": "₹12999", "rating": 4.2},
        {"name": "Power Bank", "brand": "MI", "price": "₹999", "rating": 4.1},
        {"name": "Wireless Mouse", "brand": "Logitech", "price": "₹499", "rating": 4.5}
    ],
    "beauty": [
        {"name": "Matte Lipstick", "brand": "Lakmé", "price": "₹499", "rating": 4.6},
        {"name": "Face Wash", "brand": "Himalaya", "price": "₹199", "rating": 4.2},
        {"name": "Sunscreen SPF 50", "brand": "Neutrogena", "price": "₹549", "rating": 4.7},
        {"name": "Kajal", "brand": "Maybelline", "price": "₹249", "rating": 4.4},
        {"name": "BB Cream", "brand": "Pond’s", "price": "₹299", "rating": 4.3},
        {"name": "Compact Powder", "brand": "Lakmé", "price": "₹299", "rating": 4.1}
    ]
}

# 🧠 Step 3: Keyword Map
keywords = {
    "fashion": ["fashion", "clothes", "dress", "wear", "outfit", "style", "jacket", "jeans", "sneaker", "hoodie", "top"],
    "electronics": ["electronics", "gadgets", "tech", "device", "mobile", "phone", "speaker", "earbuds", "mouse"],
    "beauty": ["beauty", "makeup", "skincare", "lipstick", "cream", "sunscreen", "face wash", "kajal", "compact"],
    "shipping": ["shipping", "delivery", "free shipping"],
    "return": ["return", "refund", "replacement", "exchange"],
    "top": ["top", "best", "highest", "popular", "top rated"],
    "cheap": ["cheap", "budget", "lowest", "low price", "affordable"],
    "category": ["category", "categories", "sections", "what do you have"],
    "details": ["details", "all products", "show products", "product info", "information"]
}

# 🔍 Step 4: Category Matcher
def match_category(question):
    for key, words in keywords.items():
        for word in words:
            if word in question:
                return key
    return None

# 🤖 Step 5: Chatbot Endpoint
@app.get("/chatbot")
def chatbot(q: str = Query(..., alias="question")):
    question = q.lower()
    cat = match_category(question)

    if cat == "fashion":
        items = [f"{p['name']} by {p['brand']} ({p['price']})" for p in products["fashion"]]
        return {"response": "👗 Fashion Picks:\n" + "\n".join(items)}

    elif cat == "electronics":
        items = [f"{p['name']} by {p['brand']} ({p['price']})" for p in products["electronics"]]
        return {"response": "🔌 Electronic Products:\n" + "\n".join(items)}

    elif cat == "beauty":
        items = [f"{p['name']} by {p['brand']} ({p['price']})" for p in products["beauty"]]
        return {"response": "💄 Beauty Essentials:\n" + "\n".join(items)}

    elif cat == "shipping":
        return {"response": "🚚 Free 2-day shipping on orders above ₹999."}

    elif cat == "return":
        return {"response": "🔁 7-day return policy. Full refund on eligible items."}

    elif cat == "top":
        all_items = [item for cat in products.values() for item in cat]
        top_product = max(all_items, key=lambda p: p["rating"])
        return {"response": f"🏆 Top Rated: {top_product['name']} by {top_product['brand']} ({top_product['rating']}★)"}

    elif cat == "cheap":
        all_items = [item for cat in products.values() for item in cat]
        cheap_product = min(all_items, key=lambda p: int(p["price"].replace("₹", "")))
        return {"response": f"💸 Cheapest: {cheap_product['name']} at {cheap_product['price']}"}

    elif cat == "category":
        return {"response": "🛍️ We offer: Fashion, Electronics, Beauty"}

    elif cat == "details":
        details = []
        for category, items in products.items():
            for p in items:
                details.append(f"{p['name']} ({category.title()}): {p['price']} – {p['rating']}★")
        return {"response": "📋 Product Details:\n" + "\n".join(details)}

    else:
        return {
            "response": (
                "🤖 I didn't get that. Try asking:\n"
                "- Show fashion items\n"
                "- Top rated product?\n"
                "- Budget gadgets?\n"
                "- Do you offer return?\n"
                "- List all products"
            )
        }
