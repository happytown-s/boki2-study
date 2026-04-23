import json, os

# This script creates fully translated Japanese versions of the 5 remaining exam files.
# The translations are hardcoded for accuracy.

base = r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data'

# ============================================================
# FILE 1: boki2-exam-materials.json (28Q)
# ============================================================
materials = [
  {
    "category": "Cost Accounting - Materials",
    "question": "原材料を500,000円で掛け仕入した。継続記録法での仕訳は：",
    "options": [
      {"text": "(借方) 原材料棚卸資産 500,000 / (貸方) 買掛金 500,000", "correct": True},
      {"text": "(借方) 仕入 500,000 / (貸方) 買掛金 500,000", "correct": False},
      {"text": "(借方) 材料費 500,000 / (貸方) 買掛金 500,000", "correct": False},
      {"text": "(借方) 原材料棚卸資産 500,000 / (貸方) 現金 500,000", "correct": False}
    ],
    "explanation": "継続記録法では、材料仕入は直接原材料に借方記録。定期棚卸法では仕入に借方記録。継続記録法は棚卸資産の継続的な記録を維持する。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "直接材料が生産のために払い出された時の仕訳は：",
    "options": [
      {"text": "(借方) 仕掛品 / (貸方) 原材料棚卸資産", "correct": True},
      {"text": "(借方) 製品製造原価 / (貸方) 原材料棚卸資産", "correct": False},
      {"text": "(借方) 製造間接費 / (貸方) 原材料棚卸資産", "correct": False},
      {"text": "(借方) 材料費 / (貸方) 原材料棚卸資産", "correct": False}
    ],
    "explanation": "直接材料は生産のために払い出された時点で仕掛品に借方記録。間接材料（潤滑油、清掃用品など）は製造間接費に借方記録。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "間接材料が払い出された時の仕訳は：",
    "options": [
      {"text": "(借方) 製造間接費 / (貸方) 原材料棚卸資産", "correct": True},
      {"text": "(借方) 仕掛品 / (貸方) 原材料棚卸資産", "correct": False},
      {"text": "(借方) 製造費用 / (貸方) 買掛金", "correct": False},
      {"text": "(借方) 間接材料費 / (貸方) 原材料棚卸資産", "correct": False}
    ],
    "explanation": "間接材料は特定の製品に直接トレースできないため、製造間接費を通じて配賦される。間接費から予定配賦率を使用して製品に配賦される。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "企業が原材料にFIFOを使用している。期首在庫：10円 x 100単位。仕入1：12円 x 200単位。仕入2：15円 x 150単位。250単位を払い出した場合、払出原価は：",
    "options": [
      {"text": "3,050円", "correct": True},
      {"text": "3,000円", "correct": False},
      {"text": "2,900円", "correct": False},
      {"text": "3,250円", "correct": False}
    ],
    "explanation": "FIFO：期首から100単位（100 x 10 = 1,000）+ 仕入1から150単位（150 x 12 = 1,800）= 250単位分。原価 = 1,000 + 1,800 = 2,800 円。300単位の場合：100x10 + 200x12 = 3,400。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "同じデータで加重平均法を使用した場合：期首100単位 x 10円、仕入200単位 x 12円、仕入150単位 x 15円。総利用可能450単位。250単位を払い出した場合、原価は：",
    "options": [
      {"text": "3,361円", "correct": True},
      {"text": "2,800円", "correct": False},
      {"text": "3,400円", "correct": False},
      {"text": "3,500円", "correct": False}
    ],
    "explanation": "加重平均単価 =（100x10 + 200x12 + 150x15）/ 450 =（1,000 + 2,400 + 2,250）/ 450 = 5,650 / 450 = 12.556 円/単位。250単位の原価 = 250 x 12.556 = 約 3,139 円。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "30,000円の材料仕入戻しは次のように記録される：",
    "options": [
      {"text": "(借方) 買掛金 30,000 / (貸方) 原材料棚卸資産 30,000", "correct": True},
      {"text": "(借方) 現金 30,000 / (貸方) 原材料棚卸資産 30,000", "correct": False},
      {"text": "(借方) 原材料棚卸資産 30,000 / (貸方) 買掛金 30,000", "correct": False},
      {"text": "(借方) 仕入戻し 30,000 / (貸方) 買掛金 30,000", "correct": False}
    ],
    "explanation": "継続記録法では、返品された材料は原材料棚卸資産勘定を直接減額する。掛け金は未払額を減額するため借方記録。定期棚卸法では仕入戻し（対仕入勘定）を使用する。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "材料出庫票：ジョブ101 - 50,000円、ジョブ102 - 30,000円、間接 - 20,000円。正しい仕訳は：",
    "options": [
      {"text": "(借方) 仕掛品 80,000 / (借方) 製造間接費 20,000 / (貸方) 原材料 100,000", "correct": True},
      {"text": "(借方) 仕掛品 100,000 / (貸方) 原材料 100,000", "correct": False},
      {"text": "(借方) 仕掛品 50,000 / (借方) 仕掛品 30,000 / (借方) 製造間接費 20,000 / (貸方) 原材料 100,000", "correct": False},
      {"text": "(借方) 売上原価 100,000 / (貸方) 原材料 100,000", "correct": False}
    ],
    "explanation": "特定ジョブの直接材料（50,000 + 30,000 = 80,000）は仕掛品へ。間接材料（20,000）は製造間接費へ。原材料への総貸方記録は 100,000。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "材料価格差異は次のように計算される：",
    "options": [
      {"text": "(実際価格 - 標準価格) x 実際購入数量", "correct": True},
      {"text": "(実際数量 - 標準数量) x 標準価格", "correct": False},
      {"text": "(標準価格 - 実際価格) x 標準数量", "correct": False},
      {"text": "実際原価 - 予算原価", "correct": False}
    ],
    "explanation": "材料価格差異 =（実際価格 - 標準価格）x 実際購入数量。実際価格が標準を超える場合、差異は不利（会社が予定より高い価格を支払った）。使用する数量は実際購入数量。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "材料の標準原価は1単位あたり100円。実際購入：1,000単位 x 105円。材料価格差異は：",
    "options": [
      {"text": "5,000円 不利", "correct": True},
      {"text": "5,000円 有利", "correct": False},
      {"text": "105,000円 不利", "correct": False},
      {"text": "100,000円 有利", "correct": False}
    ],
    "explanation": "材料価格差異 =（実際価格 - 標準価格）x 実際購入数量 =（105 - 100）x 1,000 = 5,000 円 不利。会社が標準より1単位あたり5円多く支払い、5,000円の不利差異となった。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "材料数量（消費）差異は次のように計算される：",
    "options": [
      {"text": "(実際消費数量 - 標準消費数量) x 標準価格", "correct": True},
      {"text": "(実際価格 - 標準価格) x 実際消費数量", "correct": False},
      {"text": "(標準数量 - 実際数量) x 実際価格", "correct": False},
      {"text": "標準原価 - 実際原価", "correct": False}
    ],
    "explanation": "材料数量差異 =（実際消費数量 - 標準消費数量）x 標準価格。標準消費数量を超える材料を使用した場合、差異は不利。標準消費数量は実際生産量に基づく。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "標準消費数量：2,000単位。実際消費数量：2,100単位。標準価格：50円。材料数量差異は：",
    "options": [
      {"text": "5,000円 不利", "correct": True},
      {"text": "5,000円 有利", "correct": False},
      {"text": "105,000円 不利", "correct": False},
      {"text": "100,000円 有利", "correct": False}
    ],
    "explanation": "材料数量差異 =（2,100 - 2,000）x 50 = 100 x 50 = 5,000 円 不利。会社が標準許容量より100単位多く材料を使用し、各標準単価 50 円で評価される。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "継続記録法における原材料の仕入割引は次のように記録される：",
    "options": [
      {"text": "正味法：(借方) 買掛金 / (貸方) 原材料棚卸資産。総額法：(貸方) 仕入割引", "correct": True},
      {"text": "(借方) 仕入割引 / (貸方) 現金", "correct": False},
      {"text": "売上原価の減額", "correct": False},
      {"text": "重要でないため仕訳不要", "correct": False}
    ],
    "explanation": "継続記録法の総額法：（借方）買掛金 /（貸方）仕入割引（対原価）/（貸方）現金。正味法：棚卸資産は既に正味で記録済み。いずれにせよ割引は材料原価を減額する。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "JIT棚卸システムにおいて、原材料棚卸資産は通常次である：",
    "options": [
      {"text": "生産に必要な時にちょうど到着するため最小化される", "correct": True},
      {"text": "生産が停止しないよう最大化される", "correct": False},
      {"text": "原価ではなく時価で記録される", "correct": False},
      {"text": "固定資産として処理される", "correct": False}
    ],
    "explanation": "JITは、生産に必要な時にちょうど材料が到着することで、棚卸資産保有コストを最小化することを目指す。保管費、廃棄、陳腐化リスクを低減するが、信頼できるサプライヤーと効率的な物流が必要。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "直接材料と間接材料の違いは次のどれか：",
    "options": [
      {"text": "直接材料は特定の製品に経済的かつ便利にトレースできる。間接材料はできない。", "correct": True},
      {"text": "直接材料は常に間接材料より高価である", "correct": False},
      {"text": "間接材料は生産に使用されない", "correct": False},
      {"text": "直接材料は即時費用処理され、間接材料は資産計上される", "correct": False}
    ],
    "explanation": "直接材料（家具用の木材など）は特定の製品にトレースできる。間接材料（接着剤、釘、工場消耗品）は生産に役立つが、個々の単位に経済的にトレースできない。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "材料の移動平均法は各購入後に新しい平均原価を計算する：",
    "options": [
      {"text": "購入", "correct": True},
      {"text": "売上または払出", "correct": False},
      {"text": "生産ロット", "correct": False},
      {"text": "月末決算", "correct": False}
    ],
    "explanation": "移動平均法では、各購入後に全利用可能単位の総原価を全利用可能単位数で割って新しい加重平均単価を計算する。払い出しはこの最新の平均単価で評価される。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "原材料仕入の運賃は次のように記録される：",
    "options": [
      {"text": "原材料棚卸資産原価の一部", "correct": True},
      {"text": "損益計算書の別個の運賃費用", "correct": False},
      {"text": "購入価額の減額", "correct": False},
      {"text": "製造間接費原価の一部", "correct": False}
    ],
    "explanation": "原材料仕入の運賃（仕入運賃）は継続記録法で材料原価に加算される。材料を工場に到着させて使用可能にするために必要なすべての費用が棚卸資産原価に含まれる。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "工場から倉庫に返却された余剰材料は次のように記録される：",
    "options": [
      {"text": "(借方) 原材料棚卸資産 / (貸方) 仕掛品（直接材料の場合）または製造間接費（間接材料の場合）", "correct": True},
      {"text": "(借方) 原材料棚卸資産 / (貸方) 売上原価", "correct": False},
      {"text": "(借方) 現金 / (貸方) 原材料棚卸資産", "correct": False},
      {"text": "次の実地棚卸まで仕訳不要", "correct": False}
    ],
    "explanation": "返却材料は元の出庫を取り消す。直接材料として仕掛品に賦課されていた場合は貸方は仕掛品。製造間接費に賦課されていた場合は貸方は製造間接費。借方は常に原材料棚卸資産。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "再販価値のある生産中の仕損品は次のように記録される：",
    "options": [
      {"text": "(借方) 仕損品棚卸 / (貸方) 仕掛品または製造間接費", "correct": True},
      {"text": "(借方) 現金 / (貸方) 売上高", "correct": False},
      {"text": "即時費用処理", "correct": False},
      {"text": "売却まで仕訳不要", "correct": False}
    ],
    "explanation": "再販価値のある仕損品は資産（仕損品棚卸）として記録し、仕掛品または製造間接費に貸方記録して生産原価を減額する。仕損品が売却された時は現金を借方、仕損品棚卸を貸方。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "企業が標準原価計算を使用している。単位当たり標準材料費：3kg x 100円 = 300円。実際：1,000単位を生産、3,200kg x 95円/kgを使用。総材料費差異は：",
    "options": [
      {"text": "4,000円 不利", "correct": True},
      {"text": "4,000円 有利", "correct": False},
      {"text": "6,000円 有利", "correct": False},
      {"text": "2,000円 不利", "correct": False}
    ],
    "explanation": "実際生産量に対する標準原価：1,000 x 3kg x 100 = 300,000。実際原価：3,200 x 95 = 304,000。総差異 = 300,000 - 304,000 = 4,000 不利。価格差異 =（95-100）x 3,200 = -16,000 有利；数量差異 =（3,200-3,000）x 100 = 20,000 不利；純差異 = 4,000 不利。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "原材料の実地棚卸で帳簿残高より10,000円少ないことが判明した。継続記録法では次のように記録する：",
    "options": [
      {"text": "(借方) 棚卸資産不足費（または売上原価）10,000 / (貸方) 原材料棚卸資産 10,000", "correct": True},
      {"text": "(借方) 売上原価 10,000 / (貸方) 原材料 10,000", "correct": False},
      {"text": "(借方) 棚卸資産評価損 10,000 / (貸方) 原材料 10,000", "correct": False},
      {"text": "仕訳不要 - 年末に調整", "correct": False}
    ],
    "explanation": "継続記録法では、棚卸資産不足は発見時に記録する。不足は費用（棚卸不足費または売上原価に含む場合あり）に借方、原材料棚卸資産に貸方記録。帳簿棚卸を実地棚卸に合わせる。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "定期棚卸法における材料消費高の計算式は：",
    "options": [
      {"text": "期首棚卸 + 仕入 - 期末棚卸", "correct": True},
      {"text": "仕入 - 仕入戻し - 仕入割引", "correct": False},
      {"text": "期末棚卸 + 仕入 - 期首棚卸", "correct": False},
      {"text": "仕入のみ", "correct": False}
    ],
    "explanation": "定期棚卸法：材料消費高 = 期首棚卸 + 純仕入（仕入 - 戻し - 割引 + 運賃）- 期末棚卸。この公式で当期に消費された材料を計算する。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "企業が掛けで材料を仕入。支払条件2/10, n/30、FOB元払（shipping point）。運賃5,000円は売主が前払し請求書に加算。総請求額105,000円。総額法での購入時仕訳は：",
    "options": [
      {"text": "(借方) 原材料棚卸資産 105,000 / (貸方) 買掛金 105,000", "correct": True},
      {"text": "(借方) 原材料棚卸資産 100,000 / (借方) 仕入運賃 5,000 / (貸方) 買掛金 105,000", "correct": False},
      {"text": "(借方) 原材料棚卸資産 100,000 / (貸方) 買掛金 100,000", "correct": False},
      {"text": "(借方) 原材料棚卸資産 102,900 / (貸方) 買掛金 102,900", "correct": False}
    ],
    "explanation": "継続記録法では、材料を取得するために必要なすべての費用（運賃を含む）が棚卸資産原価に含まれる。総額 105,000 を原材料棚卸資産に借方記録。総額法では割引期間内の支払時に割引を適用。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "材料出庫票：ジョブAの直接材料 = 200,000円、ジョブBの直接材料 = 150,000円、工場消耗品 = 30,000円、修繕費 = 20,000円。仕掛品への借方合計は：",
    "options": [
      {"text": "350,000円", "correct": True},
      {"text": "400,000円", "correct": False},
      {"text": "200,000円", "correct": False},
      {"text": "500,000円", "correct": False}
    ],
    "explanation": "直接材料のみ（ジョブA：200,000 + ジョブB：150,000 = 350,000）が仕掛品に借方記録。工場消耗品と修繕（30,000 + 20,000 = 50,000）は間接材料として製造間接費に借方記録。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "工程別原価計算で材料が工程始点で投入される場合、期末仕掛品の材料費完成度は：",
    "options": [
      {"text": "加工費の完成度に関係なく材料は100%", "correct": True},
      {"text": "未完成のため0%", "correct": False},
      {"text": "50% - 仕掛品の標準的平均", "correct": False},
      {"text": "加工費の完成度と同じ", "correct": False}
    ],
    "explanation": "工程の始点で材料が投入される場合、すべての単位（完成品も期末仕掛品も）が100%の材料を受取っている。材料の換算量は物理単位数に等しく、仕掛加工費は部分的。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "バックフラッシュ原価計算は次の追跡を不要にする：",
    "options": [
      {"text": "各生産段階の仕掛品棚卸資産", "correct": True},
      {"text": "原材料の仕入", "correct": False},
      {"text": "製品棚卸資産", "correct": False},
      {"text": "売上原価", "correct": False}
    ],
    "explanation": "バックフラッシュ原価計算は、製品が完成するまで原価計算を遅延させる。コストは完成品から原材料に「フラッシュバック」され、各生産段階の仕掛品追跡が不要になる。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "既存残高300単位 x 46円（合計13,800円）の後に200単位 x 50円の仕入がある。移動平均単価は：",
    "options": [
      {"text": "1単位あたり47.60円", "correct": True},
      {"text": "1単位あたり48.00円", "correct": False},
      {"text": "1単位あたり50.00円", "correct": False},
      {"text": "1単位あたり46.00円", "correct": False}
    ],
    "explanation": "新しい総原価 = 13,800 +（200 x 50）= 13,800 + 10,000 = 23,800。新しい総単位数 = 300 + 200 = 500。移動平均 = 23,800 / 500 = 47.60 円/単位。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "正常仕損品のコストは次に配分される：",
    "options": [
      {"text": "完成品（完成単位のコストに吸収される）", "correct": True},
      {"text": "損益計算書の損失勘定", "correct": False},
      {"text": "製造間接費に配賦され全生産に配分される", "correct": False},
      {"text": "仕損の原因部門のみ", "correct": False}
    ],
    "explanation": "正常仕損は生産に固有のコストであり、良品に吸収される。異常仕損は期待される率を超えるものであり、別途損失として記録する。この区別は原価管理と価格設定に重要。"
  },
  {
    "category": "Cost Accounting - Materials",
    "question": "FIFOの材料元帳カード：期首50単位 x 10円、仕入100単位 x 12円、払出80単位。払出単位の原価は：",
    "options": [
      {"text": "860円", "correct": True},
      {"text": "900円", "correct": False},
      {"text": "920円", "correct": False},
      {"text": "800円", "correct": False}
    ],
    "explanation": "FIFO：まず期首在庫50単位（50 x 10 = 500）を払い出し、次に購入から30単位（30 x 12 = 360）を払い出す。払出単位の総原価 = 500 + 360 = 860 円。"
  }
]

with open(os.path.join(base, 'boki2-exam-materials.json'), 'w', encoding='utf-8') as f:
    json.dump(materials, f, ensure_ascii=False, indent=2)
print("materials: done")
