import os
import re
from utils import read_file, remove_unused_data, fix_intervals, filter_by_date, array_to_dict, array_to_dict_usage_totals, export_data_to_csv, get_cost_totals, get_number_of_days

date_pattern = r'^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-(20\d{2})$'

try:
    data = read_file(os.environ.get('MPRN'))
    cleaned_data = remove_unused_data(data)
    fix_intervals(cleaned_data)

    filter_date = input("Do you wish to filter the data by date (y/n)?\t")
    if filter_date.lower() == 'y':
        from_date = input("From date (dd-mm-yyyy):\t")
        from_date = from_date.replace('/', '-')
        while not re.match(date_pattern, from_date):
            from_date = input("Incorrect date/format. From date (dd-mm-yyyy):\t")
        to_date = input("To date (dd-mm-yyyy):\t")
        to_date = to_date.replace('/', '-')
        while not re.match(date_pattern, to_date):
            to_date = input("Incorrect date/format. To date (dd-mm-yyyy):\t")
    
        filtered_by_date_data = filter_by_date(cleaned_data, from_date, to_date)
    
    else:
        filtered_by_date_data = cleaned_data
        
    dict = array_to_dict(filtered_by_date_data)
    number_of_days = get_number_of_days(filtered_by_date_data)
    usage_totals = array_to_dict_usage_totals(filtered_by_date_data)
    cost_totals = get_cost_totals(usage_totals)
    export_data_to_csv(dict, usage_totals, cost_totals, number_of_days)
    


except Exception as e:
    print(e)