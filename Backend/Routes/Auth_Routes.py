from flask import Blueprint, render_template, request, jsonify
from Backend.databases.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.models.Users_Schema import Consumers
from sqlalchemy import select


auth_bp = Blueprint("Auth",__name__)

@auth_bp.get('/signup')
def signup_page():
    return render_template('signup.html')

@auth_bp.post("/signup")
def signup():
    try:
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()

        username = (data.get("Username") or data.get("username") or "").strip()
        email = (data.get("Email") or data.get("email") or "").strip()
        password = (data.get("Password") or data.get("password") or "").strip()

        print("RAW DATA:", data)
        print("USERNAME:", username)
        print("EMAIL:", email)
        print("PASSWORD:", password)

        
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

            return jsonify({"success": "Consumer registered successfully"}), 201

        finally:
            if db:
                db.close()

    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


