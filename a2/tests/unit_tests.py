import os

from COVIDMonitor.main import app
from COVIDMonitor.parsing_utils import get_date_from_filename
from COVIDMonitor.parsing_utils import is_valid_time_series, is_valid_daily_report
from COVIDMonitor.parsing_utils import parse_time_series, parse_daily_report
import COVIDMonitor.db_utils as db_utils
import COVIDMonitor.query_utils as query_utils


def test_upload_form():
    response = app.test_client().post('/')
    assert response.status_code == 302


def test_daily_query():
    response = app.test_client().get('/daily')

    assert response.status_code == 200


def test_time_query():
    response = app.test_client().get('/time')

    assert response.status_code == 200


def test_delete_data():
    response = app.test_client().get('/delete')

    assert response.status_code == 302


def test_upload_sample():
    response = app.test_client().get('/load_sample')

    assert response.status_code == 302


def test_get_time_series_values():
    assert query_utils.get_time_series_values({(1,): 2}, 0) == [1]


def test_get_time_series_dates_empty():
    assert query_utils.get_time_series_dates({}) == []


def test_time_query_json():
    data = {('a', 'b'): {'data': {'1/22/20': 0, '1/23/20': 0}}}
    result = query_utils.execute_time_query(data, [], [], [], [])
    correct = '{"a|b": {"1/22/20": 0, "1/23/20": 0}}'
    assert result == correct


def test_time_query_csv():
    data = {('a', 'b'): {'data': {'1/22/20': 0, '1/23/20': 0}}}
    result = query_utils.execute_time_query(data, [], [], [], ['1'])
    correct = '<pre>place,1/22/20,1/23/20\n' \
              'a|b,0,0</pre>'
    assert result == correct


def test_time_query_text():
    data = {('a', 'b'): {'data': {'1/22/20': 0, '1/23/20': 0}}}
    result = query_utils.execute_time_query(data, [], [], [], ['2'])
    assert result == 'Location: a|b<br>&emsp;Date: 1/22/20: 0<br>&emsp;Date: 1/23/20: 0<br>'


def test_query_utils_get_daily():
    assert query_utils.get_daily_values({'date': {('a', 'b', 'c'): 'test'}}, 0) == ['a']


def test_daily_query_execute_json():
    data = {'test': {('Abbeville', 'South Carolina', 'US'): (47, 0, 0, 47)}}
    result = query_utils.execute_daily_query(data, [], [], [], [], [], [])
    correct = '{"test": {"Abbeville|South Carolina|US": ' \
              '{"deaths": 47, "confirmed": 0, "active": 0, "recovered": 47}}}'
    assert result == correct


def test_daily_query_execute_csv():
    data = {'test': {('Abbeville', 'South Carolina', 'US'): (47, 0, 0, 47)}}
    result = query_utils.execute_daily_query(data, [], [], [], [], [], ['1'])
    assert result == '<pre>date,place,deaths,confirmed,active,recovered\n' \
                     'test,Abbeville|South Carolina|US,47,0,0,47</pre>'


def test_daily_query_execute_text():
    data = {'test': {('Abbeville', 'South Carolina', 'US'): (47, 0, 0, 47)}}
    result = query_utils.execute_daily_query(data, [], [], [], [], [], ['2'])
    assert result == 'Date: test<br>&emsp;Location: Abbeville|South Carolina|US<br>' \
                     '&emsp;&emsp;47 deaths<br>&emsp;&emsp;0 confirmed<br>&emsp;&emsp;' \
                     '0 active<br>&emsp;&emsp;47 recovered<br>'


def test_filename_valid_date():
    assert get_date_from_filename('03-15-2021.csv') == '03-15-2021'


def test_filename_invalid_date1():
    assert get_date_from_filename('03-15-202.csv') == 'no-date'


def test_valid_time_series():
    assert is_valid_time_series('COVIDMonitor/data/time_series_sample.csv')


def test_invalid_time_series():
    assert not is_valid_time_series('COVIDMonitor/data/daily_report_sample.csv')


def test_valid_daily_report():
    assert is_valid_daily_report('COVIDMonitor/data/daily_report_sample.csv')


def test_invalid_daily_report():
    assert not is_valid_daily_report('COVIDMonitor/data/time_series_sample.csv')


def test_parse_time():
    result = parse_time_series('COVIDMonitor/data/time_series_sample.csv')
    assert len(result) == 274


def test_parse_daily():
    result = parse_daily_report('COVIDMonitor/data/daily_report_sample.csv')
    assert len(result) == 3672


def test_db():
    test_db_name = 'testdb.db'
    conn, curs = db_utils.get_conn(test_db_name)
    assert os.path.exists(test_db_name)
    db_utils.close_conn(conn)
    db_utils.drop_database(test_db_name)
    assert not os.path.exists(test_db_name)
