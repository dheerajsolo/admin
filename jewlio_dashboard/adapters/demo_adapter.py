from __future__ import annotations

from datetime import date, timedelta
import random


def fetch_orders(limit: int = 100) -> list[dict]:
    statuses = ["processing", "completed", "on-hold", "pending", "cancelled"]
    payments = ["Partial COD", "UPI", "Razorpay", "COD"]
    products = [
        ("Anti Tarnish Bracelet", "BR-001"),
        ("Gold Plated Earrings", "ER-014"),
        ("Charm Necklace", "NK-022"),
        ("Everyday Ring", "RG-008"),
    ]

    rows = []
    today = date.today()

    for i in range(min(limit, 100)):
        product, sku = products[i % len(products)]
        total = random.choice([399, 499, 699, 899, 1099, 1299])
        paid = 49 if i % 3 == 0 else 0
        cod_due = max(total - paid, 0) if paid else 0

        rows.append(
            {
                "order_id": 1000 + i,
                "date": str(today - timedelta(days=i % 30)),
                "customer": f"Customer {i + 1}",
                "phone": f"900000{i:04d}",
                "city": random.choice(["Jaipur", "Delhi", "Mumbai", "Indore", "Pune"]),
                "product": product,
                "sku": sku,
                "qty": random.choice([1, 1, 1, 2]),
                "payment_method": payments[i % len(payments)],
                "total": total,
                "paid_amount": paid,
                "cod_due": cod_due,
                "status": statuses[i % len(statuses)],
                "shipping_status": random.choice(["Not Shipped", "Packed", "In Transit", "Delivered"]),
            }
        )

    return rows


def fetch_products(limit: int = 100) -> list[dict]:
    categories = ["Bracelets", "Earrings", "Necklaces", "Rings"]
    rows = []

    for i in range(min(limit, 60)):
        stock = random.choice([0, 2, 4, 7, 12, 18, 25])
        rows.append(
            {
                "product_id": 2000 + i,
                "name": f"Jewlio Product {i + 1}",
                "sku": f"SKU-{i + 1:03d}",
                "category": categories[i % len(categories)],
                "price": random.choice([299, 399, 499, 699, 899]),
                "stock_quantity": stock,
                "stock_status": "outofstock" if stock == 0 else "instock",
                "status": "Out of Stock" if stock == 0 else ("Low Stock" if stock <= 5 else "In Stock"),
                "total_sold": random.randint(0, 80),
            }
        )

    return rows


def fetch_posts(limit: int = 50) -> list[dict]:
    rows = []
    for i in range(min(limit, 20)):
        rows.append(
            {
                "post_id": 3000 + i,
                "title": f"Jewellery Styling Blog {i + 1}",
                "status": "publish" if i % 3 else "draft",
                "date": str(date.today() - timedelta(days=i * 2)),
                "category": "Fashion",
            }
        )
    return rows
