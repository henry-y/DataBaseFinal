from flask import jsonify
from app.routes import bp
from app.models import Customer

@bp.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]) 