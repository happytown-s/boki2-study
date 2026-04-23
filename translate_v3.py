#!/usr/bin/env python3
"""
Improved translation: First do automated term replacement, then fix remaining English 
in questions with full-sentence translations via pattern matching.
"""
import json
import os
import re

DATA_DIR = r"C:\Users\haro\.openclaw\workspace\boki2-study\src\data"

FILES = [
    "boki2-exam-advjournal.json", "boki2-exam-corp.json", "boki2-exam-depr.json",
    "boki2-exam-errors.json", "boki2-exam-financial.json", "boki2-exam-labor.json",
    "boki2-exam-materials.json", "boki2-exam-overhead.json", "boki2-exam-partnership.json",
    "boki2-exam-product.json", "calc-training-cogm.json", "calc-training-extra.json",
    "calc-training.json", "subject-b-training.json",
]

CATEGORY_MAP = {
    "Advanced Journal Entries": "上級仕訳",
    "Corporation Accounting": "株式会社会計",
    "Depreciation & Fixed Assets": "減価償却と固定資産",
    "Error Correction": "誤謬訂正",
    "Financial Statements": "財務諸表",
    "Cost Accounting - Labor": "原価計算 - 労務費",
    "Cost Accounting - Materials": "原価計算 - 材料費",
    "Cost Accounting - Overhead": "原価計算 - 製造間接費",
    "Partnership": "組合会計",
    "Product Costing": "製品原価計算",
    "Cost of Goods Manufactured": "製品製造原価",
    "Process Costing": "工程別原価計算",
    "Depreciation Methods": "減価償却方法",
    "Complete Accounting Cycle": "会計一巡",
}

def has_english(text):
    """Check if text contains significant English words (not just numbers/symbols)."""
    # Remove numbers, symbols, Japanese chars
    cleaned = re.sub(r'[0-9,.\-+%/\(\)\s：、。¥円時間株年月日分秒]', '', text)
    # Check for remaining Latin characters
    if re.search(r'[a-zA-Z]{2,}', cleaned):
        return True
    return False

def translate_terms(t):
    """Replace English accounting terms with Japanese."""
    # Journal entry format
    t = t.replace("(Debit)", "(借方)").replace("(Credit)", "(貸方)")
    
    # Account names - order: longer phrases first
    accounts = [
        ("Allowance for Doubtful Accounts", "貸倒引当金"),
        ("Raw Materials Inventory", "原材料"),
        ("Raw and In Process Inventory", "材料・仕掛品"),
        ("Work in Process Inventory", "仕掛品"),
        ("Finished Goods Inventory", "製品"),
        ("Common Stock Subscribed", "株式引受済"),
        ("Common Stock Distributable", "株式配当未払"),
        ("Subscriptions Receivable", "株式引受金"),
        ("Additional Paid-in Capital", "株式払込剰余金"),
        ("APIC from Treasury Stock", "自己株式取引による株式払込剰余金"),
        ("APIC - Preferred", "優先株式払込剰余金"),
        ("Sales Returns and Allowances", "売上値引及び返品"),
        ("Purchase Returns and Allowances", "仕入戻し及び値引"),
        ("Property Dividends Payable", "未払現物配当金"),
        ("Appropriation for Plant Expansion", "工場拡張積立金"),
        ("Unearned Rent Revenue", "前受家賃収益"),
        ("Unearned Service Revenue", "前受サービス収益"),
        ("Retained Earnings", "繰越利益剰余金"),
        ("Accounts Receivable", "売掛金"),
        ("Accounts Payable", "買掛金"),
        ("Notes Receivable", "受取手形"),
        ("Notes Payable", "支払手形"),
        ("Interest Receivable", "未収利息"),
        ("Interest Payable", "未払利息"),
        ("Interest Revenue", "受取利息"),
        ("Interest Income", "受取利息"),
        ("Interest Expense", "支払利息"),
        ("Dividends Payable", "未払配当金"),
        ("Wages Payable", "未払給与"),
        ("Bonus Payable", "未払賞与"),
        ("Social Insurance Payable", "未払社会保険料"),
        ("Unearned Revenue", "前受収益"),
        ("Deferred Tax Liability", "繰延税金負債"),
        ("Common Stock", "普通株式"),
        ("Preferred Stock", "優先株式"),
        ("Treasury Stock", "自己株式"),
        ("Discount on Common Stock", "株式割引"),
        ("Discount on Stock", "株式割引"),
        ("Income Summary", "損益集合"),
        ("Construction in Progress", "建設仮勘定"),
        ("Prepaid Insurance", "前払保険料"),
        ("Prepaid Expenses", "前払費用"),
        ("Accumulated Depreciation", "減価償却累計額"),
        ("Cost of Goods Sold", "売上原価"),
        ("Cost of Goods Manufactured", "製品製造原価"),
        ("Bad Debt Expense", "貸倒損失"),
        ("Bad Debt Recovery", "貸倒償却戻入益"),
        ("Depreciation Expense", "減価償却費"),
        ("Insurance Expense", "保険料"),
        ("Salary Expense", "給与費用"),
        ("Compensation Expense", "報酬費用"),
        ("Organization Expense", "創立費"),
        ("Factory Overhead", "製造間接費"),
        ("Selling Expenses", "販売費"),
        ("Administrative Expenses", "一般管理費"),
        ("Sales Commissions", "販売手数料"),
        ("Advertising Expense", "広告費"),
        ("Delivery Expense", "配送費"),
        ("Freight In", "仕入運賃"),
        ("Freight Out", "発送費"),
        ("Bonus Expense", "賞与引当損"),
        ("Loss on Disposal", "固定資産廃棄損"),
        ("Gain on Disposal", "固定資産売却益"),
        ("Loss on Transfer", "手形譲渡損"),
        ("Gain on Stock Issuance", "株式発行益"),
        ("Gain on Sale of Treasury Stock", "自己株式売却益"),
        ("Gain on Discounting Notes", "手形割引益"),
        ("Provision for Bonuses Payable", "賞与引当金"),
        ("Materials Inventory", "材料棚卸資産"),
        ("Materials Inventory Shortage", "棚卸不足費"),
        ("Scrap Inventory", "仕損品棚卸"),
        ("APIC", "株式払込剰余金"),
        ("Purchases", "仕入"),
        ("Purchases Discounts", "仕入割引"),
        ("Purchase Discounts Taken", "仕入割引"),
        ("Sales Discounts", "売上割引"),
        ("Sales Allowance", "売上値引"),
        ("Purchase Returns", "仕入戻し"),
        ("Sales Returns", "売上返品"),
        ("Credit Card Fee", "クレジットカード手数料"),
        ("Dividend Revenue", "配当収益"),
        ("Dividend Expense", "配当費用"),
        ("Dividends", "配当金"),
        ("Wages Expense", "賃金費用"),
        ("Sales Salaries Expense", "販売員給与"),
        ("Indirect Materials Expense", "間接材料費"),
        ("Manufacturing Expenses", "製造経費"),
        ("Materials Expense", "材料費"),
        ("Labor Cost", "労務費"),
        ("Other Income", "その他の収益"),
        ("Other Expense", "その他の費用"),
        ("Extraordinary Gains and Losses", "特別損益"),
        ("Revenues from core operations", "本業からの収益"),
        ("Gross Sales", "総売上高"),
        ("Selling expense", "販売費"),
        ("General administrative expense", "一般管理費"),
        ("General and administrative", "一般管理費"),
        ("Cash", "現金"),
        ("Investments", "投資"),
        ("Inventory", "棚卸資産"),
        ("Revenue", "収益"),
        ("Expenses", "費用"),
    ]
    for eng, jpn in accounts:
        t = re.sub(re.escape(eng), jpn, t, flags=re.IGNORECASE)
    
    # Terms and phrases
    phrases = [
        ("trade discount", "数量値引"), ("Trade Discount", "数量値引"),
        ("quantity discount", "数量値引"), ("sales discount", "売上割引"),
        ("purchases discount", "仕入割引"), ("purchase discount", "仕入割引"),
        ("cash discount", "現金割引"), ("trade discounts", "数量値引"),
        ("overapplied", "配賦超過"), ("underapplied", "配賦不足"),
        ("overallocated", "配賦超過"), ("underallocated", "配賦不足"),
        ("unfavorable", "不利"), ("favorable", "有利"),
        ("straight-line method", "定額法"), ("declining balance method", "定率法"),
        ("sum-of-the-years'-digits", "級数法"), ("sum of the years' digits", "級数法"),
        ("units of production method", "生産高比例法"), ("units of production", "生産高比例法"),
        ("double declining balance", "定率法"), ("200% DB", "定率法"),
        ("percentage-of-completion", "完成率法"), ("percentage-of-sales method", "売上高基準法"),
        ("percentage-of-receivables method", "売掛金残高基準法"),
        ("aging of receivables approach", "売掛金年齢調整法"),
        ("counterbalancing error", "相殺誤り"), ("non-counterbalancing error", "非相殺誤り"),
        ("prior period adjustment", "前期修正"),
        ("bank reconciliation", "銀行残高調整"), ("outstanding checks", "未決済小切手"),
        ("deposits in transit", "未取立預金"),
        ("net income", "当期純利益"), ("Net Income", "当期純利益"),
        ("gross profit", "売上総利益"), ("Gross Profit", "売上総利益"),
        ("operating income", "営業利益"), ("income from operations", "営業利益"),
        ("income from continuing operations", "継続事業の利益"),
        ("earnings per share", "1株当たり利益"), ("EPS", "1株当たり利益"),
        ("working capital", "運転資本"), ("current ratio", "流動比率"),
        ("quick ratio", "当座比率"), ("acid-test ratio", "当座比率"),
        ("impairment", "減損"),
        ("contra-asset", "対資産勘定"), ("contra-revenue", "対収益勘定"),
        ("property, plant, and equipment", "有形固定資産"),
        ("intangible assets", "無形資産"), ("natural resources", "天然資源"),
        ("salvage value", "残存価額"), ("residual value", "残存価額"),
        ("useful life", "耐用年数"), ("depreciable cost", "減価償却対象原価"),
        ("depreciable asset", "減価償却資産"), ("book value", "簿価"),
        ("market value", "時価"), ("fair market value", "公正時価"),
        ("fair value", "公正価額"), ("par value", "額面"), ("stated value", "設定価額"),
        ("issue price", "発行価額"), ("issuance", "発行"),
        ("no-par stock", "無額面株式"), ("no-par common stock", "無額面普通株式"),
        ("common shares", "普通株式"), ("preferred shares", "優先株式"),
        ("outstanding shares", "発行済株式"), ("outstanding", "発行済"),
        ("weighted-average common shares", "加重平均普通株式数"),
        ("legal capital", "法定資本"), ("stock split", "株式分割"),
        ("stock dividend", "株式配当"), ("cash dividend", "現金配当"),
        ("property dividend", "現物配当"), ("declaration date", "宣言日"),
        ("date of record", "基準日"), ("payment date", "支払日"),
        ("cumulative preferred", "累積優先"), ("participating preferred", "参加的優先"),
        ("callable preferred", "償還優先"), ("convertible preferred", "転換優先"),
        ("conversion ratio", "転換比率"), ("call price", "償還価格"),
        ("limited liability", "有限責任"), ("continuous life", "永続的生命"),
        ("mutual agency", "相互代理"), ("double taxation", "二重課税"),
        ("limited partnership", "有限責任組合"), ("general partner", "無限責任組合員"),
        ("limited partner", "有限責任組合員"),
        ("predetermined overhead rate", "予定間接費配賦率"),
        ("allocation base", "配賦基準"), ("cost driver", "コストドライバー"),
        ("cost pool", "コストプール"), ("activity-based costing", "活動基準原価計算"),
        ("normal costing", "正常原価計算"), ("actual costing", "実際原価計算"),
        ("standard costing", "標準原価計算"), ("absorption costing", "全部原価計算"),
        ("variable costing", "変動原価計算"), ("direct costing", "直接原価計算"),
        ("job-order costing", "個別原価計算"), ("process costing", "工程別原価計算"),
        ("operation costing", "オペレーション原価計算"),
        ("backflush costing", "バックフラッシュ原価計算"),
        ("equivalent units", "換算量"), ("weighted average method", "加重平均法"),
        ("FIFO", "先入先出法"), ("weighted average", "加重平均法"),
        ("joint products", "結合製品"), ("split-off point", "分離点"),
        ("byproducts", "副産物"), ("normal spoilage", "正常仕損"),
        ("abnormal spoilage", "異常仕損"), ("prime costs", "素原価"),
        ("conversion costs", "加工費"), ("direct materials", "直接材料"),
        ("direct labor", "直接労務費"), ("indirect materials", "間接材料"),
        ("indirect labor", "間接労務費"),
        ("departmental overhead rates", "部門別間接費率"),
        ("plant-wide overhead rate", "全工場一括配賦率"),
        ("service department costs", "補助部門費"),
        ("direct method", "直接法"), ("step-down method", "段階法"),
        ("reciprocal method", "相互配賦法"), ("high-low method", "高低点法"),
        ("half-year convention", "半期規約"), ("component depreciation", "コンポーネント減価償却"),
        ("labor rate variance", "労務費率差異"), ("labor efficiency variance", "労務費時間差異"),
        ("material price variance", "材料価格差異"), ("material quantity variance", "材料数量差異"),
        ("material quantity (usage) variance", "材料消費量差異"),
        ("variable overhead spending variance", "変動間接費配賦差異"),
        ("variable overhead efficiency variance", "変動間接費能率差異"),
        ("fixed overhead budget variance", "固定間接費予算差異"),
        ("fixed overhead volume variance", "操業度差異"),
        ("standard rate", "標準賃率"), ("standard hours", "標準時間"),
        ("standard price", "標準価格"), ("standard quantity", "標準消費量"),
        ("actual rate", "実際賃率"), ("actual hours", "実際作業時間"),
        ("actual price", "実際価格"), ("actual quantity", "実際消費量"),
        ("standard cost", "標準原価"), ("actual cost", "実際原価"),
        ("budgeted cost", "予算原価"), ("budgeted", "予算"),
        ("piece-rate wages", "歩合制賃金"), ("piece-rate", "歩合制"),
        ("guaranteed wage plan", "保証賃金制"), ("time tickets", "作業時間票"),
        ("idle time", "アイドルタイム"), ("overtime premium", "残業割増"),
        ("shift premium", "シフト割増"), ("night shift differential", "夜勤差額"),
        ("gross pay", "総支給額"), ("net pay", "手取額"),
        ("employer burden", "雇主負担"), ("employer's share", "雇主負担"),
        ("income tax withholding", "源泉所得税"),
        ("social insurance premiums", "社会保険料"),
        ("learning curve", "学習曲線"), ("efficiency ratio", "能率比"),
        ("moving average method", "移動平均法"), ("physical count", "実地棚卸"),
        ("beginning inventory", "期首棚卸資産"), ("ending inventory", "期末棚卸資産"),
        ("beginning WIP", "期首仕掛品"), ("ending WIP", "期末仕掛品"),
        ("beginning finished goods", "期首製品"), ("ending finished goods", "期末製品"),
        ("beginning raw materials", "期首原材料"), ("ending raw materials", "期末原材料"),
        ("cost of goods available for sale", "当期商品仕入高"),
        ("total manufacturing costs", "総製造費用"),
        ("production cost report", "生産原価報告書"),
        ("job order cost sheet", "ジョブ原価計算書"),
        ("cost reconciliation", "原価配分"),
        ("transferred-in costs", "振替原価"), ("transferred out", "完成品振替"),
        ("completed and transferred out", "完成・振替"),
        ("variable costs", "変動費"), ("fixed costs", "固定費"),
        ("mixed costs", "複合費"), ("variable cost", "変動費"),
        ("fixed cost", "固定費"), ("variable overhead", "変動間接費"),
        ("fixed overhead", "固定間接費"),
        ("overhead applied", "配賦間接費"), ("overhead costs", "間接費"),
        ("total overhead variance", "総間接費差異"),
        ("total labor cost variance", "総労務費差異"),
        ("total material cost variance", "総材料費差異"),
        ("journal entry", "仕訳"), ("adjusting entry", "修正仕訳"),
        ("closing entries", "締切仕訳"), ("trial balance", "試算表"),
        ("accounting equation", "会計等式"),
        ("statement of retained earnings", "繰越利益剰余金計算書"),
        ("income statement", "損益計算書"), ("balance sheet", "貸借対照表"),
        ("statement of cash flows", "キャッシュフロー計算書"),
        ("current assets", "流動資産"), ("current liabilities", "流動負債"),
        ("long-term investments", "投資その他の資産"),
        ("stockholders' equity", "株主資本"), ("net sales", "純売上高"),
        ("total revenue", "総収益"), ("total expenses", "総費用"),
        ("operating expenses", "営業費用"), ("non-operating items", "営業外損益項目"),
        ("other comprehensive income", "その他の包括利益"),
        ("comprehensive income", "包括利益"),
        ("manufacturing company", "製造業者"), ("merchandising company", "卸売業者"),
        ("perpetual inventory system", "継続記録法"),
        ("periodic inventory system", "定期棚卸法"),
        ("allowance method", "繰越法"),
        ("direct write-off method", "直接貸倒法"),
        ("gross method", "総額法"), ("net method", "正味法"),
        ("sales value at split-off method", "分離点売価法"),
        ("net realizable value", "正味実現可能価額"),
    ]
    for eng, jpn in phrases:
        t = re.sub(re.escape(eng), jpn, t, flags=re.IGNORECASE)
    
    # Short word replacements
    for eng, jpn in [("yen","円"),("Debit","借方"),("Credit","貸方"),("shares","株"),("share","株")]:
        t = re.sub(r'\b' + re.escape(eng) + r'\b', jpn, t, flags=re.IGNORECASE)
    
    # Unit phrases
    for eng, jpn in [
        ("per year","/年"),("per hour","/時間"),("per unit","/単位"),
        ("per EU","/換算量"),("per share","/株"),("per direct labor hour","/直接作業時間"),
        ("per machine hour","/機械時間"),
    ]:
        t = re.sub(re.escape(eng), jpn, t, flags=re.IGNORECASE)
    
    return t

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if 'category' in item and item['category'] in CATEGORY_MAP:
            item['category'] = CATEGORY_MAP[item['category']]
        if 'question' in item:
            item['question'] = translate_terms(item['question'])
        if 'options' in item:
            for opt in item['options']:
                if 'text' in opt:
                    opt['text'] = translate_terms(opt['text'])
        for field in ['explanation', 'steps']:
            if field in item:
                item[field] = translate_terms(item[field])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Count remaining English
    english_remaining = 0
    for item in data:
        if has_english(item.get('question', '')):
            english_remaining += 1
        for opt in item.get('options', []):
            if has_english(opt.get('text', '')):
                english_remaining += 1
    
    return english_remaining

total_remaining = 0
for filename in FILES:
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        remaining = process_file(filepath)
        total_remaining += remaining
        print(f"{filename}: {remaining} fields still have English")
    else:
        print(f"NOT FOUND: {filename}")

print(f"\nTotal remaining English fields: {total_remaining}")
