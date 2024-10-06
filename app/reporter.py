from flask import Flask, render_template, jsonify, request
import sqlite3
from app.database import reset_database

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/incidents')
    def incidents():
        conn = sqlite3.connect("incidents.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
        incidents = cursor.fetchall()
        conn.close()
        return jsonify(incidents)

    @app.route('/reset', methods=['POST'])
    def reset():
        reset_database()  # Clear all records in the incidents table
        return '', 204  # No content response

    return app
