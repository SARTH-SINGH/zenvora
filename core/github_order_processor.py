# -*- coding: utf-8 -*-
"""
GITHUB ORDER PROCESSOR FOR ZENVORA 24/7 CLOUD AUTOPILOT
Scans for incoming orders in repository issues, processes fulfillment via
domestic wholesale suppliers, assigns Delhivery tracking AWBs, and logs profits.
"""

import os
import sys
import json
import urllib.request
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "core"))

from fulfillment_engine import process_new_order, load_orders, save_orders

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "SARTH-SINGH/zenvora")

def get_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Zenvora-Order-Bot"
    }

def fetch_pending_orders():
    url = f"https://api.github.com/repos/{REPO}/issues?state=open&labels=order-pending"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"[!] Error fetching issues: {e}")
        return []

def process_pending_orders():
    print(f"=== [ZENVORA 24/7 AUTOPILOT] ORDER AUDIT START ===")
    issues = fetch_pending_orders()
    print(f"[+] Found {len(issues)} pending order(s) to fulfill.")

    for issue in issues:
        issue_num = issue["number"]
        body = issue.get("body", "")
        print(f"\nProcessing Issue #{issue_num}: {issue['title']}")

        # Extract JSON payload from codeblock in issue body
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", body, re.DOTALL)
        if not json_match:
            print(f"  [!] No valid JSON found in issue #{issue_num}")
            continue

        try:
            order_data = json.loads(json_match.group(1))
        except Exception as e:
            print(f"  [!] Failed to parse JSON: {e}")
            continue

        # Execute automated zero-inventory fulfillment
        res = process_new_order(order_data)

        if res.get("status") == "success":
            awb = res.get("courier_awb", "DLHV-PENDING")
            profit = res.get("financials", {}).get("net_profit_margin_inr", 0)
            supplier = res.get("items_fulfilled", [{}])[0].get("supplier_assigned", "Domestic Surat Hub")

            comment_body = (
                f"### ✅ ORDER AUTOMATICALLY FULFILLED!\n"
                f"- **Order ID**: `{res.get('order_id')}`\n"
                f"- **Assigned Supplier**: {supplier}\n"
                f"- **Delhivery Tracking AWB**: `{awb}`\n"
                f"- **Estimated Delivery**: 2-3 Business Days\n"
                f"- **Net Profit Deposited**: `+₹{profit}`\n\n"
                f"Package dispatched to courier with Zenvora white-label packaging. Customer COD collection active."
            )

            # 1. Post comment on issue
            comment_url = f"https://api.github.com/repos/{REPO}/issues/{issue_num}/comments"
            req_c = urllib.request.Request(comment_url, data=json.dumps({"body": comment_body}).encode(), headers=get_headers(), method="POST")
            try:
                urllib.request.urlopen(req_c)
            except Exception as e:
                print(f"  [!] Failed to post comment: {e}")

            # 2. Close issue and mark fulfilled
            patch_url = f"https://api.github.com/repos/{REPO}/issues/{issue_num}"
            patch_data = {
                "state": "closed",
                "labels": ["order-fulfilled", "delhivery-active"]
            }
            req_p = urllib.request.Request(patch_url, data=json.dumps(patch_data).encode(), headers=get_headers(), method="PATCH")
            try:
                urllib.request.urlopen(req_p)
                print(f"  [+] Issue #{issue_num} closed and marked fulfilled! Profit: +Rs {profit}")
            except Exception as e:
                print(f"  [!] Failed to close issue: {e}")

    print(f"\n=== [ZENVORA 24/7 AUTOPILOT] AUDIT COMPLETE ===")

if __name__ == "__main__":
    process_pending_orders()
