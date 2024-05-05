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
    complex = conn.execute('SELECT * FROM complex INNER JOIN complex_review ON complex.id = complex_review.complex_id INNER JOIN company ON company.company_id = complex.company WHERE complex.id = ?',
                           (complex_id,)).fetchone()
    conn.close()
    if complex is None:
        abort(404)
    return complex


def get_company(company_id):
    conn = get_db_connection()
    company = conn.execute('SELECT * FROM company INNER JOIN company_review ON company.company_id = company_review.company_id WHERE company.company_id = ?',
                           (company_id,)).fetchone()
    conn.close()
    if company is None:
        abort(404)
    return company


app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/complex_search')
def complex_search():
    conn = get_db_connection()
    complex = conn.execute('SELECT * FROM complex').fetchall()
    conn.close()
    return render_template('complex_search.html', complexes=complex)


@app.route('/company_search')
def company_search():
    conn = get_db_connection()
    company = conn.execute('SELECT * FROM company').fetchall()
    conn.close()
    return render_template('company_search.html', companies=company)


# @app.route("/livesearch", methods=["POST", "GET"])
# def livesearch():
#     searchbox = request.form.get("text")
#     conn = get_db_connection()
#     query = "SELECT title FROM complex where title LIKE '{}%' order by title".format(searchbox)
#     results = conn.execute(query).fetchall()
#     results = [tuple(row) for row in results]
#     json_string = json.dumps(results)
#     return jsonify(json_string)


@app.route('/complex/<int:complex_id>')
def complex(complex_id):
    complex = get_complex(complex_id)
    return render_template('post.html', complex=complex)


@app.route('/company/<int:company_id>')
def company(company_id):
    company = get_company(company_id)
    return render_template('company.html', company=company)
