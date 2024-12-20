from flask import jsonify, request, Blueprint
from app.routes import bp
from app.models import Customer
from app import db

@bp.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@bp.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    
    # 验证必需字段
    required_fields = ['name', 'phone', 'address', 'id_card']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # 检查身份证号是否已存在
    if Customer.query.filter_by(id_card=data['id_card']).first():
        return jsonify({'error': 'ID card already exists'}), 400
    
    try:
        customer = Customer(
            name=data['name'],
            phone=data['phone'],
            address=data['address'],
            id_card=data['id_card']
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 