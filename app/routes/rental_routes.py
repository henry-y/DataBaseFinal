from flask import jsonify, request
from app.routes import bp
from app.models import Rental, Vehicle, Customer
from app import db
from datetime import datetime, timedelta

@bp.route('/api/rentals', methods=['GET'])
def get_rentals():
    rentals = Rental.query.all()
    return jsonify([rental.to_dict() for rental in rentals])

@bp.route('/api/rentals', methods=['POST'])
def create_rental():
    data = request.get_json()
    
    # 验证必需字段
    required_fields = ['vehicle_id', 'customer_id', 'duration_days']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # 检查车辆是否存在且可租用
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    if vehicle.status != '可租用':
        return jsonify({'error': 'Vehicle is not available'}), 400
    
    # 检查客户是否存在
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    try:
        start_time = datetime.now()
        duration_days = int(data['duration_days'])
        expected_return_time = start_time + timedelta(days=duration_days)
        total_fee = float(vehicle.price_per_day) * duration_days
        
        rental = Rental(
            vehicle_id=data['vehicle_id'],
            customer_id=data['customer_id'],
            start_time=start_time,
            duration_days=duration_days,
            expected_return_time=expected_return_time,
            total_fee=total_fee,
            status='进行中'
        )
        
        # 更新车辆状态
        vehicle.status = '已租出'
        
        db.session.add(rental)
        db.session.commit()
        return jsonify(rental.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 