import json


def get_daily_values(data_dict: dict, index: int) -> list:
    """
    Returns the set of data values at index.
    """
    return sorted(list({key[index]
                        for data in data_dict.values()
                        for key in data.keys() if key[index]}))


def get_time_series_values(data_dict: dict, index: int) -> list:
    """
    Returns the set of data values at index.
    """
    return sorted(list({key[index] for key in data_dict.keys() if key[index]}))


def get_time_series_dates(data_dict: dict) -> list:
    """
    Returns the list of dates in the current time series dictionary.
    """
    if not data_dict:
        return []
    else:
        for data in data_dict.values():
            return list(data['data'].keys())


def _convert_time_to_csv(results: dict, dates: list) -> str:
    """
    Converts time series results to a csv format.
    """
    csv_header = ['place'] + dates
    csv_values = [','.join(csv_header)]
    for place, data in results.items():
        entry = [place]
        for key in dates:
            entry.append(str(data[key]))
        csv_values.append(','.join(entry))
    final_csv = '\n'.join(csv_values)
    return f'<pre>{final_csv}</pre>'


def _convert_time_to_string(results: dict, dates: list) -> str:
    """
    Converts time series results to a string format.
    """
    output = ""
    for place, data in results.items():
        output += "Location: " + place + "<br>"
        for key in dates:
            output += "&emsp;Date: " + key + ": " + str(data[key]) + "<br>"
    return output


def execute_time_query(data: dict, states: list, countries: list, dates: list,
                       ret_type: list) -> str:
    """
    Returns the query result of a time series data query.
    """
    result = {}
    for key, values in data.items():
        state, country = key
        key = '|'.join([state, country]).strip('|')
        state_match = state in states or not states
        country_match = country in countries or not countries
        if state_match and country_match:
            result[key] = {}
            for date, number in values['data'].items():
                if not dates or date in dates:
                    result[key][date] = number
        if not dates:
            dates = list(result[key].keys())
    if not ret_type or '0' in ret_type:
        return json.dumps(result)
    elif '1' in ret_type:
        return _convert_time_to_csv(result, dates)
    else:
        return _convert_time_to_string(result, dates)


def _convert_daily_to_csv(results: dict) -> str:
    """
    Converts daily query results to a csv format.
    """
    csv_values = ['date,place,deaths,confirmed,active,recovered']
    for d, val in results.items():
        for key, numbers in val.items():
            entry = [d, key]
            for stat in ['deaths', 'confirmed', 'active', 'recovered']:
                if stat in numbers:
                    entry.append(str(numbers[stat]))
                else:
                    entry.append('-')
            csv_values.append(','.join(entry))
    final_csv = '\n'.join(csv_values)
    return f'<pre>{final_csv}</pre>'


def _convert_daily_to_string(results: dict) -> str:
    """
    Converts daily query results to a string format.
    """
    output = ""
    for d, val in results.items():
        output += "Date: " + d + "<br>"
        for key, numbers in val.items():
            output += "&emsp;Location: " + key + "<br>"
            for stat in ['deaths', 'confirmed', 'active', 'recovered']:
                if stat in numbers:
                    output += "&emsp;&emsp;" + str(numbers[stat]) + " " + stat + "<br>"
    return output


def execute_daily_query(data: dict, counties: list, states: list,
                        countries: list, dates: list, fields: list,
                        ret_type: list) -> str:
    """
    Returns the query result of a daily data query.
    """
    result = {}
    if not fields:
        fields = ['0', '1', '2', '3']
    for d, val in data.items():
        if not dates or d in dates:
            result[d] = {}
            for key, numbers in val.items():
                county, state, country = key
                key = '|'.join([county, state, country]).strip('|')
                county_match = county in counties or not counties
                state_match = state in states or not states
                country_match = country in countries or not countries
                if county_match and state_match and country_match:
                    result[d][key] = {}
                    death, confirmed, active, recovered = numbers
                    if '0' in fields:
                        result[d][key]['deaths'] = death
                    if '1' in fields:
                        result[d][key]['confirmed'] = confirmed
                    if '2' in fields:
                        result[d][key]['active'] = active
                    if '3' in fields:
                        result[d][key]['recovered'] = recovered
    if not ret_type or '0' in ret_type:
        return json.dumps(result)
    elif '1' in ret_type:
        return _convert_daily_to_csv(result)
    else:
        return _convert_daily_to_string(result)
