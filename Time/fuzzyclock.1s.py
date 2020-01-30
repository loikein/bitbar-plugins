#!/usr/bin/python
# encoding=utf8

# <bitbar.title>Fuzzy Clock</bitbar.title>
# <bitbar.author>Dylan Evans + loikein</bitbar.author>
# <bitbar.author.github>whonut</bitbar.author.github>
# <bitbar.desc>Display the current system time in a 'fuzzy' manner, rounding to the nearest 5 minutes and using words.</bitbar.desc>
# <bitbar.version>1.0</bitbar.version>
#
# 1 second refresh rate may be overkill. Wording & formatting of the time may
# also be easily altered below.

from __future__ import absolute_import, division, print_function, unicode_literals
from time import localtime
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def round_to_nearest_five(n):
    '''Round the float n to the nearest 5.'''
    return int(5 * round(n / 5))


def next_hour(hour):
    # modulo before adding one so that 11 => 12 and not 0
    return (hour % 12) + 1


def fuzzy_time(struct_time):
    '''Return the current 'fuzzy time' (rounded to the nearest 5 minutes) as a
       string.'''

    # Split it into hours & minutes and rounding the minutes to make the time
    # 'fuzzy'. Use 12-hour clock.
    hour = (struct_time.tm_hour % 12) or 12
    minute = struct_time.tm_min + (struct_time.tm_sec / 60)
    rounded_min = round_to_nearest_five(minute)
    if rounded_min == 60:
        rounded_min = 0
        hour = next_hour(hour)

    num_word = {1: "一", 2: "两", 3: "三", 4: "四", 5: "五", 6: "六",
                7: "七", 8: "八", 9: "九", 10: "十", 11: "十一",
                12: "十二", 20: "二十", 25: "二十五"}

    # Work out what to display and display it.
    if rounded_min == 0:
        return "{hr}点".format(hr=num_word[hour])
    elif rounded_min == 15:
        return "{hr}点一刻".format(hr=num_word[hour])
    elif rounded_min < 30:
        return "{hr}点 {min} 分".format(min=num_word[rounded_min],
                                      hr=num_word[hour])
    elif rounded_min == 30:
        return "{hr}点半".format(hr=num_word[hour])
    elif rounded_min == 45:
        return "{hr}点三刻".format(hr=num_word[hour])
    else:
        return "差 {min} 分{hr}点".format(min=num_word[60-rounded_min],
                                       hr=num_word[next_hour(hour)])


if __name__ == '__main__':
    print(fuzzy_time(localtime()))
