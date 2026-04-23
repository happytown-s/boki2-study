import json, glob, os

base = r'C:\Users\haro\.openclaw\workspace\boki2-study\src\data'
files = sorted(glob.glob(os.path.join(base, 'boki2-exam-*.json')))

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    eng_questions = 0
    eng_options = 0
    total_q = len(data)
    total_opt = sum(len(q['options']) for q in data)
    
    for q in data:
        # Check if question has significant English content (not just accounting abbreviations)
        q_text = q['question']
        # Count ASCII letters (not in common abbreviations)
        ascii_letters = sum(1 for c in q_text if c.isascii() and c.isalpha() and c not in 'DLHMHCOGMWIPCOR/EU')
        if ascii_letters > 20:
            eng_questions += 1
        
        for opt in q['options']:
            opt_text = opt['text']
            ascii_letters = sum(1 for c in opt_text if c.isascii() and c.isalpha() and c not in 'DLHMHCOGMWIPCOR/EU')
            if ascii_letters > 15:
                eng_options += 1
    
    status = "OK" if eng_questions == 0 and eng_options == 0 else f"NEEDS WORK ({eng_questions}Q, {eng_options}O still English)"
    print(f"{fname}: {total_q}Q, {total_opt} options - {status}")
