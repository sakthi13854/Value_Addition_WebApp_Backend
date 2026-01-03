from dotenv import load_dotenv
load_dotenv()
import os 
from flask import Flask
from flask import render_template
from Backend.Routes.Auth_Routes import auth_bp
from Backend.Routes.Product_Routes import product_bp
from Backend.databases.db import engine, Base ,get_db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from Backend.config import (
    JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION,
    JWT_COOKIE_CSRF_PROTECT,
    JWT_COOKIE_SECURE,
    JWT_COOKIE_SAMESITE,
)


app = Flask(__name__)

#Jwt token acces
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
app.config["JWT_COOKIE_CSRF_PROTECT"] = JWT_COOKIE_CSRF_PROTECT
app.config["JWT_COOKIE_SECURE"] = JWT_COOKIE_SECURE
app.config["JWT_COOKIE_SAMESITE"] = JWT_COOKIE_SAMESITE

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)

#database initialitation
def init_db():
    Base.metadata.create_all(bind=engine)
    print(" Database initialized successfully")



@app.route("/dashboard")
@jwt_required(locations=["cookies"])
def dashboard():
    user_id_or_email = get_jwt_identity()
    return render_template(
        "dashboard.html",
        user_email=user_id_or_email
    )

init_db()

if __name__ == "__main__":
    app.run(debug=True)