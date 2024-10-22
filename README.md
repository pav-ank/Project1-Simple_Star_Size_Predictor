# 🌟 Star Size Predictor
This project implements a Star Size Prediction application, allowing users to generate and predict star sizes based on brightness using a linear regression model. The project is built with a Streamlit frontend and a FastAPI backend.

- Here is me explaining the web application: https://drive.google.com/file/d/1oTS716M8ocJOzXLuSkTHMFfRYmEL8WR_/view?usp=sharing
* Here’s a detailed README.md file for your project:

## 📜 Table of Contents
1) Features
2) Technologies
3) Requirements
4) Installation
5) Usage
6) API Endpoints
7) Project Structure
8) Acknowledgments

## 🌟 Features
* Data Generation: Generate random star data based on brightness and size.
* Predictions: Predict the size of stars using a linear regression model.
* Interactive Plots: Visualize the actual vs predicted star sizes using a scatter plot.
* Background Styling: Customizable styling with a background image of the Pleiades and a centered title.
* Fixed Footer: Displays the developer's name and project context.

## 💻 Technologies
* Streamlit: Web app framework used to build the frontend.
* FastAPI: Backend framework for creating API endpoints.
* Pandas: For data manipulation and analysis.
* Matplotlib: For generating plots.
* NumPy: Used for mathematical computations and generating random data.
* CORS Middleware: Allows Cross-Origin Resource Sharing (CORS) in FastAPI.

## 📦 Requirements
* Python 3.8 or later
* pip (Python package installer)

#### Python Libraries:

* streamlit
* fastapi
* uvicorn
* requests
* pandas
* numpy
* matplotlib

## ⚙️ Installation
1) ⚙️ Installation:
```python
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2) Install the necessary dependencies:
```python
pip install -r requirements.txt
```

3) Run the FastAPI backend:
```python
uvicorn main:app --reload
```

4) Run the Streamlit frontend:
```python
streamlit run app.py
```

## 🚀 Usage
1) Open your browser and navigate to http://localhost:8501 to access the Streamlit frontend.
2) Enter the number of stars you want to generate and press the Generate Data button.
3) View the generated and predicted star data on the page.
4) Press the Generate Plot button to visualize the prediction against the actual star data in a plot

## 📡 API Endpoints
#### /create_data/ (POST)
Generates star data based on brightness and size.

Query Parameters:
* num_stars: The number of stars to generate (default: 500).

#### /predict/ (POST)
Accepts a CSV file with generated star data and returns predictions using the linear regression model.

Form Data:
* file: CSV file containing star brightness and size.

#### /plot/ (POST)
Generates a plot of the actual vs predicted star sizes.

Form Data:
* file: CSV file containing star brightness, size, and predictions.

## 🏗️ Project Structure
```python
├── app.py                # Streamlit frontend
├── main.py               # FastAPI backend
├── requirements.txt      # Required Python libraries
└── README.md             # Project README
```

## 🎨 Styling
The Streamlit frontend includes a custom background image of the Pleiades star cluster. The title is centered in a semi-transparent container for readability. The footer remains fixed at the bottom of the page, containing the text: "This project is developed by Pavankumar Megeri as part of the ML4A Training Program at Spartifical.".

## 🙏 Acknowledgments
This project is developed as part of the ML4A Training Program at Spartifical

