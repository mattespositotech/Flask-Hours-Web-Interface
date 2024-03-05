from flask import Flask, render_template, request, redirect, url_for, abort
from sqlite.db_manager import get_all_data_from_this_month, insert_into_db, delete_from_db, get_hours_by_date, update_hours, get_all_data, upsert_hours, get_data_adjusted_from_current_month, get_all_future_data
from errors import handle_error
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = get_all_data_from_this_month()
    month_name = None
    if data:
        date_str = data[0]['date']
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month_name = date.strftime("%B")

    return render_template('main.html', data=data, month_name=month_name, month=0, disable='')

@app.route("/table")
def table():
    data = get_all_data_from_this_month()
    if data:
        date_str = data[0]['date']
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month_name = date.strftime("%B")
        
    return render_template('main.html', data=data, month_name=month_name, month=0, disable='')

@app.route("/table/all")
def table_all():
    data = get_all_data()
    return render_template('main.html', data=data)

@app.route('/table/prev/<string:month>')
def table_prev(month):
    prev_month = int(month) - 1
    data = get_data_adjusted_from_current_month(prev_month)
    disable = ''
    if data:
        date_str = data[0]['date']
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month_name = date.strftime("%B")
    else:
        month_name = 'No More Data'
        disable = 'prev'
        
    return render_template('main.html', data=data, month_name=month_name, month=prev_month, disable=disable)
    
@app.route('/table/next/<string:month>')
def table_next(month):
    next_month = int(month) + 1
    data = get_data_adjusted_from_current_month(next_month)
    disable = ''
    if data:
        date_str = data[0]['date']
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month_name = date.strftime("%B")
    else:
        data = get_all_future_data()
        month_name = 'All Future Data'
        disable = 'next'
    return render_template('main.html', data=data, month_name=month_name, month=next_month, disable=disable)

@app.route('/form/today')
def add_today():
    route='/add_data'
    return render_template('form.html', route=route)

@app.route('/form/pick')
def add_pick():
    route='/add_pick'
    return render_template('pickedform.html', route=route)

@app.route('/add_data', methods=['POST'])
def add_hours():
    formData = {
        'new_dev': request.form.get('new_dev', 0, type=int),
        'old_dev': request.form.get('old_dev', 0, type=int),
        'analytics': request.form.get('analytics', 0, type=int),
        'other': request.form.get('other', 0, type=int)
    }

    error_code = insert_into_db(formData)

    handle_error(error_code)

    return redirect(url_for('table'))

@app.route('/add_pick', methods=['POST'])
def add_hours_pick():
    formData = {
        'new_dev': request.form.get('new_dev', 0, type=int),
        'old_dev': request.form.get('old_dev', 0, type=int),
        'analytics': request.form.get('analytics', 0, type=int),
        'other': request.form.get('other', 0, type=int),
        'date': request.form.get('date')
    }

    print(formData)

    error_code = upsert_hours(formData)

    handle_error(error_code)

    return redirect(url_for('table'))

@app.route('/<string:date>/edit', methods=('GET', 'POST'))
def edit_hours(date):
    hours_by_date = get_hours_by_date(date)

    if hours_by_date is None:
        abort(404)
    
    if request.method == 'POST':
        formData = {
            'new_dev': request.form.get('new_dev', 0, type=int),
            'old_dev': request.form.get('old_dev', 0, type=int),
            'analytics': request.form.get('analytics', 0, type=int),
            'other': request.form.get('other', 0, type=int),
            'date': date
        }

        error_code = update_hours(formData)
        handle_error(error_code)

        return redirect(url_for('table'))
    
    route = url_for('edit_hours', date=date)
    print(route)

    return render_template('form.html', route=route, date=date, hours=hours_by_date)

@app.route('/<string:date>/delete', methods=['POST'])
def delete(date):
    print(date)

    delete_from_db(date)

    return redirect(url_for('table'))