# Movie Ratings Analysis Flask App

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.5+-orange.svg)](https://matplotlib.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-red.svg)](https://scikit-learn.org/)

This Flask application allows users to analyze movie ratings by genre and predict future ratings using machine learning.


## 🚀 Quick Start

### Local Development

#### 1. Create a Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
# Make sure your virtual environment is activated, then:
pip install -r requirements.txt
```

#### 3. Run the Application

```bash
# Make sure your virtual environment is activated, then:
python app.py
```

The application will be available at `http://localhost:5000`

#### 4. Deactivate Virtual Environment (when done)

```bash
deactivate
```

## Features

- Select movie genres to view average ratings over time
- Filter ratings by year range
- Predict future ratings using linear regression
- Interactive visualizations with matplotlib

## Dependencies

- Flask: Web framework
- pandas: Data manipulation
- matplotlib: Data visualization
- scikit-learn: Machine learning for predictions

## 📁 Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel deployment configuration
├── runtime.txt        # Python runtime specification
├── .gitignore         # Git ignore rules
├── csv/               # Data files
│   ├── movies.csv
│   └── ratings.csv
└── templates/         # HTML templates
    ├── home.html
    └── ratings.html
``` 

## 👤 Author

Grace Park
- Email: parkjgrace2025@gmail.com