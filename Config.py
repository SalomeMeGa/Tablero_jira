import os
from dotenv import load_dotenv

#Cargar las variables de entorno desde el archivo .env
load_dotenv()

#install python-dotenv

# Read the value of the environment variable
USER= os.environ['USER']
API_TOKEN= os.environ['API_TOKEN']
BASE_URL=os.environ['BASE_URL']
URL_PARTE_1=os.environ['URL_PARTE_1']
URL_PARTE_2=os.environ['URL_PARTE_2']

MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DB = os.environ['MYSQL_DB']
MYSQL_PORT = os.environ['MYSQL_PORT']
MYSQL_TABLE = os.environ['MYSQL_TABLE']

class Config:
    username = USER
    api_token = API_TOKEN
    base_url = BASE_URL
    Url_parte_1 = URL_PARTE_1
    Url_parte_2 = URL_PARTE_2
    mysql_user = MYSQL_USER
    mysql_host = MYSQL_HOST
    mysql_password = MYSQL_PASSWORD
    mysql_port = MYSQL_PORT
    mysql_db = MYSQL_DB
    mysql_table = MYSQL_TABLE