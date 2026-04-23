#!/usr/bin/env python3
"""Translate all quiz JSON files from English to Japanese using systematic replacement."""

import json
import os
import re

DATA_DIR = r"C:\Users\haro\.openclaw\workspace\boki2-study\src\data"

FILES = [
    "boki2-exam-advjournal.json",
    "boki2-exam-corp.json",
    "boki2-exam-depr.json",
    "boki2-exam-errors.json",
    "boki2-exam-financial.json",
    "boki2-exam-labor.json",
    "boki2-exam-materials.json",
    "boki2-exam-overhead.json",
    "boki2-exam-partnership.json",
    "boki2-exam-product.json",
    "calc-training-cogm.json",
    "calc-training-extra.json",
    "calc-training.json",
    "subject-b-training.json",
]

# Category translations
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

def translate_accounting_terms(text):
    """Systematically replace English accounting terms with Japanese equivalents."""
    
    # Order matters - longer phrases first to avoid partial replacements
    
    # --- Journal entry format ---
    t = text.replace("(Debit)", "(借方)")
    t = t.replace("(Credit)", "(貸方)")
    
    # --- Account names in journal entries ---
    # Assets
    replacements = [
        # Assets
        ("Cash", "現金"),
        ("Accounts Receivable", "売掛金"),
        ("Notes Receivable", "受取手形"),
        ("Interest Receivable", "未収利息"),
        ("Allowance for Doubtful Accounts", "貸倒引当金"),
        ("Raw Materials Inventory", "原材料"),
        ("Materials Inventory", "材料棚卸資産"),
        ("Raw Materials", "原材料"),
        ("Raw and In Process Inventory", "材料・仕掛品"),
        ("Work in Process", "仕掛品"),
        ("Work in Process Inventory", "仕掛品"),
        ("Finished Goods Inventory", "製品"),
        ("Finished Goods", "製品"),
        ("Inventory", "棚卸資産"),
        ("Prepaid Insurance", "前払保険料"),
        ("Prepaid Expenses", "前払費用"),
        ("Prepaid Revenue", "前受収益勘定"),  # rare
        ("Construction in Progress", "建設仮勘定"),
        ("Land", "土地"),
        ("Building", "建物"),
        ("Buildings", "建物"),
        ("Equipment", "設備"),
        ("Machinery", "機械"),
        ("Accumulated Depreciation", "減価償却累計額"),
        ("Marketable Securities", "有価証券"),
        ("Treasury Stock", "自己株式"),
        ("Investments", "投資"),
        ("Property, Plant, and Equipment", "有形固定資産"),
        ("Intangible Assets", "無形資産"),
        ("Scrap Inventory", "仕損品棚卸"),
        
        # Liabilities
        ("Accounts Payable", "買掛金"),
        ("Notes Payable", "支払手形"),
        ("Dividends Payable", "未払配当金"),
        ("Property Dividends Payable", "未払現物配当金"),
        ("Wages Payable", "未払給与"),
        ("Salary Payable", "未払給与"),
        ("Interest Payable", "未払利息"),
        ("Social Insurance Payable", "未払社会保険料"),
        ("Bonus Payable", "未払賞与"),
        ("Provision for Bonuses Payable", "賞与引当金"),
        ("Unearned Revenue", "前受収益"),
        ("Unearned Rent Revenue", "前受家賃収益"),
        ("Unearned Service Revenue", "前受サービス収益"),
        ("Deferred Tax Liability", "繰延税金負債"),
        ("Bonds Payable", "社債"),
        ("Mortgage Payable", "抵当借入金"),
        ("Common Stock Subscribed", "株式引受済"),
        ("Common Stock Distributable", "株式配当未払"),
        ("Subscriptions Receivable", "株式引受金"),
        
        # Equity
        ("Common Stock", "普通株式"),
        ("Preferred Stock", "優先株式"),
        ("Additional Paid-in Capital", "株式払込剰余金"),
        ("APIC", "株式払込剰余金"),
        ("APIC from Treasury Stock", "自己株式取引による株式払込剰余金"),
        ("APIC - Preferred", "優先株式払込剰余金"),
        ("Retained Earnings", "繰越利益剰余金"),
        ("Discount on Common Stock", "株式割引"),
        ("Discount on Stock", "株式割引"),
        ("Appropriation for Plant Expansion", "工場拡張積立金"),
        ("Income Summary", "損益集合"),
        ("Partner, Capital", "組合員資本"),
        ("Partner, Drawings", "組合員引出"),
        ("A, Capital", "A資本"),
        ("B, Capital", "B資本"),
        
        # Revenue
        ("Sales Revenue", "売上高"),
        ("Service Revenue", "サービス収益"),
        ("Rent Revenue", "受取家賃"),
        ("Interest Revenue", "受取利息"),
        ("Interest Income", "受取利息"),
        ("Sales Returns and Allowances", "売上値引及び返品"),
        ("Sales Returns", "売上返品"),
        ("Sales Discounts", "売上割引"),
        ("Sales Allowance", "売上値引"),
        ("Dividend Revenue", "配当収益"),
        ("Other Income", "その他の収益"),
        ("Bad Debt Recovery", "貸倒償却戻入益"),
        ("Gain on Stock Issuance", "株式発行益"),
        ("Gain on Sale of Treasury Stock", "自己株式売却益"),
        ("Gain on Discounting Notes", "手形割引益"),
        ("Gain on Disposal", "固定資産売却益"),
        ("Gain on Retirement", "退職益"),
        
        # Expenses (Contra accounts and regular)
        ("Purchases", "仕入"),
        ("Purchases Discounts", "仕入割引"),
        ("Purchase Returns and Allowances", "仕入戻し及び値引"),
        ("Purchase Returns", "仕入戻し"),
        ("Purchase Discounts Taken", "仕入割引"),
        ("Freight In", "仕入運賃"),
        ("Freight Out", "発送費"),
        ("Delivery Expense", "配送費"),
        ("Cost of Goods Sold", "売上原価"),
        ("Cost of Goods Manufactured", "製品製造原価"),
        ("Depreciation Expense", "減価償却費"),
        ("Bad Debt Expense", "貸倒損失"),
        ("Bonus Expense", "賞与引当損"),
        ("Salary Expense", "給料手当"),
        ("Sales Salaries Expense", "販売員給与"),
        ("Compensation Expense", "報酬費用"),
        ("Wages Expense", "賃金費用"),
        ("Factory Overhead", "製造間接費"),
        ("Applied Overhead", "配賦間接費"),
        ("Insurance Expense", "保険料"),
        ("Organization Expense", "創立費"),
        ("Selling Expenses", "販売費"),
        ("Administrative Expenses", "一般管理費"),
        ("Sales Commissions", "販売手数料"),
        ("Advertising Expense", "広告費"),
        ("Office Salaries", "事務員給与"),
        ("Executive Salaries", "役員報酬"),
        ("Quality Control Costs", "品質管理費"),
        ("Factory Supervisor Salaries", "工場監督者給与"),
        ("Indirect Materials Expense", "間接材料費"),
        ("Manufacturing Expenses", "製造経費"),
        ("Materials Expense", "材料費"),
        ("Loss on Inventory", "棚卸減耗損"),
        ("Loss on Transfer", "手形譲渡損"),
        ("Loss on Disposal", "固定資産廃棄損"),
        ("Loss on Treasury Stock", "自己株式売却損"),
        ("Construction Expense", "建設費"),
        ("Indirect Labor Expense", "間接労務費"),
        ("Salary Expense", "給与費用"),
        ("Dividend Expense", "配当費用"),
        ("Tax Expense", "法人税等"),
        ("Income Tax Expense", "法人税等"),
        ("Labor Cost", "労務費"),
        ("Dividends", "配当金"),
        ("Discount Received", "仕入割引"),
        ("Credit Card Fee", "クレジットカード手数料"),
    ]
    
    for eng, jpn in replacements:
        t = t.replace(eng, jpn)
    
    # --- Common phrases ---
    phrase_replacements = [
        # Descriptive terms
        ("under the gross method", "総額法による"),
        ("Under the gross method", "総額法による"),
        ("under the net method", "正味法による"),
        ("Under the net method", "正味法による"),
        ("under the allowance method", "繰越法（貸倒引当金法）で"),
        ("Under the allowance method", "繰越法（貸倒引当金法）で"),
        ("under the direct write-off method", "直接貸倒法で"),
        ("Under the direct write-off method", "直接貸倒法で"),
        ("under the straight-line method", "定額法による"),
        ("Under the straight-line method", "定額法による"),
        ("under the declining balance method", "定率法による"),
        ("Under the declining balance method", "定率法による"),
        ("under the periodic inventory system", "定期棚卸法で"),
        ("Under the periodic inventory system", "定期棚卸法で"),
        ("under the perpetual inventory system", "継続記録法で"),
        ("Under the perpetual inventory system", "継続記録法で"),
        ("overapplied", "配賦超過"),
        ("underapplied", "配賦不足"),
        ("overallocated", "配賦超過"),
        ("underallocated", "配賦不足"),
        ("unfavorable", "不利"),
        ("favorable", "有利"),
        
        # Misc accounting terms
        ("trade discount", "数量値引き"),
        ("Trade Discount", "数量値引き"),
        ("sales discount", "売上割引"),
        ("purchases discount", "仕入割引"),
        ("purchase discount", "仕入割引"),
        ("cash discount", "現金割引"),
        ("quantity discount", "数量値引き"),
        ("FOB destination", "FOB目的地"),
        ("FOB shipping point", "FOB指定地元払"),
        ("FOB Shipping Point", "FOB指定地元払"),
        ("FOB Destination", "FOB目的地"),
        ("par value", "額面"),
        ("stated value", "設定価額"),
        ("issue price", "発行価額"),
        ("issuance", "発行"),
        ("market price", "時価"),
        ("book value", "簿価"),
        ("fair market value", "公正時価"),
        ("fair value", "公正価額"),
        ("salvage value", "残存価額"),
        ("residual value", "残存価額"),
        ("useful life", "耐用年数"),
        ("depreciable cost", "減価償却対象原価"),
        ("depreciable asset", "減価償却資産"),
        ("accumulated depreciation", "減価償却累計額"),
        ("net income", "当期純利益"),
        ("Net Income", "当期純利益"),
        ("gross profit", "売上総利益"),
        ("Gross Profit", "売上総利益"),
        ("operating income", "営業利益"),
        ("Operating Income", "営業利益"),
        ("income from operations", "営業利益"),
        ("Income from Operations", "営業利益"),
        ("income from continuing operations", "継続事業の利益"),
        ("earnings per share", "1株当たり利益"),
        ("Earnings per share", "1株当たり利益"),
        ("EPS", "1株当たり利益"),
        ("working capital", "運転資本"),
        ("Working Capital", "運転資本"),
        ("current ratio", "流動比率"),
        ("quick ratio", "当座比率"),
        ("acid-test ratio", "当座比率"),
        ("straight-line method", "定額法"),
        ("declining balance method", "定率法"),
        ("sum-of-the-years'-digits method", "級数法"),
        ("sum-of-the-years'-digits", "級数法"),
        ("units of production method", "生産高比例法"),
        ("units of production", "生産高比例法"),
        ("double declining balance", "定率法（200% DDB）"),
        ("percentage-of-completion method", "完成率法"),
        ("percentage-of-sales method", "売上高基準法"),
        ("percentage-of-receivables method", "売掛金残高基準法"),
        ("aging of receivables", "売掛金年齢調整"),
        ("aging approach", "売掛金年齢調整法"),
        ("impairment", "減損"),
        ("contra-asset account", "対資産勘定"),
        ("contra-revenue account", "対収益勘定"),
        ("prior period adjustment", "前期修正"),
        ("counterbalancing error", "相殺誤り"),
        ("non-counterbalancing error", "非相殺誤り"),
        ("bank reconciliation", "銀行残高調整"),
        ("outstanding checks", "未決済小切手"),
        ("deposits in transit", "未取立預金"),
        ("trial balance", "試算表"),
        ("journal entry", "仕訳"),
        ("Journal entry", "仕訳"),
        ("journal entries", "仕訳"),
        ("adjusting entry", "修正仕訳"),
        ("closing entries", "締切仕訳"),
        ("accounting equation", "会計等式"),
        ("balance sheet equation", "貸借対照表等式"),
        ("statement of retained earnings", "繰越利益剰余金計算書"),
        ("income statement", "損益計算書"),
        ("balance sheet", "貸借対照表"),
        ("statement of cash flows", "キャッシュフロー計算書"),
        ("current assets", "流動資産"),
        ("current liabilities", "流動負債"),
        ("long-term investments", "投資その他の資産"),
        ("stockholders' equity", "株主資本"),
        ("equity", "資本"),
        ("net sales", "純売上高"),
        ("total revenue", "総収益"),
        ("total expenses", "総費用"),
        ("gross sales", "総売上高"),
        ("operating expenses", "営業費用"),
        ("non-operating expense", "営業外費用"),
        ("financial expense", "金融費用"),
        ("non-operating items", "営業外損益項目"),
        ("extraordinary item", "特別損益"),
        ("other comprehensive income", "その他の包括利益"),
        ("comprehensive income", "包括利益"),
        ("manufacturing company", "製造業者"),
        ("merchandising company", "卸売業者"),
        ("direct materials used", "直接材料費"),
        ("direct labor", "直接労務費"),
        ("factory overhead", "製造間接費"),
        ("total manufacturing costs", "総製造費用"),
        ("cost of goods available for sale", "当期商品仕入高"),
        ("equivalent units", "換算量"),
        ("equivalent units of production", "換算量"),
        ("EU", "換算量"),
        ("weighted average method", "加重平均法"),
        ("FIFO", "先入先出法"),
        ("weighted average", "加重平均法"),
        ("predetermined overhead rate", "予定間接費配賦率"),
        ("allocation base", "配賦基準"),
        ("cost driver", "コストドライバー"),
        ("cost pool", "コストプール"),
        ("activity-based costing", "ABC（活動基準原価計算）"),
        ("ABC", "ABC"),
        ("normal costing", "正常原価計算"),
        ("actual costing", "実際原価計算"),
        ("standard costing", "標準原価計算"),
        ("absorption costing", "全部原価計算"),
        ("variable costing", "変動原価計算"),
        ("direct costing", "直接原価計算"),
        ("job-order costing", "個別原価計算"),
        ("process costing", "工程別原価計算"),
        ("operation costing", "オペレーション原価計算"),
        ("backflush costing", "バックフラッシュ原価計算"),
        ("just-in-time", "JIT"),
        ("JIT", "JIT"),
        ("joint products", "結合製品"),
        ("split-off point", "分離点"),
        ("byproducts", "副産物"),
        ("normal spoilage", "正常仕損"),
        ("abnormal spoilage", "異常仕損"),
        ("prime costs", "素原価"),
        ("conversion costs", "加工費"),
        ("direct materials", "直接材料"),
        ("direct labor", "直接労務費"),
        ("indirect materials", "間接材料"),
        ("indirect labor", "間接労務費"),
        ("overhead applied", "配賦間接費"),
        ("departmental overhead rates", "部門別間接費率"),
        ("plant-wide overhead rate", "全工場一括配賦率"),
        ("service department costs", "補助部門費"),
        ("direct method", "直接法"),
        ("step-down method", "段階法"),
        ("reciprocal method", "相互配賦法"),
        ("high-low method", "高低点法"),
        ("half-year convention", "半期規約"),
        ("component depreciation", "コンポーネント減価償却"),
        ("natural resources", "天然資源"),
        ("intangible assets", "無形資産"),
        ("finite lives", "有限耐用年数"),
        ("infinite lives", "無限耐用年数"),
        ("goodwill", "のれん"),
        ("patents", "特許権"),
        ("copyrights", "著作権"),
        ("trademarks", "商標権"),
        ("franchise", "フランチャイズ"),
        ("commercial substance", "商業的実質"),
        ("cumulative preferred stock", "累積優先株式"),
        ("participating preferred stock", "参加的優先株式"),
        ("callable preferred stock", "償還優先株式"),
        ("convertible preferred stock", "転換優先株式"),
        ("conversion ratio", "転換比率"),
        ("call price", "償還価格"),
        ("limited partnership", "有限責任組合"),
        ("mutual agency", "相互代理"),
        ("limited liability", "有限責任"),
        ("continuous life", "永続的生命"),
        ("double taxation", "二重課税"),
        ("stock split", "株式分割"),
        ("stock dividend", "株式配当"),
        ("cash dividend", "現金配当"),
        ("property dividend", "現物配当"),
        ("declaration date", "宣言日"),
        ("date of record", "基準日"),
        ("payment date", "支払日"),
        ("ex-dividend", "配当落ち"),
        ("treasury stock", "自己株式"),
        ("legal capital", "法定資本"),
        ("common shares", "普通株式"),
        ("preferred shares", "優先株式"),
        ("no-par stock", "無額面株式"),
        ("no-par common stock", "無額面普通株式"),
        ("outstanding shares", "発行済株式"),
        ("outstanding", "発行済"),
        ("weight-average common shares", "加重平均普通株式数"),
        ("labor rate variance", "労務費率差異"),
        ("labor efficiency variance", "労務費時間差異"),
        ("material price variance", "材料価格差異"),
        ("material quantity variance", "材料数量差異"),
        ("material quantity (usage) variance", "材料数量（消費）差異"),
        ("variable overhead spending variance", "変動間接費配賦差異"),
        ("variable overhead efficiency variance", "変動間接費能率差異"),
        ("fixed overhead budget variance", "固定間接費予算差異"),
        ("fixed overhead volume variance", "操業度差異"),
        ("total overhead variance", "総間接費差異"),
        ("total labor cost variance", "総労務費差異"),
        ("total material cost variance", "総材料費差異"),
        ("standard rate", "標準賃率"),
        ("standard hours", "標準時間"),
        ("standard price", "標準価格"),
        ("standard quantity", "標準消費量"),
        ("actual rate", "実際賃率"),
        ("actual hours", "実際作業時間"),
        ("actual price", "実際価格"),
        ("actual quantity", "実際消費量"),
        ("standard cost", "標準原価"),
        ("actual cost", "実際原価"),
        ("budgeted cost", "予算原価"),
        ("piece-rate", "歩合制"),
        ("piece-rate wages", "歩合制賃金"),
        ("guaranteed wage", "保証賃金"),
        ("time tickets", "作業時間票"),
        ("idle time", "アイドルタイム"),
        ("overtime premium", "残業割増"),
        ("shift premium", "シフト割増"),
        ("night shift differential", "夜勤差額"),
        ("gross pay", "総支給額"),
        ("net pay", "手取額"),
        ("employer burden", "雇主負担"),
        ("employer's share", "雇主負担"),
        ("deductions", "控除"),
        ("income tax withholding", "源泉所得税"),
        ("social insurance premiums", "社会保険料"),
        ("learning curve", "学習曲線"),
        ("efficiency ratio", "能率比"),
        ("materials requisition", "材料出庫票"),
        ("moving average method", "移動平均法"),
        ("physical count", "実地棚卸"),
        ("COGM", "製品製造原価"),
        ("COGS", "売上原価"),
        ("WIP", "仕掛品"),
        ("FG", "製品"),
        ("Beginning WIP", "期首仕掛品"),
        ("Ending WIP", "期末仕掛品"),
        ("Beginning RM", "期首原材料"),
        ("Ending RM", "期末原材料"),
        ("Beginning FG", "期首製品"),
        ("Ending FG", "期末製品"),
        ("Beginning Inventory", "期首棚卸資産"),
        ("Ending Inventory", "期末棚卸資産"),
        ("Beginning finished goods", "期首製品"),
        ("Ending finished goods", "期末製品"),
        ("Beginning raw materials", "期首原材料"),
        ("Ending raw materials", "期末原材料"),
        ("Total Manufacturing Costs", "総製造費用"),
        ("Total Cost to Account For", "総原価配分対象"),
        ("Cost per EU", "換算単位原価"),
        ("transferred out", "完成品振替"),
        ("completed and transferred out", "完成・振替"),
        ("transferred-in costs", "振替原価"),
        ("spoiled goods", "仕損品"),
        ("beginning balance", "期首残高"),
        ("ending balance", "期末残高"),
        ("production cost report", "生産原価報告書"),
        ("job order cost sheet", "ジョブ原価計算書"),
        ("bill of materials", "材料明細表"),
        ("cost reconciliation", "原価配分"),
        ("prime costs", "素原価"),
        ("conversion costs", "加工費"),
        ("variable costs", "変動費"),
        ("fixed costs", "固定費"),
        ("mixed costs", "複合費"),
        ("variable cost per hour", "時間当たり変動費"),
        ("fixed cost per hour", "時間当たり固定費"),
    ]
    
    for eng, jpn in phrase_replacements:
        # Case-insensitive replacement for most terms
        pattern = re.compile(re.escape(eng), re.IGNORECASE)
        t = pattern.sub(jpn, t)
    
    # --- Unit translations ---
    unit_map = {
        "yen": "円",
        "yuan": "元",
        "units": "単位",
        "hours": "時間",
        "DLH": "直接作業時間",
        "MH": "機械時間",
        "per year": "/年",
        "per hour": "/時間",
        "per unit": "/単位",
        "per EU": "/換算量",
        "per share": "/株",
        "per direct labor hour": "/直接作業時間",
        "per machine hour": "/機械時間",
    }
    
    # Simple word replacements
    word_map = {
        "Debit": "借方",
        "Credit": "貸方",
        "debit": "借方",
        "credit": "貸方",
        "shares": "株",
        "share": "株",
        "percent": "%",
        "per": "",
    }
    
    for eng, jpn in word_map.items():
        t = re.compile(r'\b' + re.escape(eng) + r'\b', re.IGNORECASE).sub(jpn, t)
    
    # yen replacement (after word boundary)
    t = re.compile(r'\byen\b', re.IGNORECASE).sub("円", t)
    
    return t


def translate_file(filepath):
    """Read a JSON file, translate questions and options, write back."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = 0
    for item in data:
        # Translate category
        if 'category' in item and item['category'] in CATEGORY_MAP:
            item['category'] = CATEGORY_MAP[item['category']]
        
        # Translate question
        if 'question' in item:
            old_q = item['question']
            item['question'] = translate_accounting_terms(old_q)
            if old_q != item['question']:
                modified += 1
        
        # Translate options
        if 'options' in item:
            for opt in item['options']:
                if 'text' in opt:
                    old_t = opt['text']
                    opt['text'] = translate_accounting_terms(old_t)
                    if old_t != opt['text']:
                        modified += 1
        
        # For calc-training files, also translate explanation and steps
        for field in ['explanation', 'steps']:
            if field in item:
                item[field] = translate_accounting_terms(item[field])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  Modified {modified} fields")
    return len(data)


if __name__ == "__main__":
    total_questions = 0
    for filename in FILES:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            count = translate_file(filepath)
            total_questions += count
        else:
            print(f"  NOT FOUND: {filepath}")
    
    print(f"\nDone! Total questions processed: {total_questions}")
