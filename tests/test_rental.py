import pytest
from datetime import datetime, timedelta
from app import db
from app.models import Rental
from sqlalchemy.exc import IntegrityError

def test_rental_creation(test_rental):
    """测试租赁创建和所有属性"""
    assert test_rental.rental_id is not None
    assert test_rental.vehicle_id is not None
    assert test_rental.customer_id is not None
    assert isinstance(test_rental.start_time, datetime)
    assert test_rental.duration_days == 3
    assert isinstance(test_rental.expected_return_time, datetime)
    assert test_rental.actual_return_time is None
    assert float(test_rental.total_fee) == 900.00
    assert test_rental.status == '进行中'
    assert test_rental.created_at is not None
    assert test_rental.updated_at is not None

def test_rental_to_dict(test_rental):
    """测试租赁转字典功能"""
    rental_dict = test_rental.to_dict()
    assert rental_dict['rental_id'] == test_rental.rental_id
    assert rental_dict['vehicle_id'] == test_rental.vehicle_id
    assert rental_dict['customer_id'] == test_rental.customer_id
    assert isinstance(rental_dict['start_time'], str)
    assert rental_dict['duration_days'] == 3
    assert isinstance(rental_dict['expected_return_time'], str)
    assert rental_dict['actual_return_time'] is None
    assert float(rental_dict['total_fee']) == 900.00
    assert rental_dict['status'] == '进行中'

def test_rental_relationships(test_rental):
    """测试租赁关系"""
    assert test_rental.vehicle is not None
    assert test_rental.customer is not None
    assert test_rental.vehicle.type == 'SUV'
    assert test_rental.customer.name == '张三'

def test_rental_foreign_key_constraint(app):
    """测试外键约束"""
    with app.app_context():
        # 测试不存在的车辆ID
        with pytest.raises(IntegrityError):
            rental = Rental(
                vehicle_id=99999,  # 不存在的车辆ID
                customer_id=1,
                start_time=datetime.now(),
                duration_days=3,
                expected_return_time=datetime.now() + timedelta(days=3),
                total_fee=900.00,
                status='进行中'
            )
            db.session.add(rental)
            db.session.commit()

def test_rental_cascade_delete(app, test_rental, test_vehicle, test_customer):
    """测试级联删除"""
    with app.app_context():
        # 确保所有对象都在同一个会话中
        rental_id = test_rental.rental_id
        
        # 重新从数据库加载对象
        vehicle = db.session.merge(test_vehicle)
        customer = db.session.merge(test_customer)
        rental = db.session.merge(test_rental)
        
        # 尝试删除被引用的车辆，应该失败
        with pytest.raises(IntegrityError):
            db.session.delete(vehicle)
            db.session.commit()
        db.session.rollback()
        
        # 尝试删除被引用的客户，应该失败
        with pytest.raises(IntegrityError):
            db.session.delete(customer)
            db.session.commit()
        db.session.rollback()
        
        # 删除租赁记录应该成功
        db.session.delete(rental)
        db.session.commit()
        assert Rental.query.get(rental_id) is None