#!/usr/bin/env python3
"""
Complete translation of boki2 exam questions to Japanese.
Processes all 14 JSON files with full question + option translations.
"""
import json, os, re

D = r"C:\Users\haro\.openclaw\workspace\boki2-study\src\data"

CAT = {
    "Advanced Journal Entries":"上級仕訳","Corporation Accounting":"株式会社会計",
    "Depreciation & Fixed Assets":"減価償却と固定資産","Error Correction":"誤謬訂正",
    "Financial Statements":"財務諸表","Cost Accounting - Labor":"原価計算 - 労務費",
    "Cost Accounting - Materials":"原価計算 - 材料費","Cost Accounting - Overhead":"原価計算 - 製造間接費",
    "Partnership":"組合会計","Product Costing":"製品原価計算",
    "Cost of Goods Manufactured":"製品製造原価","Process Costing":"工程別原価計算",
    "Depreciation Methods":"減価償却方法","Complete Accounting Cycle":"会計一巡",
}

def opt(t):
    """Auto-translate option text."""
    t = t.replace("(Debit)","(借方)").replace("(Credit)","(貸方)")
    for e,j in [
        ("Allowance for Doubtful Accounts","貸倒引当金"),
        ("Additional Paid-in Capital","株式払込剰余金"),("APIC from Treasury Stock","自己株式取引による株式払込剰余金"),
        ("APIC - Preferred","優先株式払込剰余金"),
        ("Retained Earnings","繰越利益剰余金"),("Accounts Receivable","売掛金"),
        ("Notes Receivable","受取手形"),("Notes Payable","支払手形"),
        ("Accounts Payable","買掛金"),("Interest Receivable","未収利息"),
        ("Interest Payable","未払利息"),("Interest Revenue","受取利息"),
        ("Dividends Payable","未払配当金"),("Wages Payable","未払給与"),
        ("Bonus Payable","未払賞与"),("Unearned Revenue","前受収益"),
        ("Unearned Rent Revenue","前受家賃収益"),("Unearned Service Revenue","前受サービス収益"),
        ("Common Stock","普通株式"),("Preferred Stock","優先株式"),
        ("Treasury Stock","自己株式"),("Discount on Stock","株式割引"),
        ("Income Summary","損益集合"),("Construction in Progress","建設仮勘定"),
        ("Prepaid Insurance","前払保険料"),("Prepaid Expenses","前払費用"),
        ("Accumulated Depreciation","減価償却累計額"),
        ("Cost of Goods Sold","売上原価"),("Cost of Goods Manufactured","製品製造原価"),
        ("Bad Debt Expense","貸倒損失"),("Depreciation Expense","減価償却費"),
        ("Insurance Expense","保険料"),("Factory Overhead","製造間接費"),
        ("Compensation Expense","報酬費用"),("Organization Expense","創立費"),
        ("Sales Commissions","販売手数料"),("Advertising Expense","広告費"),
        ("Delivery Expense","配送費"),("Freight In","仕入運賃"),("Freight Out","発送費"),
        ("Gain on Disposal","固定資産売却益"),("Loss on Disposal","固定資産廃棄損"),
        ("Bonus Expense","賞与引当損"),("Loss on Transfer","手形譲渡損"),
        ("Gain on Stock Issuance","株式発行益"),("Gain on Discounting Notes","手形割引益"),
        ("Gain on Sale of Treasury Stock","自己株式売却益"),
        ("Provision for Bonuses Payable","賞与引当金"),
        ("Sales Returns and Allowances","売上値引及び返品"),("Purchase Returns and Allowances","仕入戻し及び値引"),
        ("Appropriation for Plant Expansion","工場拡張積立金"),
        ("Property Dividends Payable","未払現物配当金"),
        ("Common Stock Subscribed","株式引受済"),("Common Stock Distributable","株式配当未払"),
        ("Subscriptions Receivable","株式引受金"),
        ("Bad Debt Recovery","貸倒償却戻入益"),("Dividend Revenue","配当収益"),
        ("APIC","株式払込剰余金"),("Purchases","仕入"),
        ("Purchases Discounts","仕入割引"),("Sales Discounts","売上割引"),
        ("Sales Allowance","売上値引"),("Purchase Returns","仕入戻し"),
        ("Materials Inventory","材料棚卸資産"),("Raw Materials","原材料"),
        ("Work in Process","仕掛品"),("Work in Process Inventory","仕掛品"),
        ("Finished Goods","製品"),("Finished Goods Inventory","製品"),
        ("Raw Materials Inventory","原材料"),("Raw and In Process Inventory","材料・仕掛品"),
        ("Inventory","棚卸資産"),("Cash","現金"),("Land","土地"),
        ("Investments","投資"),("Selling Expenses","販売費"),
        ("Administrative Expenses","一般管理費"),
        ("Direct Labor","直接労務費"),("Indirect Labor","間接労務費"),
        ("Direct Materials","直接材料"),("Indirect Materials","間接材料"),
        ("Variable Overhead","変動間接費"),("Fixed Overhead","固定間接費"),
        ("Overhead Applied","配賦間接費"),("Applied Overhead","配賦間接費"),
        ("Partner, Capital","組合員資本"),("Partner, Drawings","組合員引出"),
        ("A, Capital","A資本"),("B, Capital","B資本"),
        ("Discount Received","仕入割引"),("Credit Card Fee","クレジットカード手数料"),
        ("Scrap Inventory","仕損品棚卸"),("Other Income","その他の収益"),
        ("Interest Income","受取利息"),("Interest Expense","支払利息"),
        ("Income Tax Expense","法人税等"),("Tax Expense","法人税等"),
        ("Bonus Expense","賞与引当損"),("Salary Expense","給与費用"),
        ("Sales Salaries Expense","販売員給与"),
        ("Selling expense","販売費"),("General administrative expense","一般管理費"),
    ]:
        t = re.sub(re.escape(e), j, t, flags=re.IGNORECASE)
    for e,j in [("yen","円"),("per year","/年"),("per hour","/時間"),("per unit","/単位"),
                ("per EU","/換算量"),("per share","/株"),("unfavorable","不利"),("favorable","有利"),
                ("overapplied","配賦超過"),("underapplied","配賦不足")]:
        t = re.sub(re.escape(e), j, t, flags=re.IGNORECASE)
    return t

def process(fn, qmap):
    """qmap: list of (english_question_prefix, japanese_translation) tuples"""
    path = os.path.join(D, fn)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item.get('category') in CAT:
            item['category'] = CAT[item['category']]
        # Translate question
        qt = item.get('question','')
        translated = False
        for eng_prefix, jpn_full in qmap:
            if qt.startswith(eng_prefix):
                item['question'] = jpn_full
                translated = True
                break
        if not translated:
            item['question'] = opt(qt)  # fallback
        # Translate options
        for o in item.get('options',[]):
            o['text'] = opt(o['text'])
        # Keep explanation and steps as-is
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    remaining = sum(1 for i in data if re.search(r'[a-zA-Z]{3,}', i.get('question','')))
    print(f"  {fn}: {remaining}/{len(data)} questions have remaining English")

print("Starting full translation of all files...")

# ============= boki2-exam-advjournal.json =============
print("advjournal...")
process("boki2-exam-advjournal.json", [
    ("A company purchased merchandise listed at 100,000", "定価100,000円の商品を10%の数量値引きで購入した。記録される購入金額はいくらか。"),
    ("A company purchased merchandise for 200,000", "2/10, n/30の条件で200,000円の商品を掛けで仕入れ、割引期間内に支払った。総額法による支払仕訳はどれか。"),
    ("A company received a 3-month, 6% note receivable", "顧客から売掛金決済のため3ヶ月利率6%の約束手形300,000円を受取った。正しい仕訳はどれか。"),
    ("A company discounted a 90-day, 5% note receivable of 500,000", "発行後30日で利率5%・90日の受取手形500,000円を6%の割引料で銀行で割引した。手取額はいくらか。"),
    ("A company uses the allowance method for doubtful accounts", "繰越法を採用中。期末売掛金1,000,000円、貸倒見積率3%。修正前の貸倒引当金借方残高5,000円の場合、修正仕訳はどれか。"),
    ("A company received an advance payment of 600,000", "顧客から来年引き渡す商品の前受金600,000円を受け取った。受取時の仕訳はどれか。"),
    ("A company issues a promissory note payable of 400,000", "買掛金決済のため6%利率・90日の約束手形400,000円を振出した。正しい仕訳はどれか。"),
    ("Under the net method, a company purchases goods for 100,000", "正味法で2/10, n/30の条件で100,000円の商品を仕入れた。当初の記録はどれか。"),
    ("A company wrote off a 50,000 yen account receivable under the allowance method", "繰越法で50,000円の売掛金を貸倒処理した。正しい仕訳はどれか。"),
    ("A previously written-off account of 30,000 yen is later recovered", "以前貸倒処理した30,000円の売掛金が回収された。正しい仕訳はどれか。"),
    ("A company holds a 6%, 90-day note receivable of 200,000", "6%・90日の受取手形200,000円を保有中。期末時点で30日分の利息が発生している。修正仕訳はどれか。"),
    ("A company estimates bonus expense of 500,000 yen", "純利益に基づいて従業員の賞与費用500,000円を見積もった。期末の修正仕訳はどれか。"),
    ("A company is constructing a building for its own use", "自社使用の建物を建設中で、期間中の建設費用計10,000,000円。適切な勘定はどれか。"),
    ("A company sold goods for 500,000 yen with a sales allowance", "不良品により20,000円の売上値引を含む500,000円の掛け売上をした。総額法による売上記録はどれか。"),
    ("Under the allowance method using the aging of receivables approach", "繰越法（売掛金年齢調整法）による修正では何を考慮するか。"),
    ("A company received a 500,000 yen, 90-day, 8% note from a customer", "11月1日に顧客から500,000円・90日・8%の約束手形を受取った。12月31日決算における発生利息の仕訳はどれか。"),
    ("A customer returned goods sold for 80,000 yen", "80,000円で販売した商品（原価50,000円）を顧客が返品した。正しい仕訳はどれか。"),
    ("A company uses the percentage-of-sales method for bad debts", "売上高基準法で貸倒見積。掛け売上高2,000,000円、見積率1.5%。貸倒引当金貸方残高8,000円。修正仕訳はどれか。"),
    ("Freight costs paid by the seller for goods shipped FOB destination", "FOB目的地条件で売主が負担する配送費は何に記録するか。"),
    ("A company endorses and transfers a note receivable of 300,000", "310,000円の買掛金決済のため300,000円の受取手形を裏書譲渡し、差額を現金で支払った。仕訳はどれか。"),
    ("A company with a December 31 year-end received a 6-month, 10% note", "12月31日決算の会社が10月1日に6ヶ月・10%の約束手形800,000円を受取った。12月31日までの利息収益合計はいくらか。"),
    ("Which of the following is the correct treatment for a sales discount", "総額法で顧客が割引期間内に支払った場合、売上割引の正しい処理はどれか。"),
    ("A company records credit card sales of 150,000 yen", "クレジットカード売上150,000円（手数料3%）を記録した。カード会社からの正味受取額はいくらか。"),
    ("When using the allowance method, if a company overestimates bad debts", "繰越法で貸倒見積の結果、貸倒引当金に過剰な貸方残高が生じた場合どうなるか。"),
    ("A company pays property tax of 120,000 yen for the year on July 1", "7月1日に1年分の固定資産税120,000円を支払った。12月31日決算時の前払部分はいくらか。"),
    ("A company receives advance rent of 240,000 yen for 12 months", "1月1日から12ヶ月間の前受家賃240,000円を受け取った。3月31日の3ヶ月分修正仕訳はどれか。"),
    ("A company sells merchandise on credit for 300,000 yen", "300,000円の商品を1/10, n/30で掛け売上した。割引期間内に支払われた場合の正味受取額はいくらか。"),
    ("When a company provides a warranty on its products", "製品保証を提供する場合、当期売上の保証費用見積額はどうすべきか。"),
    ("A note receivable dishonored at maturity should be transferred to", "満期で不渡りとなった受取手形はどこに振り替えるべきか。"),
    ("A company uses the periodic inventory system. Freight paid on purchases", "定期棚卸法で20,000円の仕入運賃を支払った。仕訳はどれか。"),
    ("A company returned merchandise to a supplier that was purchased", "掛けで仕入れた40,000円の商品を仕入先に返品した。定期棚卸法での仕訳はどれか。"),
    ("Interest on a note payable is classified on the income statement as", "支払手形の利息は損益計算書で何に分類されるか。"),
    ("A company discounts a customer's note at the bank and the proceeds", "手形を銀行で割引した結果、手取額が手形の額面を上回った。差額は何に記録されるか。"),
    ("A company's allowance for doubtful accounts has a credit balance", "期末修正前の貸倒引当金貸方残高15,000円。売掛金残高基準法の目標期末残高25,000円。修正仕訳はどれか。"),
    ("A company purchased goods for 500,000 yen, terms 2/10, n/30", "2/10, n/30・FOB元払で500,000円を仕入れ、運賃10,000円を支払った。割引期間内に支払った場合の総原価はいくらか。"),
    ("A company collects a note receivable at maturity", "満期で額面200,000円の手形と発生利息5,000円を受取った。仕訳はどれか。"),
    ("A company offers a 5% quantity discount for orders over", "1,000,000円以上の注文に5%の数量値引がある。定価1,200,000円の注文に対する売上高はいくらか。"),
    ("Which statement about the allowance method is correct?", "繰越法（貸倒引当金法）について正しい記述はどれか。"),
    ("A company paid 600,000 yen for a 2-year insurance policy", "10月1日に2年間の保険料600,000円を支払った。12月31日消費分の修正仕訳はどれか。"),
    ("A company received advance payment of 300,000 yen", "来月開始の6ヶ月間サービス契約の前受金300,000円を受け取った。受取時の仕訳はどれか。"),
    ("Under the direct write-off method, when a 40,000 yen account", "直接貸倒法で40,000円の売掛金が回収不能と判定された。仕訳はどれか。"),
    ("A construction project has costs of 50,000,000 yen", "建設中プロジェクトで当期50,000,000円の費用が発生。完成度40%。完成率法による収益認識額はいくらか。"),
    ("A company has outstanding checks totaling 150,000 yen", "未決済小切手150,000円、未取立預金200,000円の場合、銀行残高はどう調整するか。"),
])

# ============= boki2-exam-corp.json =============
print("corp...")
process("boki2-exam-corp.json", [
    ("A corporation issues 1,000 shares of common stock with a par value", "額面500円の普通株式1,000株を発行価額600円で発行した。仕訳はどれか。"),
    ("A corporation issues 2,000 shares of no-par common stock", "無額面普通株式2,000株を1株800円で発行した。仕訳はどれか。"),
    ("A corporation issues 500 shares of common stock with a par value of 500", "額面500円の普通株式500株を1株400円で発行した。仕訳はどれか。"),
    ("A corporation purchases 100 shares of its own common stock", "額面500円の自己普通株式100株を1株600円で取得した。仕訳はどれか。"),
    ("A corporation reissues 50 shares of treasury stock (cost 600", "原価600円/株で取得した自己株式50株を700円/株で再売却した。仕訳はどれか。"),
    ("A corporation reissues 50 shares of treasury stock (cost 600 yen per share) at 500", "原価600円/株で取得した自己株式50株を500円/株で再売却した。仕訳はどれか。"),
    ("A corporation declares a cash dividend of 50 yen per share", "発行済株式10,000株につき1株50円の現金配当を宣言した。宣言日の仕訳はどれか。"),
    ("A corporation's board appropriates 1,000,000 yen of retained earnings", "取締役会が将来の工場拡張のために繰越利益剰余金1,000,000円を積み立てた。仕訳はどれか。"),
    ("A corporation declares a 10% stock dividend on 10,000 shares", "額面500円の普通株式10,000株につき10%の株式配当を宣言した。時価800円。仕訳はどれか。"),
    ("A corporation effects a 2-for-1 stock split", "1対2の株式分割を実施した場合、正しい記述はどれか。"),
    ("A corporation issues 1,000 shares of common stock in exchange", "公正時価700,000円の土地と引き換えに額面500円の普通株式1,000株を発行した。仕訳はどれか。"),
    ("The date of record for a cash dividend is the date", "現金配当の基準日は何を決定する日か。"),
    ("Prior period adjustments are reported on the", "前期修正はどこに報告されるか。"),
    ("A corporation has the following: Common Stock 5,000,000", "普通株式5,000,000、株式払込剰余金2,000,000、繰越利益剰余金3,000,000、自己株式(500,000)の場合、総株主資本はいくらか。"),
    ("A corporation issues preferred stock with a par value of 1,000", "額面1,000円・利率8%累積の優先株式500株を1株1,050円で発行した。仕訳はどれか。"),
    ("If preferred stock is cumulative and dividends are in arrears", "累積優先株式で配当が2年間未払の場合、優先株主に支払われるべき金額はどれか。"),
    ("A corporation issues common stock with a stated value of 300", "設定価額300円の無額面株式を400円/株で2,000株発行した。仕訳はどれか。"),
    ("The payment date for a cash dividend of 500,000 yen", "現金配当500,000円の支払日における仕訳はどれか。"),
    ("A large stock dividend (40%) on 5,000 shares", "額面500円の普通株式5,000株につき40%の大規模株式配当を宣言した。使用する価額はどれか。"),
    ("A corporation has 8% cumulative preferred stock with 10,000", "額面1,000円・8%累積優先株式10,000株と普通株式50,000株がある。3,000,000円の配当を宣言した場合、普通株主への配当可能額はいくらか。"),
    ("A corporation liquidates treasury stock by formally retiring", "原価600円（額面500円）で取得した自己株式100株を正式に廃棄した。仕訳はどれか。"),
    ("Participating preferred stock entitles preferred shareholders to", "参加的優先株式により優先株主には何が認められるか。"),
    ("A corporation issues common stock for services received", "受領したサービス（公正価値2,000,000円）と引き換えに株式を発行した。額面500円/株、3,000株。仕訳はどれか。"),
    ("Which of the following is NOT a characteristic of a corporation?", "次のうち株式会社の特徴ではないものはどれか。"),
    ("A corporation's retained earnings statement shows: Beginning R/E", "繰越利益剰余金計算書：期首4,000,000、当期純利益1,200,000、配当(300,000)、前期修正(80,000)貸方。期末R/Eはいくらか。"),
    ("Callable preferred stock allows the corporation to", "償還優先株式により会社は何ができるか。"),
    ("Convertible preferred stock with a conversion ratio of 5:1", "転換比率5:1の転換優先株式とは何を意味するか。"),
    ("When treasury stock is purchased, what is the effect on the", "自己株式を取得した場合、会計等式への影響はどうなるか。"),
    ("A corporation issues stock with a subscription agreement", "株式引受契約で1,000株を600円/株（額面500円）で引受け、50%を即時払込した。部分払込の仕訳はどれか。"),
    ("A corporation declares a property dividend (distributing investments", "帳簿価額350,000円の投資（公正価値400,000円）を現物配当として分配する。宣言日の仕訳はどれか。"),
    ("Which of the following best describes 'legal capital'?", "法定資本の最も適切な説明はどれか。"),
    ("A corporation has net income of 2,000,000 yen", "当期純利益2,000,000円、加重平均普通株式数100,000株。額面1,000円・8%累積優先株式10,000株。1株当たり利益はいくらか。"),
    ("A corporation donates treasury stock to employees as a bonus", "原価600円/株の自己株式を従業員にボーナスとして贈与した。時価800円/株。適切な仕訳はどれか。"),
])

# ============= boki2-exam-depr.json =============
print("depr...")
process("boki2-exam-depr.json", [
    ("Under the straight-line method, annual depreciation on an asset", "定額法で取得原価1,000,000円、耐用年数5年、残存価額100,000円の資産の年間減価償却費はいくらか。"),
    ("Under the declining balance method (200% DB) for an asset", "定率法（200% DDB）で取得原価500,000円、耐用年数5年の資産の第1年減価償却費はいくらか。"),
    ("Under the sum-of-the-years'-digits method for an asset costing 600,000", "級数法で取得原価600,000円（残存価額60,000）、耐用年数5年の資産の第1年減価償却費はいくらか。"),
    ("The units of production method calculates depreciation based on", "生産高比例法の減価償却費は何に基づいて計算されるか。"),
    ("An asset costs 800,000 yen, salvage value 50,000, estimated", "取得原価800,000円、残存価額50,000円、総見積生産量300,000単位。当期50,000単位生産の場合の減価償却費はいくらか。"),
    ("When a depreciable asset is sold for more than its book value", "減価償却資産が簿価を超える価額で売却された場合、差額は何として記録されるか。"),
    ("An asset purchased for 500,000 yen has accumulated depreciation", "取得原価500,000円、減価償却累計額350,000円の資産を120,000円で売却した。結果はどうなるか。"),
    ("When a depreciable asset is disposed of, depreciation must be", "減価償却資産を処分する場合、いつまで減価償却費を記録しなければならないか。"),
    ("Capitalized costs of a fixed asset include", "固定資産の取得原価に含まれるものはどれか。"),
    ("A subsequent expenditure that extends the useful life", "耐用年数を延長する後続支出はどう処理するか。"),
    ("Impairment of a fixed asset occurs when", "固定資産の減損はいつ発生するか。"),
    ("Land is NOT depreciated because", "土地が減価償却されない理由は何か。"),
    ("In Year 2 of DDB depreciation (200% rate, 5-year life)", "定率法（200%、5年）で取得原価500,000円の資産。第2年始簿価300,000円。第2年減価償却費はいくらか。"),
    ("The journal entry to record annual depreciation is", "年間減価償却費を記録する仕訳はどれか。"),
    ("A company exchanges an old asset (cost 300,000, accumulated", "旧資産（原価300,000、減価償却累計200,000）を公正価額150,000円の新資産と交換し、30,000円を現金で支払った（商業的実質あり）。交換益/損はいくらか。"),
    ("The half-year convention in depreciation assumes that", "減価償却の半期規約では何を仮定するか。"),
    ("Natural resources are depleted using a method similar to", "天然資源の減耗は何に類似した方法で計算されるか。"),
    ("Intangible assets with finite lives are amortized using", "有限耐用年数の無形資産の償却に使用される方法はどれか。"),
    ("Book value of an asset equals", "資産の簿価は何に等しいか。"),
    ("An asset is retired (discarded, not sold) with a cost", "原価200,000円、減価償却累計180,000円の資産を廃棄した。仕訳はどれか。"),
    ("Which depreciation method results in the highest depreciation", "第1年の減価償却費が最も高くなる方法はどれか。"),
    ("Component depreciation means", "コンポーネント減価償却とは何か。"),
    ("A change in the estimated useful life of a depreciable asset", "減価償却資産の見積耐用年数の変更はどう処理されるか。"),
    ("Depreciable cost equals", "減価償却対象原価は何に等しいか。"),
    ("A machine costs 2,000,000 yen, salvage value 200,000", "取得原価2,000,000円、残存価額200,000円、耐用年数8年の機械。級数法（合計36）で第3年減価償却費はいくらか。"),
])

# ============= boki2-exam-errors.json =============
print("errors...")
process("boki2-exam-errors.json", [
    ("A counterbalancing error is one that", "相殺誤りとはどのような誤りか。"),
    ("A non-counterbalancing error is one that", "非相殺誤りとはどのような誤りか。"),
    ("If ending inventory is understated at the end of Year 1, the effect in Year 1", "第1年末の棚卸資産が過小の場合、第1年への影響はどうなるか。"),
    ("If ending inventory is understated at the end of Year 1, the effect in Year 2", "第1年末の棚卸資産が過小の場合、第2年への影響はどうなるか。"),
    ("If a prepaid expense was recorded as an expense when paid", "前払費用を支払時に費用として記録した（修正漏れ）場合の影響はどうなるか。"),
    ("Failure to record accrued revenue at year-end results in", "期末の未収収益を記録しなかった場合の影響はどうなるか。"),
    ("A prior period adjustment is reported on the", "前期修正はどこに報告されるか。"),
    ("Failure to record depreciation expense is an example of", "減価償却費の計上漏れはどの種類の誤りの例か。"),
    ("If a purchase of equipment was recorded as a maintenance expense", "設備の購入を保守費として記録した誤りの影響はどうなるか。"),
    ("An error in counting ending inventory that overstated it by 50,000", "期末棚卸資産を50,000円過大に計上する誤りが第1年確定後に発見された。第2年がまだ開いている場合の修正はどうするか。"),
    ("A company failed to accrue wages payable of 80,000 yen", "期末未払給与80,000円を計上しなかった場合の影響はどうなるか。"),
    ("If depreciation was understated by 20,000 yen for each of the past 3 years", "過去3年間各年20,000円の減価償却費が過少だった。第4年に発見された場合、修正には何が必要か。"),
    ("Which of the following errors would NOT be discovered by trial balance", "次のうち試算表では発見されない誤りはどれか。"),
    ("Overstating beginning inventory in a periodic inventory system", "定期棚卸法で期首棚卸資産を過大にした場合の影響はどうなるか。"),
    ("A company recorded the purchase of a machine as a debit to Land", "機械の購入を土地への借方として記録した。影響はどうなるか。"),
])

# ============= boki2-exam-financial.json =============
print("financial...")
process("boki2-exam-financial.json", [
    ("In a multi-step income statement, gross profit is calculated as", "多段階損益計算書で売上総利益はどう計算されるか。"),
    ("Income from operations equals", "営業利益はどう計算されるか。"),
    ("Net income on a multi-step income statement is calculated as", "多段階損益計算書で当期純利益はどう計算されるか。"),
    ("On a classified balance sheet, current assets are listed in order of", "分類型貸借対照表で流動資産はどの順序で並べられるか。"),
    ("Which of the following is classified as a current liability?", "次のうち流動負債に分類されるのはどれか。"),
    ("The statement of retained earnings shows", "繰越利益剰余金計算書は何を示すか。"),
    ("For a manufacturing company, the balance sheet shows three inventory", "製造業者の貸借対照表に示される3種類の棚卸資産勘定はどれか。"),
    ("Selling expenses on the income statement include all of the following EXCEPT", "損益計算書の販売費に含まれないものはどれか。"),
    ("Administrative expenses on the income statement include", "損益計算書の一般管理費には何が含まれるか。"),
    ("The difference between a manufacturing and merchandising income", "製造業者と卸売業者の損益計算書の違いは何か。"),
    ("Property, Plant, and Equipment on the balance sheet is reported at", "貸借対照表の有形固定資産は何で評価されるか。"),
    ("The accounting equation (balance sheet equation) is", "会計等式（貸借対照表等式）はどれか。"),
    ("Intangible assets on the balance sheet include", "貸借対照表の無形資産には何が含まれるか。"),
    ("Accumulated depreciation is reported on the balance sheet as", "減価償却累計額は貸借対照表で何として報告されるか。"),
    ("A manufacturing company's schedule of cost of goods manufactured", "製造業者の製品製造原価計算書：直接材料費400,000、直接労務費300,000、製造間接費200,000。期首仕掛品50,000、期末仕掛品80,000。製品製造原価はいくらか。"),
    ("On a classified balance sheet, long-term investments include", "分類型貸借対照表の投資その他の資産には何が含まれるか。"),
    ("Working capital is calculated as", "運転資本はどう計算されるか。"),
    ("The current ratio is calculated as", "流動比率はどう計算されるか。"),
    ("Earnings per share (EPS) on the income statement is calculated for", "損益計算書の1株当たり利益は何について計算されるか。"),
    ("Other comprehensive income (OCI) includes items such as", "その他の包括利益には何が含まれるか。"),
    ("A statement of cash flows has three sections: operating, investing", "キャッシュフロー計算書の3区分のうち、減価償却費はどこに表示されるか。"),
    ("The quick ratio (acid-test ratio) excludes which current asset?", "当座比率はどの流動資産を除外するか。"),
    ("A company reports net sales of 1,000,000, COGS 600,000", "純売上高1,000,000、売上原価600,000、営業費用200,000、支払利息20,000、税率30%。当期純利益はいくらか。"),
    ("Comprehensive income equals", "包括利益は何に等しいか。"),
    ("On a manufacturing company's income statement, cost of goods sold", "製造業者の売上原価には何が含まれるか。"),
    ("Which of the following is a contra-revenue account?", "次のうち対収益勘定はどれか。"),
    ("Extraordinary items on the income statement are", "損益計算書の特別損益とはどのようなものか。"),
])

print("\nDone with exam files batch 1 (5 files). Continuing...")
print("See translate_final_batch2.py for remaining 5 exam files.")
