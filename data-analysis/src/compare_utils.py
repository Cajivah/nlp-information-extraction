letter_replacements = {
    'ę': 'e',
    'ó': 'o',
    'ą': 'a',
    'ś': 's',
    'ł': 'l',
    'ż': 'z',
    'ź': 'z',
    'ć': 'c',
    'ń': 'n',
}


def deogonkify(str):
    result = []
    for c in str:
        if c in letter_replacements:
            result.append(letter_replacements[c])
        elif c.lower() in letter_replacements:
            result.append(letter_replacements[c.lower()].capitalize())
        else:
            result.append(c)
    return ''.join(result)
