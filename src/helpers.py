import json

def extract_first_json(text):
    index = 0
    length = len(text)
    
    while index < length:
        if text[index] in ('{', '['):
            start = index
            balance = 1
            in_string = False
            escape_next = False
            index += 1
            while index < length and balance > 0:
                current_char = text[index]
                if in_string:
                    if escape_next:
                        escape_next = False
                    elif current_char == '\\':
                        escape_next = True
                    elif current_char == '"':
                        in_string = False
                else:
                    if current_char == '"':
                        in_string = True
                    elif current_char in ('{', '['):
                        balance += 1
                    elif current_char in ('}', ']'):
                        balance -= 1
                index += 1
            if balance == 0:
                json_str = text[start:index]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    index = start + 1
            else:
                index = start + 1
        else:
            index += 1
    return "No JSON found"  