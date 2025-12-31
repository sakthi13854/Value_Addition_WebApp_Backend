from flask import request, Blueprint, render_template, jsonify
from sqlalchemy import select
from Backend.databases.db import get_db
from Backend.models.Product_Schema import Products
from Backend.Utils.helpers import Category

product_bp = Blueprint('Products',__name__)

@product_bp.get('/Products/add')
def Add_page():
    return render_template('Addproducts.html')

@product_bp.post('/Products/add')
def add_products():
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()
    
    product_name = (data.get('ProductName') or data.get('productname') or "").strip()
    description =  (data.get('Description') or data.get('description') or "").strip()
    price = (data.get('Price') or data.get('price') or "").strip()
    category = (data.get('Category') or data.get('category') or "").strip()
    categroy_nm = Category[category]
    category_enum = categroy_nm.value

    if not all([product_name,price,category]):
        return jsonify({'error':'All fields are Required'}),400
    db = get_db()

    try:
        product = Products(
            Name = product_name,
            Description = description,
            Price = price,
            Category = category_enum
        )

        db.add(product)
        db.commit()
        
        return jsonify({'success':'Product added successfully'}),201

    except Exception as e:
        print("Product not added", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if db:
            db.close()
    
