from flask import Flask
from Backend.Routes.Auth_Routes import auth_bp
from Backend.databases.db import engine, Base ,get_db

app = Flask(__name__)
app.register_blueprint(auth_bp)

#database initialitation
def init_db():
    Base.metadata.create_all(bind=engine)
    print(" Database initialized successfully")


@app.route("/")
def hello():
    return "server is running"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)