import re

def extract_number(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    else:
        return None
    
def extract_text(text):
    return re.sub(r'[^a-zA-Zа-яА-Я]', '', text).strip()