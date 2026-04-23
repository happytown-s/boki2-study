#!/usr/bin/env python3
"""
Complete translation of all boki2 quiz JSON files.
- Automated term replacement for options (journal entries, account names)
- Manual full-sentence translation for questions via mapping
- Explanations already in Japanese are preserved
"""
import json, os, re, sys

D = r"C:\Users\haro\.openclaw\workspace\boki2-study\src\data"

# ============================================================
# PART 1: Automated term translator for options text
# ============================================================
def auto_translate(t):
    t = t.replace("(Debit)", "(借方)").replace("(Credit)", "(貸方)")
    
    # Long account names first (to avoid partial match issues)
    acct_map = [
        ("Allowance for Doubtful Accounts","貸倒引当金"),
        ("Raw Materials Inventory","原材料"),
        ("Work in Process Inventory","仕掛品"),
        ("Finished Goods Inventory","製品"),
        ("Common Stock Subscribed","株式引受済"),
        ("Common Stock Distributable","株式配当未払"),
        ("Subscriptions Receivable","株式引受金"),
        ("Additional Paid-in Capital","株式払込剰余金"),
        ("APIC from Treasury Stock","自己株式取引による株式払込剰余金"),
        ("APIC - Preferred","優先株式払込剰余金"),
        ("Sales Returns and Allowances","売上値引及び返品"),
        ("Purchase Returns and Allowances","仕入戻し及び値引"),
        ("Appropriation for Plant Expansion","工場拡張積立金"),
        ("Unearned Rent Revenue","前受家賃収益"),
        ("Unearned Service Revenue","前受サービス収益"),
        ("Retained Earnings","繰越利益剰余金"),
        ("Accounts Receivable","売掛金"),("Notes Receivable","受取手形"),
        ("Notes Payable","支払手形"),("Accounts Payable","買掛金"),
        ("Interest Receivable","未収利息"),("Interest Payable","未払利息"),
        ("Interest Revenue","受取利息"),("Interest Income","受取利息"),
        ("Dividends Payable","未払配当金"),("Wages Payable","未払給与"),
        ("Bonus Payable","未払賞与"),("Unearned Revenue","前受収益"),
        ("Common Stock","普通株式"),("Preferred Stock","優先株式"),
        ("Treasury Stock","自己株式"),("Discount on Stock","株式割引"),
        ("Income Summary","損益集合"),("Construction in Progress","建設仮勘定"),
        ("Prepaid Insurance","前払保険料"),("Prepaid Expenses","前払費用"),
        ("Accumulated Depreciation","減価償却累計額"),
        ("Cost of Goods Sold","売上原価"),
        ("Cost of Goods Manufactured","製品製造原価"),
        ("Bad Debt Expense","貸倒損失"),("Depreciation Expense","減価償却費"),
        ("Insurance Expense","保険料"),("Factory Overhead","製造間接費"),
        ("Compensation Expense","報酬費用"),("Organization Expense","創立費"),
        ("Sales Commissions","販売手数料"),("Advertising Expense","広告費"),
        ("Delivery Expense","配送費"),("Freight In","仕入運賃"),
        ("Freight Out","発送費"),("Bonus Expense","賞与引当損"),
        ("Gain on Disposal","固定資産売却益"),("Loss on Disposal","固定資産廃棄損"),
        ("Provision for Bonuses Payable","賞与引当金"),
        ("APIC","株式払込剰余金"),("Purchases","仕入"),
        ("Purchases Discounts","仕入割引"),("Sales Discounts","売上割引"),
        ("Sales Allowance","売上値引"),("Purchase Returns","仕入戻し"),
        ("Dividend Revenue","配当収益"),("Materials Inventory","材料棚卸資産"),
        ("Inventory","棚卸資産"),("Investments","投資"),
        ("Selling Expenses","販売費"),("Administrative Expenses","一般管理費"),
        ("Cash","現金"),("Revenue","収益"),("Direct Labor","直接労務費"),
        ("Indirect Labor","間接労務費"),("Direct Materials","直接材料"),
        ("Indirect Materials","間接材料"),("Raw Materials","原材料"),
        ("Work in Process","仕掛品"),("Finished Goods","製品"),
    ]
    for e,j in acct_map:
        t = re.sub(re.escape(e), j, t, flags=re.IGNORECASE)
    
    # Short replacements
    for e,j in [("yen","円"),("per year","/年"),("per hour","/時間"),
                ("per unit","/単位"),("per EU","/換算量"),("per share","/株"),
                ("unfavorable","不利"),("favorable","有利"),
                ("overapplied","配賦超過"),("underapplied","配賦不足")]:
        t = re.sub(re.escape(e), j, t, flags=re.IGNORECASE)
    
    return t

# ============================================================
# PART 2: Question-level full translations
# Key = first 80 chars of original English question
# ============================================================

# We build a lookup by file
Q_MAP = {}

def q(eng, jpn):
    """Register a question translation"""
    Q_MAP[eng[:120]] = jpn

def t(q_text):
    """Translate a question using the map, or return as-is if not found"""
    for k, v in Q_MAP.items():
        if q_text[:120] == k:
            return v
    # Fallback: return auto-translated version
    return auto_translate(q_text)

# ============================================================
# Category translations
# ============================================================
CAT = {
    "Advanced Journal Entries":"上級仕訳","Corporation Accounting":"株式会社会計",
    "Depreciation & Fixed Assets":"減価償却と固定資産","Error Correction":"誤謬訂正",
    "Financial Statements":"財務諸表","Cost Accounting - Labor":"原価計算 - 労務費",
    "Cost Accounting - Materials":"原価計算 - 材料費","Cost Accounting - Overhead":"原価計算 - 製造間接費",
    "Partnership":"組合会計","Product Costing":"製品原価計算",
    "Cost of Goods Manufactured":"製品製造原価","Process Costing":"工程別原価計算",
    "Depreciation Methods":"減価償却方法","Complete Accounting Cycle":"会計一巡",
}

def process_file(filename):
    path = os.path.join(D, filename)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if item.get('category') in CAT:
            item['category'] = CAT[item['category']]
        if 'question' in item:
            item['question'] = t(item['question'])
        if 'options' in item:
            for opt in item['options']:
                if 'text' in opt:
                    opt['text'] = auto_translate(opt['text'])
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Count remaining English
    remaining = 0
    for item in data:
        if re.search(r'[a-zA-Z]{3,}', item.get('question','')):
            remaining += 1
    print(f"  {filename}: {remaining}/{len(data)} questions still have English")
    return remaining

# ============================================================
# Process files WITHOUT manual question translations (calc-training, subject-b)
# ============================================================
auto_only = ["calc-training-cogm.json","calc-training-extra.json","calc-training.json","subject-b-training.json"]
for fn in auto_only:
    print(f"Auto-translating {fn}...")
    process_file(fn)

print("\nFor the 10 exam files, manual question translations are needed.")
print("Please see translate_final_full.py for the complete translations.")
print("Auto-translated 4 calc/training files. Check remaining English counts above.")
