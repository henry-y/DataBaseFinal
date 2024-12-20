import pytest
from app.models import Vehicle

def test_vehicle_creation(test_vehicle):
    """测试车辆创建和所有属性"""
    assert test_vehicle.vehicle_id is not None
    assert test_vehicle.type == 'SUV'
    assert test_vehicle.brand == 'Toyota'
    assert test_vehicle.model == 'RAV4'
    assert test_vehicle.color == '白色'
    assert float(test_vehicle.price_per_day) == 300.00
    assert test_vehicle.status == '可租用'
    assert test_vehicle.plate_number == '测试车牌A123'
    assert test_vehicle.created_at is not None
    assert test_vehicle.updated_at is not None

def test_vehicle_to_dict(test_vehicle):
    """测试车辆转字典功能"""
    vehicle_dict = test_vehicle.to_dict()
    assert vehicle_dict['vehicle_id'] == test_vehicle.vehicle_id
    assert vehicle_dict['type'] == 'SUV'
    assert vehicle_dict['brand'] == 'Toyota'
    assert vehicle_dict['model'] == 'RAV4'
    assert vehicle_dict['color'] == '白色'
    assert float(vehicle_dict['price_per_day']) == 300.00
    assert vehicle_dict['status'] == '可租用'
    assert vehicle_dict['plate_number'] == '测试车牌A123'

def test_vehicle_unique_plate_number(app):
    """测试车牌号唯一性约束"""
    with pytest.raises(Exception):
        vehicle = Vehicle(
            type='轿车',
            brand='Honda',
            model='Accord',
            color='黑色',
            price_per_day=250.00,
            status='可租用',
            plate_number='测试车牌A123'  # 使用已存在的车牌号
        )
        db.session.add(vehicle)
        db.session.commit() 