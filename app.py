# Description: This program allows users to select a genre of movie
# and see its average ratings throughout the years. The user is able to select a year
# and see its predicted rating using sklearn.

import datetime
import io
import os
from flask import Flask, redirect, render_template, request, session, url_for, send_file
from matplotlib.figure import Figure
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(12)

movies_df = pd.read_csv("csv/movies.csv")
ratings_df = pd.read_csv("csv/ratings.csv")


# Linear Regression Model
def train_model():
    """
    Description: trains linear regression model to predict average movie ratings each year
    Parameters: 0
    Returns: 1
        i. the LinearRegression model
    """
    ratings_df['date'] = ratings_df['timestamp'].apply(lambda ts: datetime.datetime.utcfromtimestamp(ts))
    ratings_df['year'] = ratings_df['date'].dt.year

    # Group by year and calculate average ratings
    avg_ratings = ratings_df.groupby('year')['rating'].mean().reset_index()

    # Train the Linear Regression model
    model = LinearRegression()
    X = avg_ratings['year'].values.reshape(-1, 1)
    y = avg_ratings['rating'].values
    model.fit(X, y)
    return model

model = train_model()

def get_genres():
    """
    Description: get genres from movies
    Parameters: 0
    Returns: 1
        i. All the genres available (list)
    """
    unique_genres = set()
    for g_list in movies_df['genres'].fillna(''):
        for g in g_list.split('|'):
            if g.strip():
                unique_genres.add(g.strip())
    return sorted(unique_genres)

def get_years_for_genre(genre):
    """
    Description: get the years for each genre where there is a rating
    Parameters: 1
        i. genre (str)
    Returns: 1
        i. A sorted list of unique years (list)
    """
    genre_mask = movies_df['genres'].str.contains(genre, case=False, na=False)
    genre_movies = movies_df[genre_mask]
    merged = ratings_df.merge(genre_movies, on='movieId', how='inner')
    merged['date'] = merged['timestamp'].apply(lambda ts: datetime.datetime.utcfromtimestamp(ts))
    years = sorted(merged['date'].dt.year.unique())
    return years

# Web App 1: Flask shall be used to create the web framework routing using endpoints and associated
# view functions.
# Flask is used for routing (@app.route)

# Functionality and UI 1: The root endpoint shall display an input section for client-supplied data.
# The root endpoint allows the user to select a genre from the dropdown menu to display its average rating.
@app.route("/")
def home():
    """
    Description: renders the home.html
    Parameters: 0
    Returns: 1
        i. Rendered template home.html
    """
    return render_template("home.html",
                           genres=get_genres(),
                           message="Please select a genre to display its average ratings each year.")

@app.route("/submit_genre", methods=["POST"])
def submit_genre():
    """
    Description: user submits genre and redirects to the genre w/ graph
    Parameters: 0
    Returns: 1
        i. Redirect to page of genre selected
    """
    session["genre"] = request.form.get("genre", "")
    if 'genre' not in session or session["genre"] == "":
        return redirect(url_for("home"))
    return redirect(url_for("genre_ratings", genre=session["genre"]))

@app.route("/genre/<genre>")
def genre_ratings(genre):
    """
    Description: display average ratings for the selected genre across all years available
    Parameters: 1
        i. genre (str)
    Returns: 1
        i. Rendered template ratings.html
    """
    years = get_years_for_genre(genre)
    return render_template("ratings.html", genre=genre, start_year=None, end_year=None, project=False, years=years)

# Functionality and UI 2: Clients shall be able to select a query of existing data
# Users can pick the start and end year of the existing data they want to see

# Functionality and UI 2: or a prediction based on existing data
# Users can pick a year they want to predict the rating for a specific genre

# Functionality and UI 3: Clients shall be able to submit query information, which will generate a POST request.
# /submit_year_range and /predict will submit the user's query using POST request
@app.route("/submit_year_range", methods=["POST"])
def submit_year_range():
    """
    Description: lets user select specific start, end, and prediction years
    Parameters: 0
    Returns: 1
        i. Redirect to the page with the years the user selected
    """
    if 'genre' not in session:
        return redirect(url_for("home"))
    start_year = request.form.get("start_year", "")
    end_year = request.form.get("end_year", "")
    session["start_year"] = start_year
    session["end_year"] = end_year
    session.pop("prediction_year", None)
    return redirect(url_for("genre_with_years", genre=session["genre"], start_year=start_year, end_year=end_year))

# Functionality and UI 4: Clients shall be able to see queried information on returned pages
# ratings.html will display the data requested in a line graph
@app.route("/genre/<genre>/<int:start_year>/<int:end_year>")
def genre_with_years(genre, start_year, end_year):
    """
    Description: displays average ratings for genre within the year range inputted
    Parameters: 3
        i. genre (str)
        ii. start_year (int)
        iii. end_year (int)
    Returns: 1
        i. rendered template ratings.html w/ graph
    """
    years = get_years_for_genre(genre)
    return render_template("ratings.html", genre=genre, start_year=start_year, end_year=end_year, project=True, years=years)

@app.route("/fig/<genre>")
def fig(genre):
    """
    Description: generate graph for average ratings and/or prediction
    Parameters: 1
        i. genre (str)
    Returns: 1
        i. file w/ graph
    """
    start_year = session.get("start_year", None)
    end_year = session.get("end_year", None)
    prediction_year = session.get("prediction_year", None)
    prediction = None

    if prediction_year:
        prediction = model.predict([[int(prediction_year)]])[0]

    # convert start and end years
    if start_year and end_year:
        start_year = int(start_year)
        end_year = int(end_year)
    else:
        start_year = None
        end_year = None

    fig = create_figure(genre, start_year, end_year, prediction_year, prediction)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype="image/png")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Description: user submits prediction year and reload page with prediction
    Parameters: 0
    Returns: 1
        i. redirects ratings.html
    """
    year = request.form.get("prediction_year", None)
    if year:
        session["prediction_year"] = int(year)
    else:
        session.pop("prediction_year", None)  # remove prediction year if nothing submitted
    return redirect(url_for("genre_ratings", genre=session.get("genre", "Unknown")))

def create_figure(genre, start_year=None, end_year=None, prediction_year=None, prediction=None):
    """
    Description: create graph for average ratings and/or predicted ratings for genre
    Parameters: 4
        i. genre (str)
        ii. start_year (int)
        iii. end_year (int)
        iv. prediction_year (int)
        v. prediction (float)
    Returns: 1
        i. Matplotlib figure
    """
    genre_mask = movies_df['genres'].str.contains(genre, case=False, na=False)
    genre_movies = movies_df[genre_mask]
    merged = ratings_df.merge(genre_movies, on='movieId', how='inner')
    merged['date'] = merged['timestamp'].apply(lambda ts: datetime.datetime.utcfromtimestamp(ts))

    if start_year and end_year:
        merged = merged[(merged['date'].dt.year >= start_year) & (merged['date'].dt.year <= end_year)]

    # group ratings by year and calc average
    merged['year'] = merged['date'].dt.year
    yearly_ratings = merged.groupby('year')['rating'].mean().reset_index()

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    # plot ratings
    ax.plot(yearly_ratings['year'], yearly_ratings['rating'], marker='o', label='Historical Ratings')

    # add prediction if user inputs something
    if prediction_year and prediction is not None:
        ax.scatter([prediction_year], [prediction], color='red', label=f'Prediction for {prediction_year}', zorder=5)
        ax.text(prediction_year, prediction, f"{prediction:.2f}", color='red', fontsize=10, ha='left')

    title_str = "Ratings for Genre: " + str(genre)
    if start_year and end_year:
        title_str += " (" + str(start_year) + "-" + str(end_year) + ")"
    fig.suptitle(title_str)

    ax.set_xlabel("Year")
    ax.set_ylabel("Average Rating")
    ax.legend()
    return fig

@app.route('/<path:path>')
def catch_all(path):
    """
    Description: error checking reroutes to homepage
    Parameters: 1
        i. path (str)
    Returns: 1
        i. redirect to home.html
    """
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)