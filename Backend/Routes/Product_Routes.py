from flask import request, Blueprint, render_template, jsonify
from sqlalchemy import select
from Backend.databases.db import get_db
from Backend.models.Product_Schema import Products
from Backend.Utils.helpers import Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import redirect, url_for



product_bp = Blueprint('Products',__name__,url_prefix = "/Products")

@product_bp.route('/')
@jwt_required(locations='cookies')
def Add_page():
    return render_template('products.html')

@product_bp.post('/add')
@jwt_required(locations='cookies')
def add_products():
    print("JWT identity:", get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()
    user_id = get_jwt_identity()
    product_name = (data.get('Name') or data.get('name') or "").strip()
    description =  (data.get('Description') or data.get('description') or "").strip()

    status =  (data.get('Status') or data.get('status') or "").strip()
    price = (data.get('Price') or data.get('price') or "").strip()

    category = (data.get('Category') or data.get('category') or "").strip()
    categroy_nm = Category[category]
    category_enum = categroy_nm.value

    if not all([product_name,price,category]):
        return jsonify({'error':'All fields are Required'}),400
    db = get_db()
    print("JWT identity:", get_jwt_identity())
    try:
        if user_id is not None:
            current_user = get_jwt_identity()
            product = Products(
                UserId = user_id,
                Name = product_name,
                Description = description,
                Price = price,
                Status = status,
                Category = category_enum
              )
                
            

            db.add(product)
            db.commit()
            return jsonify({"message": "Product added"}), 200

    except Exception as e:
        print("Product not added", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if db:
            db.close()


@product_bp.get("/list")
@jwt_required(locations="cookies")
def list_products():
    user_id = get_jwt_identity()
    db = get_db()

    try:
        products = db.execute(
            select(Products).where(Products.UserId == user_id)
        ).scalars().all()

        return jsonify([
            {
                "id": p.Id,          
                "name": p.Name,
                "price": p.Price,
                "status": p.Status,
                "category": p.Category,
            }
            for p in products
        ])
    finally:
        db.close()
  
@product_bp.put('/edit/<int:id>')
@jwt_required(locations='cookies')
def edit_products(id ):
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()
    
    product_name = (data.get('Name') or data.get('name') or "").strip()
    description =  (data.get('Description') or data.get('description') or "").strip()

    price = (data.get('Price') or data.get('price') or "").strip()
    status =  (data.get('Status') or data.get('status') or "").strip()

    category = (data.get('Category') or data.get('category') or "").strip()
    categroy_nm = Category[category]
    category_enum = categroy_nm.value


    if not all([product_name,price,category]):
        return jsonify({'error':'All fields are Required'}),400
    db = get_db()

    try:
        user_id = get_jwt_identity()
        resUlt = db.execute(
            select(Products).where(
                Products.Id == id
            )
        )
        result = resUlt.scalar_one_or_none()

        if result is not None:
            
            result.Name = product_name,
            result.Description = description,
            result.Price = price,
            result.Category = category_enum,
            result.Status = status
            
            db.commit()
            return jsonify({"message": "Product updated"}), 200
        else:
            return jsonify({'error':"User need to log in to add products"}),400

    except Exception as e:
        print("Product not added", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if db:
            db.close()

@product_bp.delete('/delete/<int:id>')
@jwt_required(locations='cookies')
def delete_products(id : int):
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()
    
    product_name = (data.get('Name') or data.get('name') or "").strip()
    current_user = get_jwt_identity()
    db = get_db()

    try:
        user_id = get_jwt_identity()
        Result = db.execute(
            select(Products).where(
                Products.Id == id
            )
        )
        result = Result.scalar_one_or_none()
        if result is not None:
            db.delete(result)
            db.commit()
            
            return jsonify({"message": "Product deleted"}), 200
        else:
            return jsonify({'error':"User need to log in to add products"}),400

    except Exception as e:
        print("Product not added", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if db:
            db.close()
    