from app.database import initialize_database
from app.detector import start_detection
from app.reporter import create_app

if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Start the network attack detection (this runs the ARP and DDoS detection)
    start_detection()

    # Start the web server (Flask) for reporting
    app = create_app()
    app.run(debug=True)
