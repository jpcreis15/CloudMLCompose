import pickle
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
import datetime

####################################################
# Function definition
def insert_db(db, input_model, prediction, timestamp):
    with db.connect() as conn:
        query = 'INSERT INTO inferences(input_sample, prediction, inference_time) VALUES (\'{}\', \'{}\', \'{}\')'.format(input_model, prediction, timestamp)
        conn.execute(text(query))
        conn.commit()

def get_inferences(db):
    with db.connect() as conn:
        query = 'SELECT * FROM inferences;'
        rows = conn.execute(text(query))
        result = []
        for row in rows:
            result.append({"id" : row[0],
                           "input" : row[1],
                           "prediction" : row[2],
                           "inference_time" : row[3].strftime('%Y-%m-%d %H:%M:%S')}) 
        return result

####################################################
# DB connection
db_engine = None
load_dotenv()

APP_DATABASE_NAME = os.getenv('APP_DATABASE_NAME')
APP_DATABASE_USER = os.getenv('APP_DATABASE_USER')
APP_DATABASE_PASS = os.getenv('APP_DATABASE_PASS')
APP_DATABASE_HOST = os.getenv('APP_DATABASE_HOST')
APP_DATABASE_PORT = os.getenv('APP_DATABASE_PORT')

try:
    db_string = 'postgresql://{}:{}@{}:{}/{}'.format(APP_DATABASE_USER, 
                                                        APP_DATABASE_PASS, 
                                                        APP_DATABASE_HOST,
                                                        APP_DATABASE_PORT,
                                                        APP_DATABASE_NAME)
    db_engine = create_engine(db_string)
except Exception as e:
    print("Somethiing went wrong while loading db!")

####################################################


# Opening the file might also be once the inference endpoint is called
# Model trained using the Iris dataset
with open("./model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check service
@app.get("/healthcheck")
async def health():
    """
    Health Check service
    """

    return {"message":"all good"}

# Inference service
@app.post("/inference")
async def predict(input: list):
    """
    Inference Service
    """

    features = list(input)
    print("features: ", features)

    pred = model.predict([features])
    print("prediction: ", pred)

    if db_engine is not None:
        insert_db(db_engine,
                features,
                pred[0],
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return json.dumps({"result": pred[0]})

# Health check service
@app.get("/get_all_inferences")
async def get_all_inferences():
    """
    Service to get all inferences stored in the DB
    """
    if db_engine is not None:
        return json.dumps({"result": get_inferences(db_engine)})
        # get_inferences(db_engine)
        # return json.dumps({"result": "all good!"})
    else:
        raise HTTPException(status_code=500, detail="Internal Error: DB not found!")