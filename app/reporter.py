from flask import Flask, render_template, redirect, url_for
import sqlite3

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        conn = sqlite3.connect("incidents.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents")
        incidents = cursor.fetchall()
        conn.close()
        return render_template("index.html", incidents=incidents)
    
    @app.route('/clear')
    def clear_db():
        conn = sqlite3.connect("incidents.db")
        cursor = conn.cursor()
        # Delete all records from the incidents table
        cursor.execute("DELETE FROM incidents")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return app
