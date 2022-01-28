import datetime
import time

__all__ = ['parse', ]

KINDLE_FIRST_LINE_NOISE = "\xef\xbb\xbf"
KINDLE_DIVIDER = '='*10
KINDLE_DATE_FORMAT = '%Y年%-m月星期* *午%H:%M:%P'
# KINDLE_DATE_FORMAT = '%A, %B %d, %Y, %I:%M %p'
LINE_BREAK = "\n"

def filter_title(title_meta):
    return title_meta[:title_meta.rfind(' (')]

def filter_author(title_meta):
    return title_meta[title_meta.rfind(' (')+2:title_meta.rfind(')')]

def filter_type(meta):
    return meta[2:meta.find(' Loc')]

def filter_location(meta):
    location = meta[meta.find('位置 ')+5:meta.find('的标注')]
    location = location.split("-")[0]
    location = location.split("）")[0]
    # print(location)
    return location

def filter_date(meta):
    text_date = meta[meta.find('添加于 ')+4:]
    # print(text_date)
    year = text_date.split('年')[0]
    month = text_date.split('年')[1].split('月')[0]
    day = text_date.split('年')[1].split('月')[1].split('日')[0]
    time = text_date.split('午')[1:8]
    times = time[0].split(':')
    # print(times)
    # print(year, month, day, time)
    return datetime.datetime(int(year), int(month), int(day), int(times[0]), int(times[1]), int(times[2]))

def parse(filename,
          title_filter=filter_title,
          author_filter=filter_author,
          type_filter=filter_type,
          location_filter=filter_location,
          date_filter=filter_date):
    fp = open(filename, mode='r')
    contents = fp.read()
    fp.close()

    contents = contents.strip().rstrip(KINDLE_DIVIDER)
    blocks = contents.split(KINDLE_DIVIDER)

    ret = []
    for block in blocks:
        # print(block)
        title_meta, meta, _empty_line, notes, _empty_line = block.lstrip().split(LINE_BREAK)
        title = title_filter(title_meta)
        author = author_filter(title_meta)
        type = type_filter(meta)
        location = location_filter(meta)
        date = date_filter(meta)

        ret.append({
            "Title": title,
            # "type": type,
            "Location": location,
            "Date": date,
            "Highlight": notes.strip() if notes.strip() else None,
            "Author": author,
        })
    return ret


