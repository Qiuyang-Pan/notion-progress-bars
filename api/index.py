from flask import Flask, render_template
import datetime
import calendar

app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Point to correct folders


def get_progress_percentages():
    """Calculates the progress percentages for the current year, month, week, and day."""

    # IMPORTANT: Vercel servers typically run in UTC.
    # Calculations will be based on UTC unless you implement timezone handling.
    now = datetime.datetime.utcnow()

    # --- Year Progress ---
    start_of_year = datetime.datetime(now.year, 1, 1)
    days_in_year = 366 if calendar.isleap(now.year) else 365
    end_of_year = start_of_year + datetime.timedelta(days=days_in_year)
    time_passed_year = now - start_of_year
    total_time_year = end_of_year - start_of_year
    # Avoid division by zero edge case right at the start/end
    year_percentage = (
                                  time_passed_year.total_seconds() / total_time_year.total_seconds()) * 100 if total_time_year.total_seconds() > 0 else 0

    # --- Month Progress ---
    start_of_month = datetime.datetime(now.year, now.month, 1)
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    end_of_month = start_of_month + datetime.timedelta(days=days_in_month)
    time_passed_month = now - start_of_month
    total_time_month = end_of_month - start_of_month
    month_percentage = (
                                   time_passed_month.total_seconds() / total_time_month.total_seconds()) * 100 if total_time_month.total_seconds() > 0 else 0

    # --- Week Progress (Assuming Monday is the start of the week, 0=Monday, 6=Sunday) ---
    start_of_week = now - datetime.timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + datetime.timedelta(days=7)
    time_passed_week = now - start_of_week
    total_time_week = end_of_week - start_of_week  # Always 7 days
    week_percentage = (
                                  time_passed_week.total_seconds() / total_time_week.total_seconds()) * 100 if total_time_week.total_seconds() > 0 else 0

    # --- Day Progress ---
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + datetime.timedelta(days=1)
    time_passed_day = now - start_of_day
    total_time_day = end_of_day - start_of_day  # Always 1 day (24 hours)
    day_percentage = (
                                 time_passed_day.total_seconds() / total_time_day.total_seconds()) * 100 if total_time_day.total_seconds() > 0 else 0

    # Return rounded percentages (can adjust precision if needed)
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


# This part is mainly for local testing, Vercel uses the 'app' object directly
if __name__ == "__main__":
    app.run(debug=True)
