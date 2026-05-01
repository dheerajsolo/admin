from __future__ import annotations

from datetime import datetime, timedelta
import random

CATEGORIES = ["Bracelets", "Earrings", "Necklaces", "Rings", "Anklets"]
PRODUCTS = [
    ("JWL-BR-101", "Anti Tarnish Clover Bracelet", "Bracelets", 18, 499),
    ("JWL-ER-204", "Golden Hoop Earrings", "Earrings", 8, 399),
    ("JWL-NK-330", "Heart Charm Necklace", "Necklaces", 3, 699),
    ("JWL-RG-119", "Adjustable Stack Ring", "Rings", 0, 299),
    ("JWL-AN-042", "Minimal Anklet", "Anklets", 12, 349),
    ("JWL-BR-118", "Pearl Charm Bracelet", "Bracelets", 5, 549),
    ("JWL-ER-221", "Daily Wear Studs", "Earrings", 26, 249),
    ("JWL-NK-344", "Butterfly Pendant", "Necklaces", 11, 599),
]
CITIES = ["Delhi", "Gurgaon", "Mumbai", "Jaipur", "Pune", "Lucknow", "Surat", "Bengaluru"]
NAMES = ["Aarohi", "Riya", "Nisha", "Kavya", "Priya", "Meera", "Tanya", "Ananya", "Simran", "Isha"]
ORDER_STATUSES = ["processing", "processing", "shipped", "delivered", "pending", "rto"]
PAYMENTS = ["Partial COD", "Prepaid UPI", "COD", "Partial COD", "Razorpay"]


def get_demo_orders(limit: int = 40) -> list[dict]:
    today = datetime.now()
    orders: list[dict] = []
    for index in range(limit):
        sku, product, category, stock, price = random.choice(PRODUCTS)
        qty = random.choice([1, 1, 1, 2])
        total = price * qty
        payment = random.choice(PAYMENTS)
        paid = 49 if payment == "Partial COD" else (total if payment in ["Prepaid UPI", "Razorpay"] else 0)
        cod = max(total - paid, 0)
        status = random.choice(ORDER_STATUSES)
        date = today - timedelta(days=random.randint(0, 12), hours=random.randint(0, 20))
        orders.append({
            "Order ID": f"#{1024 + index}",
            "Date": date.strftime("%d %b %Y"),
            "Customer": random.choice(NAMES),
            "Phone": f"9{random.randint(100000000, 999999999)}",
            "City": random.choice(CITIES),
            "Product": product,
            "SKU": sku,
            "Qty": qty,
            "Payment": payment,
            "Total": total,
            "Paid": paid,
            "COD Due": cod,
            "Order Status": status,
            "Shipping Status": "ready" if status == "processing" else status,
        })
    return orders


def get_demo_products() -> list[dict]:
    rows = []
    for sku, product, category, stock, price in PRODUCTS:
        if stock <= 0:
            status = "Out of Stock"
        elif stock <= 5:
            status = "Low Stock"
        else:
            status = "In Stock"
        rows.append({
            "SKU": sku,
            "Product": product,
            "Category": category,
            "Stock": stock,
            "Status": status,
            "Regular Price": price,
            "Sale Price": max(price - 50, 199),
            "Total Sold": random.randint(4, 95),
        })
    return rows


def get_demo_sales_series(days: int = 14) -> list[dict]:
    today = datetime.now().date()
    data = []
    for i in range(days - 1, -1, -1):
        date = today - timedelta(days=i)
        orders = random.randint(4, 26)
        revenue = orders * random.randint(350, 780)
        data.append({"Date": date.strftime("%d %b"), "Orders": orders, "Revenue": revenue})
    return data


def get_demo_shipments() -> list[dict]:
    orders = get_demo_orders(25)
    rows = []
    for item in orders:
        rows.append({
            "Order ID": item["Order ID"],
            "Customer": item["Customer"],
            "City": item["City"],
            "COD Due": item["COD Due"],
            "Courier": random.choice(["Delhivery", "Xpressbees", "Ecom Express", "Bluedart"]),
            "AWB": "" if item["Order Status"] == "processing" else f"AWB{random.randint(10000000, 99999999)}",
            "Status": item["Shipping Status"],
        })
    return rows
