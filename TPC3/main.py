import re
import sys

def process_text(text):
    sum_numbers = 0
    on = False
    for match in re.findall(r'(?:on|off|[+-]?\d+|=)', text, re.IGNORECASE):
        if match.lower() == 'on':
            on = True
        elif match.lower() == 'off':
            on = False
        elif match == '=':
            print(sum_numbers)
        elif match.lstrip('-').isdigit() and on:
            sum_numbers += int(match)

if __name__ == "__main__":
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        text = file.read()
        process_text(text)
