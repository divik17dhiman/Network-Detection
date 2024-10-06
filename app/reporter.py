from flask import Flask, render_template, redirect, url_for
import sqlite3
from app.database import reset_database


# Global flag to track if detection is running
detection_running = False

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
    

    @app.route('/reset')
    def reset_db():
        reset_database()
        return redirect(url_for('index'))
    

    return app
