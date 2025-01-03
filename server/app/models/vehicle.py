from app import db
from datetime import datetime, timezone


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    vehicle_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    price_per_day = db.Column(db.Numeric(10, 2), nullable=False)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    
    rentals = db.relationship('Rental', backref='vehicle', lazy=True)

    def to_dict(self):
        return {
            'vehicle_id': self.vehicle_id,
            'plate_number': self.plate_number,
            'type': self.type,
            'brand': self.brand,
            'model': self.model,
            'color': self.color,
            'price_per_day': float(self.price_per_day),
        }
