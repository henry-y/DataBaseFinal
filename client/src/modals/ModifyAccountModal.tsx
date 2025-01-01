import React from "react";
import { Modal, Form, Input, Button } from "antd";
import { ModifyAccountModalProps } from "../types";
import { modifyAccount } from "../services/userServices";

const ModifyAccountModal: React.FC<ModifyAccountModalProps> = ({
  user,
  visible,
  onCancel,
  onModifySuccess,
}) => {
  const [form] = Form.useForm();

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      await modifyAccount(user.user_id, values); // 调用父组件传递的回调函数
      form.resetFields(); // 重置表单
      onCancel(); // 关闭模态框
      onModifySuccess(); // 修改成功的回调
    } catch (error) {
      console.error("表单验证失败:", error);
    }
  };

  return (
    <Modal
      title="修改账号密码"
      open={visible}
      onCancel={onCancel}
      footer={[
        <Button key="cancel" onClick={onCancel}>
          取消
        </Button>,
        <Button key="submit" type="primary" onClick={handleSubmit}>
          提交
        </Button>,
      ]}
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{ username: user.username }}
      >
        <Form.Item
          label="用户名"
          name="username"
          rules={[
            { required: false, message: "请输入用户名" },
            { min: 3, message: "用户名至少 3 个字符" },
            { max: 20, message: "用户名最多 20 个字符" },
          ]}
        >
          <Input placeholder="用户名" />
        </Form.Item>
        <Form.Item
          label="旧密码"
          name="oldPassword"
          rules={[{ required: true, message: "请输入旧密码" }]}
        >
          <Input.Password placeholder="请输入旧密码" />
        </Form.Item>
        <Form.Item
          label="新密码"
          name="password"
          rules={[
            { required: true, message: "请输入新密码" },
            { min: 6, message: "密码至少 6 个字符" },
          ]}
        >
          <Input.Password placeholder="新密码" />
        </Form.Item>
        <Form.Item
          label="确认密码"
          name="confirmPassword"
          rules={[
            { required: true, message: "请确认密码" },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error("两次输入的密码不一致"));
              },
            }),
          ]}
        >
          <Input.Password placeholder="确认密码" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default ModifyAccountModal;