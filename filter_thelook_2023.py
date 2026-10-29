"""
I wrote this script to filter TheLook eCommerce to 2023 only, for my Tableau dashboard.

Usage:
    python filter_thelook_2023.py
    python filter_thelook_2023.py --source ./thelook_original --output ./thelook_2023

What I do in this script (and what I do NOT do):
- I read ONLY orders.csv, order_items.csv, products.csv, users.csv
- I keep orders created in 2023, and only the items / products / users linked to those orders
- I drop PII from users (names, email, street address, postal code, lat/long) if those columns exist
- I NEVER overwrite the original files — I write new files to --output
- I print a summary, so I can see the filtered counts from my own file,
  not from a Kaggle preview, before I build in Tableau.

Requirements: pandas
    pip install pandas
"""
import argparse
from pathlib import Path
import sys

import pandas as pd


def pick(df, candidates, label):
    for c in candidates:
        if c in df.columns:
            return c
    print(f"ERROR: {label} — none of {candidates} found. Columns are: {list(df.columns)}")
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="./thelook_original",
                    help="Folder with the original unzipped Kaggle CSVs")
    ap.add_argument("--output", default="./thelook_2023",
                    help="Folder to write the filtered 2023 files to (will be created)")
    args = ap.parse_args()

    src = Path(args.source)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    report = []

    def log(msg):
        print(msg)
        report.append(msg)

    # --- Load ---
    log("=== TheLook 2023 filter — summary ===")
    orders = pd.read_csv(src / "orders.csv", low_memory=False)
    items = pd.read_csv(src / "order_items.csv", low_memory=False)
    products = pd.read_csv(src / "products.csv", low_memory=False)
    users = pd.read_csv(src / "users.csv", low_memory=False)

    log(f"Original orders.csv: {len(orders):,} rows, columns: {list(orders.columns)}")
    log(f"Original order_items.csv: {len(items):,} rows, columns: {list(items.columns)}")
    log(f"Original products.csv: {len(products):,} rows, columns: {list(products.columns)}")
    log(f"Original users.csv: {len(users):,} rows, columns: {list(users.columns)}")

    order_key = pick(orders, ["order_id", "id"], "orders order key")
    item_order_key = pick(items, ["order_id"], "order_items order key")
    item_product_key = pick(items, ["product_id"], "order_items product key")
    product_key = pick(products, ["id", "product_id"], "products key")
    user_key_orders = pick(orders, ["user_id"], "orders user key")
    user_key_users = pick(users, ["id", "user_id"], "users key")

    # --- Filter orders to 2023 by created_at ---
    orders["created_at"] = pd.to_datetime(orders["created_at"], errors="coerce")
    n_bad_dates = int(orders["created_at"].isna().sum())
    orders_2023 = orders[orders["created_at"].dt.year == 2023].copy()
    log(f"\nOrders with unparseable created_at (dropped from date filter): {n_bad_dates:,}")
    log(f"Orders in 2023: {len(orders_2023):,}  (dropped {len(orders) - len(orders_2023):,} non-2023 / bad-date orders)")
    if len(orders_2023):
        log(f"2023 orders date range: {orders_2023['created_at'].min()} to {orders_2023['created_at'].max()}")
    if "status" in orders_2023.columns:
        log(f"Orders status values in 2023:\n{orders_2023['status'].value_counts(dropna=False).to_string()}")
    log(f"Duplicate {order_key} in 2023 orders: {int(orders_2023.duplicated(subset=[order_key]).sum()):,}")

    # --- Keep only items for 2023 orders ---
    items_2023 = items[items[item_order_key].isin(set(orders_2023[order_key]))].copy()
    log(f"\nOrder items for 2023 orders: {len(items_2023):,}  (dropped {len(items) - len(items_2023):,} items for other years)")
    if "status" in items_2023.columns:
        log(f"Order items status values in 2023:\n{items_2023['status'].value_counts(dropna=False).to_string()}")
    if "sale_price" in items_2023.columns:
        log(f"Order items sale_price: min {items_2023['sale_price'].min()}, max {items_2023['sale_price'].max()}, "
            f"missing {int(items_2023['sale_price'].isna().sum()):,}")

    # --- Keep only products / users actually used in 2023 ---
    products_2023 = products[products[product_key].isin(set(items_2023[item_product_key]))].copy()
    users_2023 = users[users[user_key_users].isin(set(orders_2023[user_key_orders]))].copy()
    log(f"\nProducts used in 2023: {len(products_2023):,}  (dropped {len(products) - len(products_2023):,})")
    log(f"Users with a 2023 order: {len(users_2023):,}  (dropped {len(users) - len(users_2023):,})")

    # --- Drop PII from users ---
    pii = ["first_name", "last_name", "email", "street_address", "postal_code", "latitude", "longitude"]
    dropped_pii = [c for c in pii if c in users_2023.columns]
    users_2023 = users_2023.drop(columns=dropped_pii, errors="ignore")
    log(f"Dropped PII columns from users: {dropped_pii if dropped_pii else 'none found'}")
    log(f"Users columns kept: {list(users_2023.columns)}")

    # --- Save (originals untouched) ---
    orders_2023.to_csv(out / "orders_2023.csv", index=False)
    items_2023.to_csv(out / "order_items_2023.csv", index=False)
    products_2023.to_csv(out / "products_2023.csv", index=False)
    users_2023.to_csv(out / "users_2023.csv", index=False)
    log(f"\nSaved to {out.resolve()}:")
    log("  orders_2023.csv, order_items_2023.csv, products_2023.csv, users_2023.csv")

    (out / "summary_2023.txt").write_text("\n".join(report), encoding="utf-8")
    log("Also saved: summary_2023.txt in the same output folder.")
    log("\nNEXT: I use this summary before building in Tableau, so my KPI definitions")
    log("(especially Complete vs Cancelled/Returned) are set on my own file.")


if __name__ == "__main__":
    main()
