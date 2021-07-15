

# ik i could just do the string by itself, but i think having it in a list makes it clearer
light_dark_chars = [c for c in '@&9#$AHhwai;:. ']
light_dark_chars2 = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`%s. '.replace('%s', "'")
light_dark_chars3 = '@%#*+=-:. '
print(light_dark_chars2)
dark_light_chars = light_dark_chars.copy()
dark_light_chars.reverse()
num_chars = len(light_dark_chars)


def intense_light(char: str, dist: int):
    if char == '#':
        return light_dark_chars[min(dist // 3, light_dark_chars.index('A'))]
    elif char == ' ':
        return light_dark_chars[min(dist // 3 + light_dark_chars.index(';'), num_chars-1)]
    elif char == '@':
        return '@'
    else:
        raise Exception('unknown character')
