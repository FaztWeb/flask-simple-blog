from extensions.mysql import mysql
from app import app

# mysql settings
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "faztpassword"
app.config["MYSQL_DB"] = "flaskblog"
app.config[
    "MYSQL_CURSORCLASS"
] = "DictCursor"  # to return a dictionary instead of a tuple

mysql.init_app(app)

if __name__ == "__main__":
    app.secret_key = "somsecretkey"
    app.run(debug=True, port=3000)
