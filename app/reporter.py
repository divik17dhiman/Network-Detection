from flask import Flask, render_template
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

    return app
