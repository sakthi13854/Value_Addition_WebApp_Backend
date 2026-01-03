from flask import Blueprint, render_template, request, jsonify
from Backend.databases.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.models.Users_Schema import Consumers
from sqlalchemy import select
from flask_jwt_extended import create_access_token
from flask import redirect, url_for

auth_bp = Blueprint("Auth",__name__)

@auth_bp.route('/signup')
def signup_page():
    return render_template('signup.html')

@auth_bp.post("/signup")
def signup():
    try:
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()

        username = (data.get("name") or data.get("Name") or "").strip()
        email = (data.get("Email") or data.get("email") or "").strip()
        password = (data.get("Password") or data.get("password") or "").strip()

        
        if not all([username, email, password]):
            return jsonify({"error": "All fields are required"}), 400

        db =  get_db()
        try:
            result =  db.execute(
                select(Consumers).where(
                    (Consumers.Name == username) |
                    (Consumers.Email == email)
                )
            )

            if result.scalar_one_or_none():
                return jsonify({"error": "Consumer already exists"}), 409

            user = Consumers(
                Name=username,
                Email=email,
                Password=password
            )

            db.add(user)
            db.commit()

            return redirect(url_for("Auth.login_page",msg="registered"))

        finally:
            if db:
                db.close()

    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500

@auth_bp.get('/login')
def login_page():
    return render_template('login.html')

@auth_bp.post("/login")
def login():
    try:
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()

        email = (data.get("Email") or data.get("email") or "").strip()
        password = (data.get("Password") or data.get("password") or "").strip()

        db = get_db()
        result = db.execute(
            select(Consumers).where(
                    Consumers.Email == email ,
                    Consumers.Password == password
                )
        )   
        user =result.scalar_one_or_none()

        if not user:
            return render_template(
                'login.html',
                error = 'Invalid credentials'
            )  
        token = create_access_token(identity = str(user.Id))
        response = redirect(url_for("dashboard"))
        response.set_cookie("access_token_cookie", token, httponly=True)
        return response


    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


    finally:
        if db:
            db.close()

@auth_bp.post('/logout')
def logout():
    response = redirect("/login")
    response.delete_cookie('access_token_cookie')
    return response

