import sqlite3
from flask import Flask, render_template, jsonify
from werkzeug.exceptions import abort
from flask import request
import simplejson as json


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def search_complex():
    conn = get_db_connection()
    all_complex = conn.execute('SELECT * FROM complex').fetchall()
    conn.close()
    if complex is None:
        abort(404)
    return all_complex


def get_complex(complex_id):
    conn = get_db_connection()
    complex = conn.execute(
        'SELECT * FROM complex INNER JOIN complex_review ON complex.id = complex_review.complex_id INNER JOIN company ON company.company_id = complex.company WHERE complex.id = ?',
        (complex_id,)).fetchone()
    conn.close()
    if complex is None:
        abort(404)
    return complex


def get_company(company_id):
    conn = get_db_connection()
    company = conn.execute(
        'SELECT * FROM company INNER JOIN company_review ON company.company_id = company_review.company_id INNER JOIN complex ON complex.company = company.company_id WHERE company.company_id = ?',
        (company_id,)).fetchone()
    conn.close()
    if company is None:
        abort(404)
    return company


def get_complex_for_company(company_id):
    conn = get_db_connection()
    complex_list = conn.execute(
        'SELECT * FROM complex INNER JOIN company ON complex.company = company.company_id WHERE company.company_id = ?',
        (company_id,)).fetchall()
    conn.close()
    if complex_list is None:
        abort(404)
    return complex_list


def getusers(search):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complex WHERE title LIKE ?", ("%" + search + "%",))
    results = cursor.fetchall()
    conn.close()
    return results


def getcompany(search):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company WHERE name LIKE ?", ("%" + search + "%",))
    results = cursor.fetchall()
    conn.close()
    return results


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/complex_search', methods=["GET", "POST"])
def complex_search():
    if request.method == "POST":
        data = dict(request.form)
        complex = getusers(data["search"])
    else:
        conn = get_db_connection()
        complex = conn.execute('SELECT * FROM complex').fetchall()
        conn.close()
    return render_template('complex_search.html', complexes=complex)


@app.route('/company_search', methods=["GET", "POST"])
def company_search():
    if request.method == "POST":
        data = dict(request.form)
        company = getcompany(data["search"])
    else:
        conn = get_db_connection()
        company = conn.execute('SELECT * FROM company').fetchall()
        conn.close()
    return render_template('company_search.html', companies=company)


@app.route('/complex/<int:complex_id>')
def complex(complex_id):
    complex = get_complex(complex_id)

    return render_template('post.html', complex=complex)


@app.route('/company/<int:company_id>')
def company(company_id):
    company = get_company(company_id)
    complex_list = get_complex_for_company(company_id)
    return render_template('company.html', company=company, complex_list=complex_list)
