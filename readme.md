# 车辆租赁管理系统

一个基于Python + Flask + PostgreSQL的车辆租赁管理系统，包括车辆信息管理、租赁管理、客户管理等核心功能模块。

## 系统功能模块

### 车辆信息管理
- 车辆信息的添加、修改、删除和查询
- 车辆状态管理（可租用、已租出、维修中等）
- 车辆历史租赁记录查询

### 租赁管理
- 租赁订单的创建、修改和查询
- 租金计算和费用管理
- 租赁状态追踪（进行中、已完成、已取消等）
- 逾期管理和提醒

### 客户管理
- 客户信息的添加、修改和查询
- 客户租赁历史记录

## 技术栈

- 后端：Python 3.8+ + Flask 2.0+
- 数据库：PostgreSQL 12+
- API文档：Swagger/OpenAPI

## 数据库设计

### 车辆表 (vehicles)
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| vehicle_id | SERIAL | 车辆ID | PRIMARY KEY |
| type | VARCHAR(50) | 车辆类型(轿车/SUV/货车等) | NOT NULL |
| brand | VARCHAR(50) | 品牌 | NOT NULL |
| model | VARCHAR(50) | 型号 | NOT NULL |
| color | VARCHAR(20) | 颜色 | NOT NULL |
| price_per_day | DECIMAL(10,2) | 日租金(元) | NOT NULL |
| status | VARCHAR(20) | 状态(可租用/已租出/维修中) | NOT NULL |
| plate_number | VARCHAR(20) | 车牌号 | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | 创建时间 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 更新时间 | DEFAULT NOW() |

### 租赁表 (rentals)
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| rental_id | SERIAL | 租赁ID | PRIMARY KEY |
| vehicle_id | INTEGER | 车辆ID | FOREIGN KEY |
| customer_id | INTEGER | 客户ID | FOREIGN KEY |
| start_time | TIMESTAMP | 租赁开始时间 | NOT NULL |
| duration_days | INTEGER | 租赁天数 | NOT NULL |
| expected_return_time | TIMESTAMP | 预计归还时间 | NOT NULL |
| actual_return_time | TIMESTAMP | 实际归还时间 | NULL |
| total_fee | DECIMAL(10,2) | 租赁总费用 | NOT NULL |
| status | VARCHAR(20) | 状态(进行中/已完成/已取消) | NOT NULL |
| created_at | TIMESTAMP | 创建时间 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 更新时间 | DEFAULT NOW() |

### 客户表 (customers)
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| customer_id | SERIAL | 客户ID | PRIMARY KEY |
| name | VARCHAR(100) | 客户姓名 | NOT NULL |
| phone | VARCHAR(20) | 联系电话 | NOT NULL |
| address | TEXT | 居住地址 | NOT NULL |
| id_card | VARCHAR(18) | 身份证号 | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | 创建时间 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 更新时间 | DEFAULT NOW() |

## API接口设计

将提供RESTful API，包括：

### 车辆相关
- GET /api/vehicles - 获取车辆列表
- POST /api/vehicles - 添加新车辆
- GET /api/vehicles/{id} - 获取特定车辆信息
- PUT /api/vehicles/{id} - 更新车辆信息
- DELETE /api/vehicles/{id} - 删除车辆

### 租赁相关
- POST /api/rentals - 创建租赁订单
- GET /api/rentals/{id} - 获取租赁详情
- PUT /api/rentals/{id} - 更新租赁信息
- GET /api/rentals/customer/{customer_id} - 获取客户租赁历史

### 客户相关
- POST /api/customers - 新增客户
- GET /api/customers/{id} - 获取客户信息
- PUT /api/customers/{id} - 更新客户信息
- GET /api/customers/{id}/rentals - 获取客户租赁历史

## 部署要求

- Python 3.8+
- PostgreSQL 12+
- pip requirements将在requirements.txt中详细列出
