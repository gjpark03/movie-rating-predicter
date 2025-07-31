# Movie Ratings Analysis Flask App

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.5+-orange.svg)](https://matplotlib.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-red.svg)](https://scikit-learn.org/)

A Flask-based web application that leverages pandas for data manipulation, matplotlib for interactive visualizations, and scikit-learn's linear regression to analyze movie ratings by genre and predict future rating trends.

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


> Example: Crime Movie Ratings from 1996 - 2016 and Prediction for 2026

  <img width="629" height="493" alt="Screenshot 2025-07-31 at 12 50 16 PM" src="https://github.com/user-attachments/assets/826f9086-6556-4d3a-8fc8-8992c8d67e25" />


## Dependencies

- Flask: Web framework
- pandas: Data manipulation
- matplotlib: Data visualization
- scikit-learn: Machine learning for predictions

## 🚨 Common Errors & Solutions

### Port 5000 Already in Use
**Error:** `Address already in use` or `OSError: [Errno 48] Address already in use`

**Solution for Mac Users:**
1. Go to **System Preferences** → **Sharing**
2. Uncheck **AirPlay Receiver** in the left sidebar
3. This will free up port 5000 for your Flask app

**Alternative Solutions:**
- Kill the process using port 5000: `kill -9 $(lsof -ti:5000)`
- Use a different port: Change `app.run(port=5001)` in `app.py`

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
