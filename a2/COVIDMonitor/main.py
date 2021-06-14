import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd() + os.sep + 'data'
ALLOWED_EXTENSIONS = {'csv'}
PROJECT_ROOT = os.path.dirname(__file__)

if __name__ == '__main__':
    import parsing_utils
    import query_utils

    app = Flask("Assignment 2", template_folder='./templates')
else:
    import COVIDMonitor.parsing_utils as parsing_utils
    import COVIDMonitor.query_utils as query_utils

    app = Flask("Assignment 2", template_folder=PROJECT_ROOT + os.sep + 'templates')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret'

curr_time_series = {}
curr_daily_reports = {}


@app.route('/load_sample')
def load_sample_data():
    try:
        global curr_time_series
        curr_time_series = parsing_utils.parse_time_series(
            os.getcwd() + os.sep + 'data' + os.sep + 'time_series_sample.csv')
        curr_daily_reports['sample-data'] = parsing_utils.parse_daily_report(
            os.getcwd() + os.sep + 'data' + os.sep + 'daily_report_sample.csv')
    except FileNotFoundError:
        pass
    return redirect('/')


@app.route('/delete')
def delete_data():
    curr_time_series.clear()
    curr_daily_reports.clear()
    return redirect('/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # set daily reports
            if parsing_utils.is_valid_time_series(filepath):
                global curr_time_series
                curr_time_series = parsing_utils.parse_time_series(filepath)
                return render_template('upload_result.html',
                                       data='Time series upload success.', color='limegreen')
            elif parsing_utils.is_valid_daily_report(filepath):
                report_date = parsing_utils.get_date_from_filename(filename)
                curr_daily_reports[report_date] = parsing_utils.parse_daily_report(filepath)
                return render_template('upload_result.html',
                                       data='Daily report upload success.', color='limegreen')
            else:
                return render_template('upload_result.html',
                                       data='Upload failed, file format is not correct.', color='red')
    return render_template('upload.html')


@app.route('/daily', methods=['GET', 'POST'])
def query_daily():
    if request.method == 'POST':
        return query_utils.execute_daily_query(curr_daily_reports,
                                               request.form.getlist('countys'),
                                               request.form.getlist('states'),
                                               request.form.getlist('countries'),
                                               request.form.getlist('dates'),
                                               request.form.getlist('fields'),
                                               request.form.getlist('return_type'))
    return render_template('daily_query.html',
                           countys=query_utils.get_daily_values(curr_daily_reports, 0),
                           states=query_utils.get_daily_values(curr_daily_reports, 1),
                           countries=query_utils.get_daily_values(curr_daily_reports, 2),
                           dates=curr_daily_reports.keys())


@app.route('/time', methods=['GET', 'POST'])
def query_time():
    if request.method == 'POST':
        return query_utils.execute_time_query(curr_time_series,
                                              request.form.getlist('states'),
                                              request.form.getlist('countries'),
                                              request.form.getlist('dates'),
                                              request.form.getlist('return_type'))
    return render_template('time_query.html',
                           states=query_utils.get_time_series_values(curr_time_series, 0),
                           countries=query_utils.get_time_series_values(curr_time_series, 1),
                           dates=query_utils.get_time_series_dates(curr_time_series))


if __name__ == "__main__":
    app.run()
