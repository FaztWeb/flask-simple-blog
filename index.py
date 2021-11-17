from utils.mysql import mysql
from app import app 

mysql.init_app(app)

if __name__ == "__main__":
    app.secret_key = "somsecretkey"
    app.run(debug=True, port=3000)
