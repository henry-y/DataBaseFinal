import pytest
from app.models import Customer

def test_customer_creation(test_customer):
    """测试客户创建和所有属性"""
    assert test_customer.customer_id is not None
    assert test_customer.name == '张三'
    assert test_customer.phone == '13800138000'
    assert test_customer.address == '北京市海淀区'
    assert test_customer.id_card == '110101199001011234'
    assert test_customer.created_at is not None
    assert test_customer.updated_at is not None

def test_customer_to_dict(test_customer):
    """测试客户转字典功能"""
    customer_dict = test_customer.to_dict()
    assert customer_dict['customer_id'] == test_customer.customer_id
    assert customer_dict['name'] == '张三'
    assert customer_dict['phone'] == '13800138000'
    assert customer_dict['address'] == '北京市海淀区'
    assert customer_dict['id_card'] == '110101199001011234'

def test_customer_unique_id_card(app):
    """测试身份证号唯一性约束"""
    with pytest.raises(Exception):
        customer = Customer(
            name='李四',
            phone='13900139000',
            address='北京市朝阳区',
            id_card='110101199001011234'  # 使用已存在的身份证号
        )
        db.session.add(customer)
        db.session.commit() 