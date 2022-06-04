import re


def to_numeric(text):
    if text[-2:] == 'm²':
        return int(text[:-3])
    elif text[-2] == 'kr':
        return int(text[:-3])

def fix_number(element, postfix_len=2):
    """Strips off whitespace, configured postfix characters and converts number to int"""
    nums = element.text.strip()[:-postfix_len]
    nums = re.sub(r'\s', '', nums)
    return int(nums)
