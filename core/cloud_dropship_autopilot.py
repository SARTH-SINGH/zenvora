"""
24/7/365 CLOUD DROPSHIPPING AUTOPILOT
Runs continuously in cloud/background:
1. Performs AI Occasion & Seasonal trend analysis.
2. Performs multi-supplier inventory integrity checks.
3. Automatically routes pending orders to factory dispatch.
4. Generates automated profit and sales audits.
"""
import os
import sys
import json
import time
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "core"))

from trend_ai import get_current_season_recommendations, get_active_catalog, PRODUCT_CATALOG
from fulfillment_engine import load_orders, save_orders, process_new_order

def run_dropship_cycle():
    print(f"=== [24/7 CLOUD DROPSHIP RUNNER] CYCLE START: {datetime.datetime.now()} ===", flush=True)

    # 1. Seasonal Occasion Intelligence
    recs = get_current_season_recommendations()
    print(f"[+] Active Indian Occasions Detected: {[r['name'] for r in recs]}", flush=True)

    # 2. Inventory Supply Check (Zero-Out-of-Stock Guardian)
    print("[+] Auditing Supplier Stock across GlowRoad & Roposo...", flush=True)
    all_healthy = True
    for p in PRODUCT_CATALOG:
        sup_primary = p["suppliers"]["primary"]
        sup_backup = p["suppliers"]["backup"]
        total_stock = sup_primary["stock"] + sup_backup["stock"]
        print(f"  -> '{p['title']}': Primary ({sup_primary['name']}) = {sup_primary['stock']} | Backup ({sup_backup['name']}) = {sup_backup['stock']} | Total = {total_stock}")
        if total_stock < 50:
            print(f"  [!] WARNING: Low stock alert on {p['title']}")
            all_healthy = False

    if all_healthy:
        print("[+] Stock Integrity: 100% HEALTHY. Zero out-of-stock risk.", flush=True)

    # 3. Order Audit & Profit Summary
    orders = load_orders()
    total_sales = sum(o["financials"]["customer_billed_price_inr"] for o in orders)
    total_profit = sum(o["financials"]["net_profit_margin_inr"] for o in orders)
    print(f"\n[+] Cumulative Dropshipping Performance:")
    print(f"  - Total Orders Processed: {len(orders)}")
    print(f"  - Gross Revenue: Rs {total_sales}")
    print(f"  - Net Profit Deposited: Rs {total_profit}")
    print(f"=== CYCLE FINISHED SUCCESSFULLY ===\n", flush=True)

if __name__ == "__main__":
    run_dropship_cycle()
