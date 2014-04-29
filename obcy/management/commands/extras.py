from datetime import datetime
from html.parser import HTMLParser
from api.commands import new_jokes


__author__ = 'kuba'


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


def inputJSON(obj):
    newDic = {}

    for key in obj:
        try:
            if float(key) == int(float(key)):
                newKey = int(key)
            else:
                newKey = float(key)

            newDic[newKey] = obj[key]
            continue
        except ValueError:
            pass

        try:
            newDic[str(key)] = datetime.strptime(obj[key], '%Y-%m-%d %H:%M:%S')
            continue
        except (TypeError, ValueError):
            pass

        newDic[str(key)] = obj[key]

    return newDic


def count_number(set1, set2):
    count = 0
    for word in set1:
        if word in set2:
            count += 1
    return count


def check_if_duplicate(joke, jokes):
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


def remove_dots(body):
    lines = body.split('\n')
    enter = False
    for i, s in reversed(list(enumerate(lines))):
        if len(s.strip()) == 1:
            if not enter:
                lines[i] = ''
                enter = True
            else:
                del lines[i]
        elif s == '':
            del lines[i]

    body = '\n'.join(lines)
    return body


class HTMLStripper(HTMLParser):
    def __init__(self):
        super(HTMLStripper, self).__init__()
        self.text = ""

    def handle_data(self, data):
        self.text += data

    def get_text(self):
        return self.text


def strip_tags(body):
    lines = body.split('\n')
    for word in lines[-1].split():
        if word[0] != '#':
            break
    else:
        del lines[-1]

    for word in lines[0].split():
        if word[0] != '#':
            break
    else:
        del lines[0]

    for i, line in reversed(list(enumerate(lines))):
        lines[i] = line.lstrip()
        if line == '':
            del lines[i]
        else:
            break

    body = '\n'.join(lines)
    return body


def notify_devices(number, last, keys):
    new_jokes(number, last, keys)