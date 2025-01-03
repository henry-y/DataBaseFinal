from flask import jsonify, request
from sqlalchemy import func
from app.routes import bp
from app.models import Vehicle, Rental
from app import db
import re

PLATE_NUMBER_PATTERN = re.compile(r'^[\u4e00-\u9fa5][A-Z][A-Z0-9]{5}$')


@bp.route('/api/vehicles', methods=['GET'])
def get_vehicles_and_rental_info():
    try:
        subquery = (
            db.session.query(
                Rental.vehicle_id,
                func.max(Rental.created_at).label('latest_created_at')
            )
            .group_by(Rental.vehicle_id)
            .subquery()
        )

        vehicles = (
            db.session.query(Vehicle, Rental.status)
            .join(subquery, Vehicle.vehicle_id == subquery.c.vehicle_id, isouter=True)
            .join(Rental, (Vehicle.vehicle_id == Rental.vehicle_id) & (Rental.created_at == subquery.c.latest_created_at), isouter=True)
            .filter(Vehicle.is_deleted == False)
            .order_by(Vehicle.vehicle_id.asc())
            .all()
        )

        result = {
            'data': [
                {
                    **vehicle.to_dict(),
                    'status': 'busy' if status in ['ongoing', 'overdue'] else 'available'
                }
                for vehicle, status in vehicles
            ],
            'total': len(vehicles)
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicles_by_id(vehicle_id):
    try:
        vehicle = Vehicle.query.filter_by(
            vehicle_id=vehicle_id).filter_by(is_deleted=False).first()
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        return jsonify(vehicle.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    try:
        data = request.get_json()

        required_fields = ['type', 'brand', 'model',
                           'color', 'price_per_day', 'plate_number']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            price = float(data['price_per_day'])
            if price <= 0:
                return jsonify({'error': 'Price must be positive'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400

        plate_number = data['plate_number']
        if not PLATE_NUMBER_PATTERN.match(plate_number):
            return jsonify({'error': 'Invalid plate number format'}), 400

        if Vehicle.query.filter_by(plate_number=data['plate_number']).first():
            return jsonify({'error': 'Plate number already exists'}), 400

        vehicle = Vehicle(
            type=data['type'],
            brand=data['brand'],
            model=data['model'],
            color=data['color'],
            price_per_day=price,
            plate_number=data['plate_number']
        )
        db.session.add(vehicle)
        db.session.commit()
        return jsonify(vehicle.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.filter_by(
            vehicle_id=vehicle_id).filter_by(is_deleted=False).first()
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404

        data = request.get_json()

        if 'type' in data:
            if not data['type'].strip():
                return jsonify({'error': 'Vehicle type cannot be empty'}), 400
            vehicle.type = data['type']

        if 'price_per_day' in data:
            try:
                price = float(data['price_per_day'])
                if price <= 0:
                    return jsonify({'error': 'Price must be positive'}), 400
                vehicle.price_per_day = price
            except ValueError:
                return jsonify({'error': 'Invalid price format'}), 400

        if 'brand' in data:
            vehicle.brand = data['brand']
        if 'model' in data:
            vehicle.model = data['model']
        if 'color' in data:
            vehicle.color = data['color']
        if 'price_per_day' in data:
            vehicle.price_per_day = data['price_per_day']
        if 'plate_number' in data and data['plate_number'] != vehicle.plate_number:
            if Vehicle.query.filter_by(plate_number=data['plate_number']).first():
                return jsonify({'error': 'Plate number already exists'}), 400
            vehicle.plate_number = data['plate_number']

        db.session.commit()
        return jsonify(vehicle.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    try:
        vehicle = Vehicle.query.get(id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404

        if Rental.query.filter_by(vehicle_id=id).first():
            return jsonify({'error': 'Cannot delete vehicle with associated rentals'}), 400

        vehicle.is_deleted = True
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
