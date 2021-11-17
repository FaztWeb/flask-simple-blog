from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_DB = os.environ["MYSQL_DB"]

print(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)