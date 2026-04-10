from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def calculate_milestones(birth, gender):
    """誕生と性別から記念日リストを計算する"""
    events = [
        {"name": "お七夜", "date": birth + timedelta(days=6)},
        {"name": "お宮参り", "date": birth + timedelta(days=30 if gender == "男の子" else 31)},
        {"name": "百日祝い（お食い初め）", "date": birth + timedelta(days=99)},
        {"name": "ハーフバースデー", "date": birth + relativedelta(months=6)},
        {"name": "1歳", "date": birth + relativedelta(years=1)},
        {"name": "1000日祝い", "date": birth + timedelta(days=999)},
    ]

    # 初節句
    if gender == "女の子":
        hina = date(birth.year, 3, 3)
        if birth > hina: hina = date(birth.year + 1, 3, 3)
        events.append({"name": "初節句 (ひな祭り)", "date": hina})
    else:
        tango = date(birth.year, 5, 5)
        if birth > tango: tango = date(birth.year + 1, 5, 5)
        events.append({"name": "初節句 (こどもの日)", "date": tango})

    # 七五三
    events.extend([
        {"name": "七五三（3歳）", "date": birth + relativedelta(years=3, month=11, day=15)},
        {"name": "七五三（5歳）", "date": birth + relativedelta(years=5, month=11, day=15)},
        {"name": "七五三（7歳）", "date": birth + relativedelta(years=7, month=11, day=15)},
    ])

    # 小学校
    if (birth.month < 4) or (birth.month == 4 and birth.day == 1):
        school_entry_year = birth.year + 6
    else:
        school_entry_year = birth.year + 7
    
    events.append({"name": "小学校 入学", "date": date(school_entry_year, 4, 1), "display": f"{school_entry_year}.04"})
    events.append({"name": "小学校 卒業", "date": date(school_entry_year + 6, 3, 20), "display": f"{school_entry_year + 6}.03"})

    events.sort(key=lambda x: x["date"])
    return events