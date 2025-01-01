import { message } from "antd";

const API_BASE_URL = "http://localhost:5000/api";

export const modifyAccount = async (user_id: number, values: any) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/${user_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: values.username,
        password: values.password,
      }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error);
    }
  } catch (error: any) {
    message.error("修改账号密码失败" + error.message);
    throw error;
  }
};