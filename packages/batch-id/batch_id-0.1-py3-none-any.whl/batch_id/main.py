import calendar

def get_Day(day, month, year):
    # If month is January or February, treat it as month 13 or 14 of the previous year
    if month < 3:
        month += 12
        year -= 1

    q = day
    m = month
    K = year % 100  # Last two digits of the year
    J = year // 100  # First two digits of the year

    # Apply Zeller's formula
    h = (q + ((13 * (m + 1)) // 5) + K + (K // 4) + (J // 4) - (2 * J)) % 7

    # Convert h to the actual day name
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    return days[h]


def get_Day_Cal(day, month, year):
    return calendar.day_name[calendar.weekday(year,month,day)]
