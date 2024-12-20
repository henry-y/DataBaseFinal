from flask import jsonify
from app.routes import bp
from app.models import Rental

@bp.route('/api/rentals', methods=['GET'])
def get_rentals():
    rentals = Rental.query.all()
    return jsonify([rental.to_dict() for rental in rentals]) 