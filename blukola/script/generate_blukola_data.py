"""Generate realistic raw CSVs for the KolaMart dbt case study.

Usage:  python scripts/generate_kolamart_data.py   (run from the project root)
Output: ./raw_data/{customers,products,orders,order_items,payments}.csv
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT = Path("raw_data")
OUT.mkdir(exist_ok=True)

N_CUSTOMERS = 300
N_ORDERS = 2000
ORDERS_START = datetime(2025, 7, 1)
END = datetime(2026, 10, 14, 23, 59, 59)  # last day of data; change if you re-run later
LOADED_AT = datetime.now().replace(microsecond=0)
FMT = "%Y-%m-%d %H:%M:%S"


def ts(dt):
    return dt.strftime(FMT)


def rand_between(start, end):
    return start + timedelta(seconds=random.random() * (end - start).total_seconds())


# ---------------------------------------------------------------- customers
FIRST = {
    "yoruba": ["Adebayo", "Tunde", "Ife", "Funke", "Bukola", "Kemi", "Seun", "Yetunde",
               "Folake", "Damilola", "Olumide", "Temitope", "Ayo", "Bisi", "Segun"],
    "igbo": ["Chidi", "Amaka", "Ngozi", "Emeka", "Chioma", "Ikenna", "Obinna", "Uche",
             "Nneka", "Kelechi", "Ifeanyi", "Adaeze"],
    "hausa": ["Zainab", "Musa", "Aisha", "Ibrahim", "Fatima", "Abubakar", "Hauwa", "Usman",
              "Maryam", "Sani", "Halima", "Yusuf"],
}
LAST = {
    "yoruba": ["Adeyemi", "Balogun", "Ogunleye", "Lawal", "Afolabi", "Akinola", "Oladipo", "Adebayo"],
    "igbo": ["Obi", "Eze", "Okafor", "Nwosu", "Okonkwo", "Chukwu", "Ogbonna", "Nnadi"],
    "hausa": ["Bello", "Musa", "Ibrahim", "Abdullahi", "Danjuma", "Yakubu", "Suleiman", "Umar"],
}
# city: (weight, {name group: weight})
CITIES = {
    "Lagos": (38, {"yoruba": 50, "igbo": 30, "hausa": 20}),
    "Abuja": (20, {"yoruba": 30, "igbo": 35, "hausa": 35}),
    "Port Harcourt": (11, {"yoruba": 15, "igbo": 70, "hausa": 15}),
    "Ibadan": (9, {"yoruba": 85, "igbo": 10, "hausa": 5}),
    "Kano": (8, {"yoruba": 5, "igbo": 5, "hausa": 90}),
    "Enugu": (7, {"yoruba": 5, "igbo": 90, "hausa": 5}),
    "Kaduna": (7, {"yoruba": 10, "igbo": 10, "hausa": 80}),
}


def make_customers():
    city_names = list(CITIES)
    city_weights = [CITIES[c][0] for c in city_names]
    signups = sorted(rand_between(datetime(2025, 1, 1), datetime(2026, 9, 30))
                     for _ in range(N_CUSTOMERS))
    rows, used = [], set()
    for i, created in enumerate(signups):
        city = random.choices(city_names, city_weights)[0]
        groups = CITIES[city][1]
        g = random.choices(list(groups), list(groups.values()))[0]
        first, last = random.choice(FIRST[g]), random.choice(LAST[g])
        domain = random.choices(["gmail.com", "yahoo.com", "outlook.com"], [65, 25, 10])[0]
        email = f"{first}.{last}@{domain}".lower()
        while email in used:
            email = f"{first}.{last}{random.randint(1, 99)}@{domain}".lower()
        used.add(email)

        # a little mess, like real raw data (staging models clean this up)
        name = f"{first} {last}"
        r = random.random()
        if r < 0.08:
            name = name.lower()
        elif r < 0.12:
            name = name.upper()
        elif r < 0.17:
            name = name + " "
        if random.random() < 0.06:
            email = email.capitalize()
        r = random.random()
        shown_city = city.lower() if r < 0.05 else (city + " " if r < 0.08 else city)

        rows.append({
            "customer_id": 1001 + i,
            "full_name": name,
            "email": email,
            "city": shown_city,
            "created_at": ts(created.replace(microsecond=0)),
        })
    return rows, signups


# ----------------------------------------------------------------- products
PRODUCTS = [
    ("Ankara Shirt", "Fashion", 15000), ("Senator Wear Set", "Fashion", 45000),
    ("Ankara Gown", "Fashion", 28000), ("Sneakers", "Fashion", 32000),
    ("Leather Sandals", "Fashion", 12000), ("Agbada Set", "Fashion", 85000),
    ("Denim Jeans", "Fashion", 18000), ("Polo T-Shirt", "Fashion", 8500),
    ("Handbag", "Fashion", 22000), ("Wrist Watch", "Fashion", 35000),
    ("Wireless Earbuds", "Electronics", 25000), ("Phone Case", "Electronics", 3500),
    ("Power Bank 20000mAh", "Electronics", 18000), ("Bluetooth Speaker", "Electronics", 28000),
    ("32-inch Smart TV", "Electronics", 165000), ("Laptop Backpack", "Electronics", 14000),
    ("USB-C Charger", "Electronics", 6500), ("Ring Light", "Electronics", 12500),
    ("Smartwatch", "Electronics", 42000), ("Rechargeable Fan", "Electronics", 24000),
    ("Rice 50kg", "Groceries", 70000), ("Vegetable Oil 5L", "Groceries", 14500),
    ("Noodles Carton", "Groceries", 8500), ("Garri 10kg", "Groceries", 9500),
    ("Honey Beans 5kg", "Groceries", 8200), ("Tomato Paste Carton", "Groceries", 18500),
    ("Spaghetti Carton", "Groceries", 15500), ("Chocolate Drink 900g", "Groceries", 6800),
    ("Powdered Milk 900g", "Groceries", 9500),
    ("Non-stick Pot Set", "Home", 38000), ("Bedsheet Set", "Home", 17500),
    ("Standing Fan", "Home", 45000), ("Blender", "Home", 26000), ("Electric Kettle", "Home", 12000),
    ("Shea Butter 500g", "Beauty", 4500), ("Hair Oil", "Beauty", 3800),
    ("Perfume", "Beauty", 18000), ("Body Lotion", "Beauty", 6500), ("Face Wash", "Beauty", 5200),
]
CATEGORY_WEIGHT = {"Groceries": 30, "Fashion": 25, "Electronics": 20, "Home": 12, "Beauty": 13}


def price_at(base, when):
    """Prices drift up about 1.2% a month, rounded to the nearest 50 naira."""
    months = max((when - ORDERS_START).days, 0) / 30
    return int(round(base * (1 + 0.012 * months) / 50) * 50)


def make_products():
    return [{"product_id": 1 + i, "product_name": n, "category": c,
             "base": b, "unit_price": price_at(b, END)}
            for i, (n, c, b) in enumerate(PRODUCTS)]


# ------------------------------------------------------------------- orders
HOUR_WEIGHTS = [1, 1, 1, 1, 1, 1, 2, 3, 5, 7, 8, 8, 8, 8, 8, 8, 9, 10, 11, 12, 11, 8, 5, 3]
STATUSES = ["placed", "shipped", "delivered", "cancelled"]


def pick_status(age_days):
    if age_days < 2:
        w = [50, 35, 5, 10]
    elif age_days < 7:
        w = [5, 30, 55, 10]
    else:
        w = [1, 2, 89, 8]
    return random.choices(STATUSES, w)[0]


def make_orders(customers, signups):
    # some customers order far more often than others
    weights = [min(random.paretovariate(1.4), 20) for _ in customers]
    raw = []
    for _ in range(N_ORDERS):
        idx = random.choices(range(len(customers)), weights)[0]
        start = max(signups[idx], ORDERS_START)
        when = rand_between(start, END).replace(
            hour=random.choices(range(24), HOUR_WEIGHTS)[0],
            minute=random.randint(0, 59), second=random.randint(0, 59), microsecond=0)
        if when < signups[idx]:
            when = signups[idx] + timedelta(minutes=random.randint(5, 120))
        when = min(when, END)
        raw.append({"customer_id": customers[idx]["customer_id"], "ordered_at": when,
                    "order_status": pick_status((END - when).days)})
    raw.sort(key=lambda o: o["ordered_at"])
    for i, o in enumerate(raw):
        o["order_id"] = 10001 + i
    return raw


# ------------------------------------------------- order items and payments
def make_items_and_payments(orders, products):
    prod_weights = [CATEGORY_WEIGHT[p["category"]] for p in products]
    items, payments = [], []
    pay_id = [1]

    def add_payment(order_id, method, amount, status, when):
        payments.append({"payment_id": pay_id[0], "order_id": order_id,
                         "payment_method": method, "amount": amount,
                         "status": status, "paid_at": ts(min(when, END))})
        pay_id[0] += 1

    def method():
        return random.choices(["card", "transfer", "wallet", "ussd"], [45, 35, 15, 5])[0]

    item_id = 1
    for o in orders:
        k = random.choices([1, 2, 3, 4, 5], [45, 30, 15, 7, 3])[0]
        chosen = []
        while len(chosen) < k:
            p = random.choices(products, prod_weights)[0]
            if p not in chosen:
                chosen.append(p)
        total = 0
        for p in chosen:
            qty = 1 if p["base"] >= 100000 else random.choices([1, 2, 3], [70, 22, 8])[0]
            price = price_at(p["base"], o["ordered_at"])
            total += qty * price
            items.append({"order_item_id": item_id, "order_id": o["order_id"],
                          "product_id": p["product_id"], "quantity": qty, "unit_price": price})
            item_id += 1
        o["order_amount"] = total

        status, t = o["order_status"], o["ordered_at"] + timedelta(minutes=random.randint(1, 10))
        if status in ("shipped", "delivered"):
            if random.random() < 0.12:  # a failed attempt before the successful one
                add_payment(o["order_id"], random.choice(["card", "ussd"]), total, "failed", t)
                t += timedelta(minutes=random.randint(1, 10))
            if random.random() < 0.10:  # split payment, e.g. wallet plus card
                first = int(round(total * random.uniform(0.3, 0.6) / 50) * 50)
                first = min(max(first, 50), total - 50)
                add_payment(o["order_id"], "wallet", first, "success", t)
                add_payment(o["order_id"], random.choice(["card", "transfer"]), total - first,
                            "success", t + timedelta(minutes=random.randint(1, 10)))
            else:
                add_payment(o["order_id"], method(), total, "success", t)
        elif status == "cancelled":
            r = random.random()
            if r < 0.35:
                add_payment(o["order_id"], method(), total, "failed", t)
            elif r < 0.60:  # paid, then cancelled (refund pending)
                add_payment(o["order_id"], method(), total, "success", t)
        elif random.random() < 0.40:  # placed
            add_payment(o["order_id"], method(), total, "failed", t)
    return items, payments


# ------------------------------------------------------------------- output
def write_csv(name, fields, rows):
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"{name}.csv: {len(rows)} rows")


def main():
    customers, signups = make_customers()
    products = make_products()
    orders = make_orders(customers, signups)
    items, payments = make_items_and_payments(orders, products)

    order_rows = [{**o, "ordered_at": ts(o["ordered_at"]), "_loaded_at": ts(LOADED_AT)}
                  for o in orders]

    write_csv("customers", ["customer_id", "full_name", "email", "city", "created_at"], customers)
    write_csv("products", ["product_id", "product_name", "category", "unit_price"], products)
    write_csv("orders", ["order_id", "customer_id", "order_status", "ordered_at", "_loaded_at"],
              order_rows)
    write_csv("order_items", ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
              items)
    write_csv("payments", ["payment_id", "order_id", "payment_method", "amount", "status", "paid_at"],
              payments)

    # sanity checks
    paid = {}
    for p in payments:
        if p["status"] == "success":
            paid[p["order_id"]] = paid.get(p["order_id"], 0) + p["amount"]
    assert all(paid.get(o["order_id"], 0) <= o["order_amount"] for o in orders), "overpaid order"
    by_status = {}
    for o in orders:
        by_status[o["order_status"]] = by_status.get(o["order_status"], 0) + 1
    revenue = sum(paid.get(o["order_id"], 0) for o in orders if o["order_status"] == "delivered")
    print("orders by status:", by_status)
    print(f"revenue (paid, delivered): NGN {revenue:,}")


if __name__ == "__main__":
    main()
