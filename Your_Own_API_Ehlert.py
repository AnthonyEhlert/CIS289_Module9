"""
Program Name: Your_Own_API_Ehlert.py
Author: Tony Ehlert
Date: 10/19/2023

Program Description: This program creates an API that utilizes a static dataset and responds to simple REST calls with
up to two different parameters.
"""
import flask
import csv
import sqlite3

from flask import request, jsonify
from sqlite3 import Error

# create dictionary from .csv file containing employee data
with open('employee_sample_data.csv') as file:
    employee_data = [{key: value for key, value in row.items()}
                     for row in csv.DictReader(file, delimiter=',')]
# print(employee_data)

# create flask application object
app = flask.Flask(__name__)
app.config['DEBUG'] = True


def dict_factory(cursor, row):
    """
    This function is used for database returns.  It converts the list of tuples from the cursor into a dictionary
    :param cursor: Cursor object
    :param row: records
    :return: dictionary of records
    """
    dict = {}
    for idx, col in enumerate(cursor.description):
        dict[col[0]] = row[idx]
    return dict


# home page/route
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Employee Data</h1>
    <p>An API the returns data about employees</p1>'''


# route that returns all entries
@app.route('/api/v1/resources/employees/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('employee_info.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_employees = cur.execute('SELECT * FROM Employees').fetchall()

    return jsonify(all_employees)


# error handler page
@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404 Error</h1><p>The resource could not be found. Please verify that the URL is correct</p>', 404


# route that returns records that match parameters (if provided), else displays error
@app.route('/api/v1/resources/employees', methods=['GET'])
def api_params():
    query_params = request.args

    # create variables for parameters.
    id = query_params.get('id')
    full_name = query_params.get('full name')
    gender = query_params.get('gender')
    age = query_params.get('age')
    # job_title = query_params('job title')

    # create base SQL statement/query
    query = 'SELECT * FROM Employees WHERE'

    # create empty list to store filters for query
    to_filter = []

    # if statements to check for any provided parameters (COLLATE NOCASE included to have query ignore case)
    if id:
        query += ' id=? COLLATE NOCASE AND'
        to_filter.append(id)
    if full_name:
        query += ' full_name=? COLLATE NOCASE AND'
        to_filter.append(full_name)
    if age:
        query += ' age=? COLLATE NOCASE AND'
        to_filter.append(age)
    if gender:
        query += ' gender=? COLLATE NOCASE AND'
        to_filter.append(gender)
    if not (id or full_name or age or gender):
        return page_not_found(404)

    # remove last 4 characters from query variable and adds semicolon to complete SQL query -> ' AND'
    query = query[:-4] + ';'

    # connect to db
    conn = sqlite3.connect('employee_info.db')

    # convert tuples to dict
    conn.row_factory = dict_factory

    # create cursor
    cur = conn.cursor()

    # get results of SQL statement/query and store in variable
    results = cur.execute(query, to_filter).fetchall()

    # convert list to JSON using Flasks' jsonify function
    return jsonify(results)


def create_connection(db_file):
    """
    This function creates a database connection to a SQLite database if it doesn't already exist
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    This function creates a table from the create_table_sql statement provided
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        # create cursor object from conn
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


if __name__ == '__main__':
    # create db and table
    database = 'employee_info.db'
    sql_create_emp_info_tbl = """ CREATE TABLE IF NOT EXISTS Employees (
                                        id text PRIMARY KEY,
                                        full_name text NOT NULL,
                                        job_title text,
                                        gender text,
                                        age int
                                        );"""

    # create db connection if it doesn't exist
    conn = create_connection(database)

    # create table
    if conn is not None:
        create_table(conn, sql_create_emp_info_tbl)
    else:
        print("Error! Cannot create the database connection")

    # populate database with list tuples representing each record in .csv file
    with open('employee_sample_data.csv', 'r') as input_file:
        data = csv.DictReader(input_file)
        to_db = [(i['id'], i['full_name'], i['job_title'], i['gender'], i['age']) for i in data]

    conn = create_connection(database)
    cur = conn.cursor()

    cur.executemany("REPLACE INTO Employees (id, full_name, job_title, gender, age) VALUES (?,?,?,?,?);", to_db)
    conn.commit()
    conn.close()

    # run flask app object
    app.run(debug=True, use_reloader=False)
