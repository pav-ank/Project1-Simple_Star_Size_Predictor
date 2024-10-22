import streamlit as st
import pandas as pd
import requests
import io

# Custom CSS for styling, including background image
st.set_page_config(
    page_title="Star Size Predictor ✨",
    page_icon="🌞"
)

st.markdown(
    """
    <style>
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

    /* Updated styling for the dialog box */
    .dialog-box {
        border: 2px solid #FFFFFF;  /* White border */
        padding: 10px;
        border-radius: 10px;
        background-color: rgba(0, 0, 0, 0.9);  /* Black with slight transparency */
        color: #F0F0F0;  /* Light white text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title (without container)
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>🌟 Star Size Prediction</h1>", unsafe_allow_html=True)

# Adding a dialogue box with updated color scheme (black background and light white text)
st.markdown("""
    <div class="dialog-box">
        <h3>HOW TO USE THIS APP</h3>
        <p>1) Enter the number of stars to generate a dataset with its brightness and size values.</p>
        <p>2) Click on the 'Generate Data' button.</p>
        <p>3) The app will generate the data and automatically predict the sizes using Linear Regression.</p>
        <p>4) Click on the 'Generate Plot' button, and it will plot the true sizes and predicted sizes based on brightness values.</p>
        <p>5) You can now download the generated data, predicted data, and the plot.</p>
    </div>
""", unsafe_allow_html=True)

# Input section for the number of stars
num_stars = st.number_input("Enter the number of stars to generate:", min_value=1, value=500)

API_URL = "https://project1-simple-star-size-predictor.onrender.com/"

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
        st.dataframe(st.session_state.df_generated)  # No explicit download button needed; Streamlit adds hover download option

    with col2:
        st.subheader("Predicted Data")
        st.dataframe(st.session_state.df_predictions)  # No explicit download button needed

# Button to generate plot after data and predictions are available
if st.button("Generate Plot"):
    if st.session_state.df_predictions is not None and st.session_state.data_csv_content:
        plot_response = requests.post(f'{API_URL}/plot/', files={'file': io.BytesIO(st.session_state.prediction_csv.encode('utf-8'))})

        if plot_response.status_code == 200:
            plot_image = plot_response.content

            # Display the plot as an image
            st.image(plot_image, caption='Linear Regression Plot', use_column_width=True)

            # Provide plot as a downloadable file (hover to download, like with dataframes)
            st.download_button(
                label="Download Plot",
                data=plot_image,
                file_name="linear_regression_plot.png",
                mime="image/png"
            )
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
