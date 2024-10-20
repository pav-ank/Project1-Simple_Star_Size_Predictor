from fastapi import FastAPI, File, UploadFile, Query
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

W = 1.982015  # Slope (weight) of the regression line
b = 9.500380  # Intercept (bias) of the regression line

@app.get('/')
def default():
    return {'App': 'Running'}

@app.post("/create_data/")
def create_data(num_stars: int = Query(500, description="Number of stars to generate")):
    X_train = 3 * np.random.random(size=(num_stars, 1))  # Brightness
    noise = np.random.normal(0, 0.5, size=(num_stars, 1))  # Noise for more realistic data
    y_train = 9 + 2 * X_train + noise  # Size based on brightness and noise

    df = pd.DataFrame(np.hstack((X_train, y_train)), columns=["brightness", "size"])

    output = df.to_csv(index=False).encode('utf-8')

    return StreamingResponse(io.BytesIO(output),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=generated_stars.csv"})

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()

    df = pd.read_csv(io.BytesIO(contents))
    df.columns = ['inputs', 'targets']

    df['predictions'] = W * df['inputs'] + b

    output = df.to_csv(index=False).encode('utf-8')

    return StreamingResponse(io.BytesIO(output),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=predictions.csv"})

@app.post("/plot/")
async def plot(file: UploadFile = File(...)):
    contents = await file.read()

    df = pd.read_csv(io.BytesIO(contents))

    # Debugging: Check the contents of the DataFrame
    if 'inputs' not in df.columns or 'targets' not in df.columns:
        return {"error": "Missing 'inputs' or 'targets' columns in the CSV."}

    plt.figure(figsize=(10, 6))
    plt.scatter(df['inputs'], df['targets'], color='royalblue', label='Actual Targets', marker='x')

    df['predictions'] = W * df['inputs'] + b

    mse_score = np.mean(np.square(df['predictions'].values - df['targets'].values))

    plt.plot(df['inputs'], df['predictions'], color='k', label='Predictions', linewidth=2)
    plt.title(f'Linear Regression for Stars Data (MSE: {round(mse_score, 1)})', color='maroon', fontsize=15)
    plt.xlabel('Brightness', color='m', fontsize=13)
    plt.ylabel('Size', color='m', fontsize=13)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    # Debugging: Check the size of the image being returned
    image_size = buf.getbuffer().nbytes
    if image_size == 0:
        return {"error": "Generated image is empty."}

    return StreamingResponse(buf,
                             media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=plot.png"})
