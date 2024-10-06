from flask import Flask, render_template, redirect, url_for
import sqlite3
from app.database import reset_database


# Global flag to track if detection is running
detection_running = False

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/get_incidents')
    def get_incidents():
        conn = sqlite3.connect("incidents.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents")
        incidents = cursor.fetchall()
        conn.close()

        # Prepare the data in JSON format
        incident_list = []
        for incident in incidents:
            incident_list.append({
                "id": incident[0],
                "type": incident[1],
                "details": incident[2],
                "timestamp": incident[3]
            })

        return jsonify(incidents=incident_list)
    

    @app.route('/reset_db')
    def reset_db():
        conn = sqlite3.connect("incidents.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM incidents")  # This will remove all records
        conn.commit()
        conn.close()
        return jsonify(message="Database has been reset successfully.")
    

    return app
