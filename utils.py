from datetime import datetime
def format_seconds_mm_ss(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)}:{round(seconds,2):.2f}"

def ConvertResult(time, category):

    if category == "333fm" and time < 100:
        return time
    if time >= 100000: #It means it's mbld
        missed = time % 100
        formattedTime = format_seconds_mm_ss(int(str(time)[2:7])).split(".")[0]
        point = 99-int(str(time)[:2])
        return f"{missed+point} / {2*missed+point} {formattedTime}"
    if time < 6000:
        formattedTime = f"{time/100:.2f}"
    else:
        formattedTime = f"{format_seconds_mm_ss(time/100)}"
    return formattedTime

def ConvertDate(fromDate, toDate):
    if fromDate == toDate:
        return f"{fromDate.strftime('%Y. %b. %d.')}"
    return f"{datetime.strftime(fromDate,'%Y. %b. %d-')}{datetime.strftime(toDate,'%d.')}"