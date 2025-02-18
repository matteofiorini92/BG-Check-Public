from pathlib import Path
from decimal import Decimal
from datetime import date, datetime
from const import TIMES, RATES, DAYS_OF_THE_WEEK

def read_file(mprn):
    '''
    Read data from a file and return it as a list of strings.
    '''
    today = datetime.strftime(date.today(), '%d-%m-%Y')
    filename = f'HDF_calckWh_{mprn}_{today}.csv'

    downloads_folder = Path.home() / "Downloads"
    file_path = downloads_folder / filename

    with open(file_path, 'r') as f:
        data = f.readlines()
    
    return data


def remove_unused_data(data):
    '''
    Remove the first two columns (MPRN,Meter Serial Number) and the headers row 
    from the data and return the cleaned data.
    '''
    cleaned_data = []
    for line in data[1:]:
        cleaned_line = line.strip()
        cleaned_data.append(cleaned_line.split(',')[2:])

    return cleaned_data


def fix_intervals(data):
    '''
    Fix the dates and times in the data by setting the value in the third column
    to the starting time of the interval instead of the ending time.
    '''
    for line in data:
        year = line[2][6:10]
        month = line[2][3:5]
        day = line[2][0:2]
        hour = line[2][11:13]
        minute = line[2][14:16]
        
        if hour == "00" and minute == "00":
            if day == "01":
                if month in ["02", "04", "06", "09", "11"]:
                    day = "31"
                elif month == "03":
                    day = "28"
                else:
                    day = "30"
                
                if month == "01":
                    month = "12"
                    year = str(int(year) - 1)
                else:
                    month = str(int(month) - 1).zfill(2)
            else:
                day = str(int(day) - 1).zfill(2)
            line[2] = f"{day}-{month}-{year} 23:30"
        else:
            if minute == "00":
                minute = "30"
                hour = str(int(hour) - 1).zfill(2)
            else:
                minute = "00"
            line[2] = f"{day}-{month}-{year} {hour}:{minute}"


def filter_by_date(data, from_date, to_date):
    res = []
    from_date_obj = datetime.strptime(from_date, '%d-%m-%Y').date()
    to_date_obj = datetime.strptime(to_date, '%d-%m-%Y').date()

    if from_date_obj > to_date_obj:
        raise Exception("from date can't be later than to date")

    for reading in data:
        reading_date = datetime.strptime(reading[2], '%d-%m-%Y %H:%M').date()
        if reading_date >= from_date_obj and reading_date <= to_date_obj:
            res.append(reading)

    return res


def array_to_dict(data):
    res = {}
    for reading in data:
        reading_date = reading[2][:10]
        reading_time = reading[2][11:16]

        if reading_date not in res:
            res[reading_date] = {}
        res[reading_date][reading_time] = reading[0]

    return res

def array_to_dict_totals(data):
    res = {
        'day': 0,
        'night': 0,
        'peak': 0,
        'ev': 0
    }
    for reading in data:

        reading_date = reading[2][:10]
        reading_time = reading[2][11:16]
        reading_date_obj = datetime.strptime(reading_date, '%d-%m-%Y')
        reading_time_obj = datetime.strptime(reading_time, '%H:%M').time()
        weekday = reading_date_obj.weekday()
        isWeekday = True if (weekday != 0 and weekday != 6) else False # peak tariff is not applicable over the weekend

        if (reading_time_obj >= TIMES['DAY']['FROM'] and reading_time_obj < TIMES['PEAK']['FROM']) or (reading_time_obj >= TIMES['PEAK']['TO'] and reading_time_obj < TIMES['NIGHT']['FROM']):
            key = 'day'
        elif reading_time_obj >= TIMES['NIGHT']['FROM'] or reading_time_obj < TIMES['EV']['FROM'] or (reading_time_obj >= TIMES['EV']['TO'] and reading_time_obj < TIMES['DAY']['FROM']):
            key = 'night'
        elif reading_time_obj >= TIMES['PEAK']['FROM'] and reading_time_obj < TIMES['PEAK']['TO']:
            if isWeekday:
                key = 'peak'
            else:
                key = 'day'
        elif reading_time_obj >= TIMES['EV']['FROM'] and reading_time_obj < TIMES['EV']['TO']:
            key = 'ev'
        else:
            raise Exception(f"Time {reading_time} doesn't fall in any of the categories.")
        
        res[key] += Decimal(reading[0]).quantize(Decimal('0.001'))

            
    return res
        

def export_data_to_csv(data, totals):
    '''
    Export the data to a CSV file.
    '''
    today = datetime.strftime(date.today(), '%d-%m-%Y')
    dates = data.keys().__reversed__()
    # tariffs_string = "Night,,,,,EV,,,,,,,Night,,,,,,,Day,,,,,,,,,,,,,,,,,,,Peak,,,,,Day,,,,,,,,,Night,,"
    tariffs_string = "N,N,N,N,E,E,E,E,E,E,N,N,N,N,N,N,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,P,P,P,P,D,D,D,D,D,D,D,D,N,N"
    # times_string = "00:00,00:30,01:00,01:30,,02:00,02:30,03:00,03:30,04:00,04:30,,05:00,05:30,06:00,06:30,07:00,07:30,,08:00,08:30,09:00,09:30,10:00,10:30,11:00,11:30,12:00,12:30,13:00,13:30,14:00,14:30,15:00,15:30,16:00,16:30,,17:00,17:30,18:00,18:30,,19:00,19:30,20:00,20:30,21:00,21:30,22:00,22:30,,23:00,23:30"
    times_string = "00:00,00:30,01:00,01:30,02:00,02:30,03:00,03:30,04:00,04:30,05:00,05:30,06:00,06:30,07:00,07:30,08:00,08:30,09:00,09:30,10:00,10:30,11:00,11:30,12:00,12:30,13:00,13:30,14:00,14:30,15:00,15:30,16:00,16:30,17:00,17:30,18:00,18:30,19:00,19:30,20:00,20:30,21:00,21:30,22:00,22:30,23:00,23:30"
    times_array = times_string.split(',')
    with open(f'./exports/{today}.csv', 'w') as f:
        f.write(f",,{tariffs_string}\n")
        f.write(f",Date,{times_string}\n")
        for d in dates:
            date_obj = datetime.strptime(d, '%d-%m-%Y')
            weekday = date_obj.weekday()
            weekday_name = DAYS_OF_THE_WEEK[weekday]
            if weekday == 6:
                f.write("\n")
            f.write(f"{weekday_name[0]},{d}")
            for time in times_array:
                try:
                    f.write(f",{data[d][time]}")
                except:
                    f.write(",")
            if weekday == 0:
                f.write("\n")
            f.write("\n")
        f.write('\nTotals\n')
        f.write("Day,Night,Peak,EV\n")
        f.write(f"{totals['day']},{totals['night']},{totals['peak']},{totals['ev']}\n")

