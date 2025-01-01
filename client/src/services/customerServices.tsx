import { message } from "antd";

const API_BASE_URL = "http://localhost:5000/api";

// 获取客户列表
export const fetchAllCustomers = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/customers`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "获取客户列表失败");
    }
    const data = await response.json();
    return data.data;
  } catch (error: any) {
    message.error("获取客户列表失败：" + error.message);
    throw error;
  }
};

// 根据 ID 获取客户信息
export const fetchCustomerById = async (customer_id: number) => {
  try {
    const response = await fetch(`${API_BASE_URL}/customers/${customer_id}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "获取客户信息失败");
    }
    const data = await response.json();
    return data.data;
  } catch (error: any) {
    message.error("获取客户信息失败：" + error.message);
    throw error;
  }
};

// 删除客户
export const deleteCustomer = async (customer_id: number) => {
  try {
    const response = await fetch(`${API_BASE_URL}/customers/${customer_id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "删除客户失败");
    }
    message.success("客户删除成功");
  } catch (error: any) {
    message.error("客户删除失败：" + error.message);
    throw error;
  }
};

// 创建客户
export const createCustomer = async (values: any) => {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "创建客户失败");
    }
    message.success("客户创建成功");
  } catch (error: any) {
    message.error("客户创建失败：" + error.message);
    throw error;
  }
};

// 更新客户信息
export const updateCustomer = async (customer_id: number, values: any) => {
  try {
    const response = await fetch(`${API_BASE_URL}/customers/${customer_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "更新客户信息失败");
    }
    message.success("客户信息更新成功");
  } catch (error: any) {
    message.error("更新客户信息失败：" + error.message);
    throw error;
  }
};