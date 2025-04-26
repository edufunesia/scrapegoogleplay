import pandas as pd
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from google_play_scraper import reviews

app = Flask(__name__)

INFO_CSV_PATH = 'BankDigital/dataset/info_BANK_MOBILE_GOOGLE_PLAY_Update21092024.csv'
REVIEWS_CSV_PATH = 'BankDigital/dataset/reviews_BANK_MOBILE_GOOGLE_PLAY_Update21092024.csv'

# Home route - display the form for app ID
@app.route("/")
def index():
    """Renders the index page with the app ID form."""
    return render_template("index.html")

# Route to fetch and display reviews based on app ID
@app.route("/fetch-reviews", methods=["POST"])
def fetch_reviews():
    """Fetches and displays reviews for a given app ID."""
    app_id = request.form.get('app_id')
    if not app_id:
        # Redirect back to index or show an error if app_id is missing
        return redirect(url_for('index'))

    fetched_reviews = []
    try:
        # Fetch reviews using google-play-scraper
        # Note: This fetches a limited number of reviews by default.
        # You might need to implement pagination or specify count for more reviews.
        fetched_reviews, _ = reviews(
            app_id,
            lang='en', # Language
            country='us', # Country
            sort='relevancy', # Sort order (newest, helpfulness, relevancy)
            count=100 # Number of reviews to fetch (max 100 per request)
        )
    except Exception as e:
        print(f"Error fetching reviews for {app_id}: {e}")
        # Optionally, add an error message to the template context
        pass # Continue with empty data

    # Render the reviews template with the fetched data
    # We convert the fetched reviews (which are dictionaries) to a list of dictionaries
    # to match the expected format in reviews.html
    reviews_data = fetched_reviews

    return render_template("reviews.html", reviews_data=reviews_data)

# Existing Reviews route - display app reviews from the local CSV (can be kept or removed)
# I'll keep it for now, but you might want to consolidate review display through /fetch-reviews
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
