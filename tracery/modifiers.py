def replace(text, *params):
    return text.replace(params[0], params[1])


def capitalizeAll(text, *params):
    return text.title()


def capitalize_(text, *params):
    return text[0].upper() + text[1:]


def a(text, *params):
    if len(text) > 0:
        if text[0].lower() == 'u':
            if len(text) > 2:
                if text[2].lower() == 'i':
                    return "a " + text
        if text[0].lower() in "aeiou":
            return "an " + text
    return "a " + text


def firstS(text, *params):
    text2 = text.split(" ")
    return " ".join([s(text2[0])] + text2[1:])


def s(text, *params):
    if text[-1] in 'shx':
        return text + "es"
    elif text[-1] == 'y':
        if text[-2] not in "aeiou":
            return text[:-1] + "ies"
        else:
            return text + "s"
    else:
        return text + "s"


def ed(text, *params):
    if text[-1] == 'e':
        return text + "d"
    elif text[-1] == 'y':
        if text[-2] not in "aeiou":
            return text[:-1] + "ied"
    else:
        return text + "ed"

base_english = {
    'replace': replace,
    'capitalizeAll': capitalizeAll,
    'capitalize': capitalize_,
    'a': a,
    'firstS': firstS,
    's': s,
    'ed': ed
}
