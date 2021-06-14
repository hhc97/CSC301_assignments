"""
Utilities for parsing COVID related csv files.
"""

import re
import csv
from datetime import datetime, date


def convert_to_date(date_string: str) -> date:
    """
    Converts time series info into a date object.
    """
    return datetime.strptime(date_string, '%m/%d/%y').date()


def get_date_from_filename(filename: str) -> str:
    """
    Returns the date from a filename.
    """
    timestamp = re.search(r'\d{2}-\d{2}-\d{4}', filename)
    if timestamp is None:
        return 'no-date'
    return timestamp.group()


def is_valid_time_series(path: str) -> bool:
    """
    Returns whether the given filepath is valid time series data.
    """
    keys = set()
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        header_length = len(header)
        # check that there are enough fields
        if header_length < 5:
            return False
        _, _, _, _, *dates = header
        for d in dates:
            try:
                convert_to_date(d)
            except ValueError:
                return False
        for line in reader:
            # check each line is the same length
            if len(line) != header_length:
                return False
            province, country, long, lat, *data = line
            # check that data points are unique
            key = province, country
            if key in keys:
                return False
            else:
                keys.add(key)
            # check that data is consistent and represents numbers
            for point in data:
                try:
                    int(point)
                except ValueError:
                    return False
    return True


def parse_time_series(path: str) -> dict:
    """
    Returns a dictionary of parsed time series data.
    """
    results = {}
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        _, _, _, _, *dates = next(reader)
        for line in reader:
            province, country, long, lat, *data = line
            key = province, country
            results[key] = {'long': long, 'lat': lat, 'data': {}}
            for day, numbers in zip(dates, data):
                results[key]['data'][day] = int(numbers)
    return results


def get_data_indexes(header: list) -> list:
    """
    Gets the data indexes of relevant columns in the header.
    """
    required = ['Admin2', 'Province_State', 'Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']
    return [header.index(item) for item in required]


def is_valid_daily_report(path: str) -> bool:
    """
    Returns whether the given filepath is valid daily report data.
    """
    keys = set()
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        try:
            indexes = get_data_indexes(header)
        except ValueError:
            return False
        header_length = len(header)
        for line in reader:
            # check each line is the same length
            if len(line) != header_length:
                return False
            county, state, country, confirmed, deaths, recovered, active = [line[i] for i in indexes]
            # check that data points are unique
            key = county, state, country
            if key in keys:
                return False
            else:
                keys.add(key)
            # check that data is consistent and represents numbers
            for stat in [confirmed, deaths, recovered, active]:
                try:
                    if stat:
                        int(stat)
                except ValueError:
                    return False
    return True


def parse_daily_report(path: str) -> dict:
    """
    Returns a dictionary of parsed daily report data.
    """
    results = {}
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        indexes = get_data_indexes(next(reader))
        for line in reader:
            county, state, country, confirmed, deaths, recovered, active = [line[i] for i in indexes]
            key = county, state, country
            if not confirmed:
                confirmed = 0
            if not deaths:
                deaths = 0
            if not recovered:
                recovered = 0
            if not active:
                active = 0
            results[key] = int(confirmed), int(deaths), int(recovered), int(active)
    return results


if __name__ == '__main__':
    pass
