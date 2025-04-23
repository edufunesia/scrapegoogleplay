import pandas as pd
from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

INFO_CSV_PATH = 'BankDigital/dataset/info_BANK_MOBILE_GOOGLE_PLAY_Update21092024.csv'
REVIEWS_CSV_PATH = 'BankDigital/dataset/reviews_BANK_MOBILE_GOOGLE_PLAY_Update21092024.csv'

# Home route - display app information
@app.route("/")
def index():
    """Renders the index page with app information from CSV."""
    app_data = []
    if os.path.exists(INFO_CSV_PATH):
        try:
            df = pd.read_csv(INFO_CSV_PATH)
            app_data = df.to_dict("records")
        except Exception as e:
            print(f"Error reading {INFO_CSV_PATH}: {e}")
            # Optionally, add an error message to the template context
            pass # Continue with empty data

    # Ensure app_data is a list, even if empty or on error, to prevent template errors
    if not app_data:
         # Provide a minimal structure if no data to prevent template errors with .keys()
         # This assumes some expected columns; adjust as per your CSV structure if needed
         # Or handle this case in the template with an if condition
         # For simplicity here, we'll just pass the empty list and assume template handles it
         pass # app_data is already []

    return render_template("index.html", app_data=app_data)

# Reviews route - display app reviews
@app.route("/reviews")
def reviews_page():
    """Renders the reviews page with reviews from CSV."""
    reviews_data = []
    if os.path.exists(REVIEWS_CSV_PATH):
        try:
            df = pd.read_csv(REVIEWS_CSV_PATH)
            # Convert timestamp to datetime objects if needed for display
            # df['at'] = pd.to_datetime(df['at'])
            reviews_data = df.to_dict("records")
        except Exception as e:
             print(f"Error reading {REVIEWS_CSV_PATH}: {e}")
             # Optionally, add an error message to the template context
             pass # Continue with empty data

    # Ensure reviews_data is a list, even if empty or on error
    if not reviews_data:
        pass # reviews_data is already []

    return render_template("reviews.html", reviews_data=reviews_data)

# Export app info CSV
@app.route("/export/info")
def export_info_csv():
    """Exports the app information CSV file."""
    if os.path.exists(INFO_CSV_PATH):
        try:
            return send_file(INFO_CSV_PATH, as_attachment=True)
        except Exception as e:
            print(f"Error sending {INFO_CSV_PATH}: {e}")
            return "Error exporting file.", 500
    else:
        return "App info CSV not found. Please run the scraping script first.", 404

# Export reviews CSV
@app.route("/export/reviews")
def export_reviews_csv():
    """Exports the app reviews CSV file."""
    if os.path.exists(REVIEWS_CSV_PATH):
        try:
            return send_file(REVIEWS_CSV_PATH, as_attachment=True)
        except Exception as e:
            print(f"Error sending {REVIEWS_CSV_PATH}: {e}")
            return "Error exporting file.", 500
    else:
        return "Reviews CSV not found. Please run the scraping script first.", 404

if __name__ == "__main__":
    # In a production environment, you would not run with debug=True
    # and likely use a production-ready WSGI server like Gunicorn or uWSGI
    app.run(debug=True)
