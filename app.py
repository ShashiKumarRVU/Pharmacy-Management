from flask import Flask, render_template, request, redirect, url_for
from pyshorteners import Shortener
import sqlite3
from datetime import datetime

app = Flask(__name__)

def initialize_database():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, original TEXT, shortened TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def shorten_url(url):
    x = Shortener()
    y = x.tinyurl
    z = y.short(url)
    return z

def add_to_database(name, original, shortened):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO urls (name, original, shortened, date) VALUES (?, ?, ?, ?)", (name, original, shortened, date))
    conn.commit()
    conn.close()

def delete_from_database(id):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("DELETE FROM urls WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_all_urls():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT * FROM urls ORDER BY id DESC")
    urls = c.fetchall()
    conn.close()
    return urls

def search_urls(query):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT * FROM urls WHERE name LIKE ?", ('%' + query + '%',))
    urls = c.fetchall()
    conn.close()
    return urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'search_query' in request.form:
            search_query = request.form.get('search_query')
            if search_query:
                search_result = search_urls(search_query)
                return render_template('index.html', shortened_urls=search_result)
        else:
            name = request.form.get('name')
            urls = request.form.get('urls').splitlines()
            shortened_urls = []
            for url in urls:
                shortened_url = shorten_url(url)
                shortened_urls.append({"original": url, "short": shortened_url})
                add_to_database(name, url, shortened_url)
            return render_template('index.html', shortened_urls=get_all_urls())
    else:
        initialize_database()
        return render_template('index.html', shortened_urls=get_all_urls())


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_from_database(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
