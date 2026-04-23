import json

files_to_check = {
    'errors': r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data\boki2-exam-errors.json',
    'materials': r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data\boki2-exam-materials.json',
    'overhead': r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data\boki2-exam-overhead.json',
    'corp': r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data\boki2-exam-corp.json',
    'advjournal': r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data\boki2-exam-advjournal.json',
    'product': r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data\boki2-exam-product.json',
}

for name, fpath in files_to_check.items():
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"=== {name} ===")
    for i, q in enumerate(data):
        ascii_q = sum(1 for c in q['question'] if c.isascii() and c.isalpha() and c not in 'DLHMHCOGMWIPCOR/EUJITFOB')
        if ascii_q > 15:
            print(f"  Q{i+1}: {q['question'][:80]}")
            for j, opt in enumerate(q['options']):
                ascii_o = sum(1 for c in opt['text'] if c.isascii() and c.isalpha() and c not in 'DLHMHCOGMWIPCOR/EUJITFOB')
                if ascii_o > 10:
                    print(f"    opt{j}: {opt['text'][:80]}")
    print()
