from flask import jsonify
from app.routes import bp
from app.models import Vehicle

@bp.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]) 