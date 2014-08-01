from datetime import datetime
from html.parser import HTMLParser
import re


def compare(set1, set2):
    len1 = len(set1)
    len2 = len(set2)

    if len1 < len2:
        count = count_number(set1, set2)
    else:
        count = count_number(set2, set1)

    if count / min(len1, len2) > 0.8:
        return True
    else:
        return False


def input_json(obj):
    new_dic = {}

    for key in obj:
        try:
            if float(key) == int(float(key)):
                new_key = int(key)
            else:
                new_key = float(key)

            new_dic[new_key] = obj[key]
            continue
        except ValueError:
            pass

        try:
            new_dic[str(key)] = datetime.strptime(obj[key], '%Y-%m-%d %H:%M:%S')
            continue
        except (TypeError, ValueError):
            pass

        new_dic[str(key)] = obj[key]

    return new_dic


def count_number(set1, set2):
    count = 0
    for word in set1:
        if word in set2:
            count += 1
    return count


def is_duplicate(joke, jokes):
    set1 = set(joke.body.split())

    for second_joke in jokes:
        if second_joke == joke:
            continue
        set2 = set(second_joke.body.split())
        if compare(set1, set2):
            if not joke.duplicate:
                joke.duplicate = second_joke
                joke.save()
            return True
    else:
        return False


class HTMLStripper(HTMLParser):
    def __init__(self):
        super(HTMLStripper, self).__init__()
        self.text = ""

    def handle_data(self, data):
        self.text += data

    def get_text(self):
        return self.text


def clean_content(body):
    body = strip_tags(body)
    body = remove_dots(body)
    body = remove_head(body)
    body = insert_spaces(body)
    return body


def remove_dots(body):
    lines = body.split('\n')
    enter = False
    for i, s in reversed(list(enumerate(lines))):
        if len(s.strip()) == 1 or s == '':
            if not enter:
                lines[i] = ''
                enter = True
            else:
                del lines[i]

    body = '\n'.join(lines)
    return body


def strip_tags(body):
    """Delete the first and last line if they full of hashtags.
    Also strip every line of unnecessary whitespaces."""
    lines = body.split('\n')

    # remove last line if full of hashtags
    for word in lines[-1].split():
        if word[0] != '#':
            break
    else:
        del lines[-1]

    # remove first line if full of hashtags
    for word in lines[0].split():
        if word[0] != '#':
            break
    else:
        del lines[0]

    # strip spaces from every line
    lines = [line.strip() for line in lines]

    body = '\n'.join(lines)
    return body


def remove_head(body):
    """Remove the first one or two lines if they contains '#number'"""
    lines = body.split('\n')
    if len(lines) < 2:
        return body

    for i in range(2):
        line = lines[i]
        if re.match(r'.*#\d+.*', line) is not None:
            lines = lines[i+1:]
            break

    return '\n'.join(lines)


def insert_spaces(body):
    """Insert space between dash and the next letter at the beginning of the line"""
    return re.sub(r'^-([^\s].+)', r'- \1', body.strip(), flags=re.MULTILINE)