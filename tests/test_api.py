import pytest
from datetime import datetime

def test_get_vehicles(client, test_vehicle):
    """测试获取车辆列表"""
    response = client.get('/api/vehicles')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    vehicle = data[0]
    assert vehicle['vehicle_id'] == test_vehicle.vehicle_id
    assert vehicle['type'] == 'SUV'
    assert vehicle['brand'] == 'Toyota'
    assert vehicle['model'] == 'RAV4'
    assert vehicle['color'] == '白色'
    assert float(vehicle['price_per_day']) == 300.00
    assert vehicle['status'] == '可租用'
    assert vehicle['plate_number'] == '测试车牌A123'

def test_get_customers(client, test_customer):
    """测试获取客户列表"""
    response = client.get('/api/customers')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    customer = data[0]
    assert customer['customer_id'] == test_customer.customer_id
    assert customer['name'] == '张三'
    assert customer['phone'] == '13800138000'
    assert customer['address'] == '北京市海淀区'
    assert customer['id_card'] == '110101199001011234'

def test_get_rentals(client, test_rental):
    """测试获取租赁列表"""
    response = client.get('/api/rentals')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    rental = data[0]
    assert rental['rental_id'] == test_rental.rental_id
    assert rental['vehicle_id'] == test_rental.vehicle_id
    assert rental['customer_id'] == test_rental.customer_id
    assert rental['duration_days'] == 3
    assert float(rental['total_fee']) == 900.00
    assert rental['status'] == '进行中' 