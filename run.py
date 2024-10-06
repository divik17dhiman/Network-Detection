from app.database import initialize_database
from app.detector import start_detection
from app.reporter import create_app

if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Start the network attack detection
    start_detection()  # Starts the detection threads

    # Start the web server (Flask) for reporting
    app = create_app()
    app.run(debug=True)