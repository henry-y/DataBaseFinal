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

def test_create_customer(client):
    """测试创建新客户"""
    data = {
        'name': '李四',
        'phone': '13900139000',
        'address': '北京市朝阳区',
        'id_card': '110101199001011235'
    }
    response = client.post('/api/customers', json=data)
    assert response.status_code == 201
    result = response.get_json()
    assert result['name'] == '李四'
    assert result['phone'] == '13900139000'

def test_create_rental(client, test_vehicle, test_customer):
    """测试创建新租赁"""
    data = {
        'vehicle_id': test_vehicle.vehicle_id,
        'customer_id': test_customer.customer_id,
        'duration_days': 5
    }
    response = client.post('/api/rentals', json=data)
    assert response.status_code == 201
    result = response.get_json()
    assert result['vehicle_id'] == test_vehicle.vehicle_id
    assert result['customer_id'] == test_customer.customer_id
    assert result['duration_days'] == 5
    assert result['status'] == '进行中'

def test_create_vehicle(client):
    """测试创建新车辆"""
    data = {
        'type': '轿车',
        'brand': 'Honda',
        'model': 'Accord',
        'color': '黑色',
        'price_per_day': 250.00,
        'plate_number': '京C12345'
    }
    response = client.post('/api/vehicles', json=data)
    assert response.status_code == 201
    result = response.get_json()
    assert result['type'] == '轿车'
    assert result['brand'] == 'Honda'
    assert result['model'] == 'Accord'
    assert result['color'] == '黑色'
    assert float(result['price_per_day']) == 250.00
    assert result['status'] == '可租用'
    assert result['plate_number'] == '京C12345'

def test_create_vehicle_duplicate_plate(client, test_vehicle):
    """测试创建重复车牌号的车辆"""
    data = {
        'type': '轿车',
        'brand': 'Honda',
        'model': 'Accord',
        'color': '黑色',
        'price_per_day': 250.00,
        'plate_number': '测试车牌A123'  # 使用已存在的车牌号
    }
    response = client.post('/api/vehicles', json=data)
    assert response.status_code == 400
    assert 'error' in response.get_json() 

def test_get_vehicle_by_id(client, test_vehicle):
    """测试获取特定车辆"""
    response = client.get(f'/api/vehicles/{test_vehicle.vehicle_id}')
    assert response.status_code == 200
    vehicle = response.get_json()
    assert vehicle['vehicle_id'] == test_vehicle.vehicle_id
    assert vehicle['type'] == 'SUV'

def test_get_nonexistent_vehicle(client):
    """测试获取不存在的车辆"""
    response = client.get('/api/vehicles/9999')
    assert response.status_code == 404

def test_update_vehicle(client, test_vehicle):
    """测试更新车辆信息"""
    data = {
        'color': '红色',
        'price_per_day': 350.00
    }
    response = client.put(f'/api/vehicles/{test_vehicle.vehicle_id}', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['color'] == '红色'
    assert float(result['price_per_day']) == 350.00

def test_update_rented_vehicle_status(client, test_rental):
    """测试更新已租出车辆的状态"""
    data = {
        'status': '可租用'
    }
    response = client.put(f'/api/vehicles/{test_rental.vehicle_id}', json=data)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_delete_vehicle(client, test_vehicle):
    """测试删除车辆"""
    response = client.delete(f'/api/vehicles/{test_vehicle.vehicle_id}')
    assert response.status_code == 204

def test_delete_rented_vehicle(client, test_rental):
    """测试删除已租出的车辆"""
    response = client.delete(f'/api/vehicles/{test_rental.vehicle_id}')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_create_vehicle_invalid_price(client):
    """测试创建车辆时价格为负数"""
    data = {
        'type': '轿车',
        'brand': 'Honda',
        'model': 'Accord',
        'color': '黑色',
        'price_per_day': -250.00,  # 负数价格
        'plate_number': '京C12345'
    }
    response = client.post('/api/vehicles', json=data)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_create_vehicle_missing_fields(client):
    """测试创建车辆时缺少必要字段"""
    data = {
        'type': '轿车',
        'brand': 'Honda'
        # 缺少其他必要字段
    }
    response = client.post('/api/vehicles', json=data)
    assert response.status_code == 400
    assert 'Missing required field' in response.get_json()['error']

def test_update_vehicle_invalid_price(client, test_vehicle):
    """测试更新车辆时价格为负数"""
    data = {
        'price_per_day': -100.00
    }
    response = client.put(f'/api/vehicles/{test_vehicle.vehicle_id}', json=data)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_update_vehicle_invalid_status(client, test_vehicle):
    """测试更新车辆为无效状态"""
    data = {
        'status': '无效状态'
    }
    response = client.put(f'/api/vehicles/{test_vehicle.vehicle_id}', json=data)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_update_nonexistent_vehicle(client):
    """测试更新不存在的车辆"""
    data = {
        'color': '红色'
    }
    response = client.put('/api/vehicles/9999', json=data)
    assert response.status_code == 404

def test_delete_nonexistent_vehicle(client):
    """测试删除不存在的车辆"""
    response = client.delete('/api/vehicles/9999')
    assert response.status_code == 404