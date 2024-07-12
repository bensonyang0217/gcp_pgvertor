import os

import pg8000
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import create_engine

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
POSTGRES_REGION = os.getenv('POSTGRES_REGION')
POSTGRES_INSTANCE = os.getenv('POSTGRES_INSTANCE')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
ip_type = IPTypes.PUBLIC
connector = Connector()
model_name = os.getenv('MODEL_NAME')
embeddings = VertexAIEmbeddings(model_name=model_name)

def get_conn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        f"{GCP_PROJECT_ID}:{POSTGRES_REGION}:{POSTGRES_INSTANCE}",
        "pg8000",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        db=POSTGRES_DB,
        ip_type=ip_type
    )
    return conn

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    creator=get_conn,
)

#pg vector info
store = PGVector(
            
            connection=str(SQLALCHEMY_DATABASE_URL),
            engine_args={"creator": get_conn},
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            use_jsonb =True)