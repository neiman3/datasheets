from shutil import get_terminal_size

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

def estimated_time_completion(current_num, max_num=None, percent=None, avg_time=1.101):
    # ETC is based on the mean time of delay function
    if percent is not None:
        max_num = current_num / percent * 100
    remaining = max_num - current_num
    # 2 hr 17 min for 7501 items so 1.101 seconds per item
    time_remaining = remaining * avg_time
    hours_remaining = int(time_remaining // 3600)
    min_remaining = int(time_remaining % 3600 // 60)
    sec_remaining = int(time_remaining % 3600 % 60 // 1)
    return ((str(hours_remaining) + " hr ") if hours_remaining != 0 else "") + (
        (str(min_remaining) + " min ") if ((min_remaining + hours_remaining) != 0) else "") + (
        (str(sec_remaining) + " sec"))

def print_same_line(text=""):
    print('\033[1A', end='\x1b[2K')
    size = get_terminal_size()[0]
    if len(str(text)) > size:
        print(str(text)[:(size - 3)] + '...')
    else:
        print(text)
    return