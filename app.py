from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from fastapi import FastAPI,  APIRouter #, Response, Body , Depends
from fastapi.responses import RedirectResponse
import models
#from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import  engine  #, get_db
#from typing import Annotated

# For Validation

from controller import student,book , menu, order

import os



# Import models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url='/docs')

## Book



app.include_router(student.router_v1)
app.include_router(book.router_v1)
app.include_router(menu.router_v1)
app.include_router(order.router_v1)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host=os.environ.get("HOST","127.0.0.1"))
