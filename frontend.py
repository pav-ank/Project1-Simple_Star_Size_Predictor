import streamlit as st
import pandas as pd
import requests
import io

# Custom CSS for styling, including background image and centered title
st.set_page_config(
    page_title="Star Size Predictor ✨",
    page_icon="🌞"
)

st.markdown(
    """
    <style>
    .title-container {
        text-align: center;
        color: #FFFFFF;
        margin-top: -50px;
        padding: 20px;
        background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent background for better readability */
        border-radius: 10px;  /* Rounded corners for the container */
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px;
    }

    .stApp {
        background: url('https://images6.alphacoders.com/664/thumb-1920-664350.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title container
with st.container():
    st.markdown("<div class='title-container'><h1>🌟 Star Size Prediction</h1></div>", unsafe_allow_html=True)

# Input section for the number of stars
num_stars = st.number_input("Enter the number of stars to generate:", min_value=1, value=500)

API_URL = "http://127.0.0.1:8000"

# State variables to hold data between interactions
if 'df_generated' not in st.session_state:
    st.session_state.df_generated = None
if 'df_predictions' not in st.session_state:
    st.session_state.df_predictions = None
if 'data_csv_content' not in st.session_state:
    st.session_state.data_csv_content = None
if 'prediction_csv' not in st.session_state:
    st.session_state.prediction_csv = None

# Button to generate data
if st.button("Generate Data"):
    create_data_response = requests.post(f'{API_URL}/create_data/?num_stars={num_stars}')
    
    if create_data_response.status_code == 200:
        st.session_state.data_csv_content = create_data_response.content
        data_csv = create_data_response.content.decode('utf-8')
        st.session_state.df_generated = pd.read_csv(io.StringIO(data_csv))

        predict_response = requests.post(f'{API_URL}/predict/', files={'file': io.BytesIO(st.session_state.data_csv_content)})

        if predict_response.status_code == 200:
            st.session_state.prediction_csv = predict_response.content.decode('utf-8')
            st.session_state.df_predictions = pd.read_csv(io.StringIO(st.session_state.prediction_csv))

# Display the generated and predicted data if they exist
col1, col2 = st.columns(2)

if st.session_state.df_generated is not None and st.session_state.df_predictions is not None:
    with col1:
        st.subheader("Generated Data")
        st.dataframe(st.session_state.df_generated)

    with col2:
        st.subheader("Predicted Data")
        st.dataframe(st.session_state.df_predictions)

# Button to generate plot after data and predictions are available
if st.button("Generate Plot"):
    if st.session_state.df_predictions is not None and st.session_state.data_csv_content:
        plot_response = requests.post(f'{API_URL}/plot/', files={'file': io.BytesIO(st.session_state.prediction_csv.encode('utf-8'))})

        if plot_response.status_code == 200:
            plot_image = plot_response.content
            st.image(plot_image, caption='Linear Regression Plot', use_column_width=True)
        else:
            st.error("Failed to generate plot. Please try again.")

# Footer
st.markdown(
    """
    <div class="footer">
    This project is developed by <strong>Pavankumar Megeri</strong> as part of the ML4A Training Program at Spartifical.
    </div>
    """,
    unsafe_allow_html=True
)
