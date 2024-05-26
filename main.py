from fastapi import FastAPI
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()



@app.get('/')
async def home():
    return 'hello world '+str(os.getenv('ALFA'))