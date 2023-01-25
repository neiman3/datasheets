def remove_newline_characters(string):
    res = ""
    for c in string:
        if not (c == "\n" or c == "\r"):
            res += c
    return res

def clean_text(string):
    res = ""
    for char in string:
        if not(char == "\n" or char == "\t" or char == ","):
            res += char
    return res