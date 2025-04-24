from flask import Flask, render_template
import datetime
import calendar
# 导入 timezone 和 timedelta
from datetime import timezone, timedelta

app = Flask(__name__, template_folder='../templates', static_folder='../static')


def get_progress_percentages():
    """Calculates the progress percentages for the current year, month, week, and day based on China Standard Time (UTC+8)."""

    # 定义中国标准时间 (CST = UTC+8)
    cst_tz = timezone(timedelta(hours=8))

    # 获取当前的中国标准时间
    now = datetime.datetime.now(cst_tz)

    # --- 年份进度 ---
    # 创建带时区的年份开始时间
    start_of_year = datetime.datetime(now.year, 1, 1, tzinfo=cst_tz)
    days_in_year = 366 if calendar.isleap(now.year) else 365
    # 下一年的开始时间作为结束时间
    end_of_year = datetime.datetime(now.year + 1, 1, 1, tzinfo=cst_tz)
    time_passed_year = now - start_of_year
    total_time_year = end_of_year - start_of_year
    year_percentage = (
                                  time_passed_year.total_seconds() / total_time_year.total_seconds()) * 100 if total_time_year.total_seconds() > 0 else 0

    # --- 月份进度 ---
    # 创建带时区的月份开始时间
    start_of_month = datetime.datetime(now.year, now.month, 1, tzinfo=cst_tz)
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    # 通过 timedelta 计算月末（避免下个月第一天）
    end_of_month = start_of_month + timedelta(days=days_in_month)
    time_passed_month = now - start_of_month
    total_time_month = end_of_month - start_of_month
    month_percentage = (
                                   time_passed_month.total_seconds() / total_time_month.total_seconds()) * 100 if total_time_month.total_seconds() > 0 else 0

    # --- 周进度 (假设星期一是周的开始, 0=Monday, 6=Sunday) ---
    # now 已经是 CST，所以计算是基于 CST 的星期几
    start_of_week = now - timedelta(days=now.weekday())
    # 重置时间到 00:00:00，保留时区
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    time_passed_week = now - start_of_week
    total_time_week = end_of_week - start_of_week  # 总是 7 天
    week_percentage = (
                                  time_passed_week.total_seconds() / total_time_week.total_seconds()) * 100 if total_time_week.total_seconds() > 0 else 0

    # --- 天进度 ---
    # now 已经是 CST，直接替换时间即可
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    time_passed_day = now - start_of_day
    total_time_day = end_of_day - start_of_day  # 总是 1 天 (24 小时)
    day_percentage = (
                                 time_passed_day.total_seconds() / total_time_day.total_seconds()) * 100 if total_time_day.total_seconds() > 0 else 0

    # 返回四舍五入的百分比
    return {
        "year": round(year_percentage),
        "month": round(month_percentage),
        "week": round(week_percentage),
        "day": round(day_percentage)
    }


@app.route('/')
def home():
    """Serves the progress bar page."""
    progress_data = get_progress_percentages()
    return render_template('index.html', progress=progress_data)


# 本地测试部分
if __name__ == "__main__":
    app.run(debug=True)
