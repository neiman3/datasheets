from shutil import get_terminal_size
from difflib import SequenceMatcher


def remove_newline_characters(string):
    res = ""
    for c in string:
        if not (c == "\n" or c == "\r"):
            res += c
    return res


def clean_text(string):
    # remove line breaks, tabs, and NBSPs
    string = string.replace("\n", "")
    string = string.replace("\t", "")
    string = string.replace("\xc2\xa0", " ")
    string = string.replace("\xa0", " ")
    string = string.replace("[Old version datasheet]", "")

    # remove duplicate spaces
    space_flag = False
    res2 = ""
    for c in string:
        if c == " ":
            if not space_flag:
                res2 += c
                space_flag = True
        else:
            res2 += c
            space_flag = False

    return res2


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


def pick_best_description(part_name, list_of_descriptions):
    cleaned_list = []
    descriptions = {}
    for item in list_of_descriptions:
        if not (item == '' or item is None):
            cleaned_list.append(item)
    if len(cleaned_list) == 1:
        return cleaned_list[0]
    for i in range(len(cleaned_list)):
        score = 0
        for j in range(len(cleaned_list)):
            if i == j:
                continue
            score += compare_two_strings(cleaned_list[i], cleaned_list[j])
        descriptions[cleaned_list[i]] = score
    if len(cleaned_list) == 2:
        # Edge case where we have only two options
        if [i for i in descriptions.items()][0][1] < 0.25:
            # they are not similar enough
            print("Two dissimilar descriptions exist for the part {}:".format(part_name))
            print("\t1) {}".format(cleaned_list[0]))
            print("\t2) {}".format(cleaned_list[1]))
            print("\t3) Enter a custom description")
            user_input = input("\tPlease select one [1,2,3] > ")
            if user_input.isnumeric():
                if (1 <= int(user_input) <= 2):
                    return cleaned_list[int(user_input)-1]
                else:
                    return input("\tPlease enter a custom description >")
            else:
                return [i for i in descriptions.items()][0][0]
    return find_highest_value(descriptions)


def sort_dict_by_length(dictionary):
    return {key: val for key, val in sorted(dictionary.items(), key=lambda ele: len(ele[0]), reverse=True)}


def find_highest_value(dictionary):
    max = None
    max_index = None
    keys = [i for i in dictionary.keys()]
    for i in range(len(keys)):
        if max_index is None:
            max = dictionary[keys[i]]
            max_index = i
        else:
            if dictionary[keys[i]] > max:
                max = dictionary[keys[i]]
                max_index = i
    return keys[max_index]


def compare_two_strings(string_1, string_2):
    return SequenceMatcher(None, string_1, string_2).ratio()

