

import React, { useState } from 'react';
import logo from '../clinical_console.png';
import { Form, Input, Button, Card, Drawer, Select, message, Typography } from 'antd';
import { authFetch } from '../utils/api';

const roles = [
  { value: '', label: 'Select Role' },
  { value: 'consultant', label: 'Consultant' },
  { value: 'senior_registrar', label: 'Senior Registrar' },
  { value: 'registrar', label: 'Registrar' },
  { value: 'house_officer', label: 'House Officer' },
  { value: 'admin', label: 'Admin' }
];

const Login = ({ onLogin, onSwitchToRegister, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = async (values) => {
    setLoading(true);
    try {
      const data = await authFetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      if (data && data.access_token) {
        localStorage.setItem('jwt', data.access_token); // Store JWT for authFetch
        onLogin(data); // This will update auth and show dashboard
      } else {
        message.error(data.msg || 'Invalid credentials');
      }
    } catch (err) {
      message.error(err?.message || 'Server error');
    }
    setLoading(false);
  };

  const formContent = (
    <>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <Typography.Title level={2} style={{ textAlign: 'center', marginBottom: 0, color: '#38b000', letterSpacing: 1 }}>CLINICAL CONSOLE</Typography.Title>
      <Typography.Text style={{ display: 'block', textAlign: 'center', marginBottom: 24, color: '#888', fontWeight: 500, fontSize: 16 }}>powered by astrobsm</Typography.Text>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleFinish}
        style={{ maxWidth: 400, margin: '0 auto' }}
        initialValues={{ role: '' }}
      >
        <Typography.Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>Login</Typography.Title>
        <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email', message: 'Please enter a valid email' }]}> 
          <Input placeholder="Email" size="large" />
        </Form.Item>
        <Form.Item name="password" label="Password" rules={[{ required: true, message: 'Please enter password' }]}> 
          <Input.Password placeholder="Password" size="large" />
        </Form.Item>
        <Form.Item name="role" label="Role" rules={[{ required: true, message: 'Please select role' }]}> 
          <Select placeholder="Select Role" size="large">
            {roles.map(r => <Select.Option key={r.value} value={r.value}>{r.label}</Select.Option>)}
          </Select>
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" size="large" loading={loading} style={{ width: 140, marginRight: 8, borderRadius: 24, fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}>Login</Button>
          <Button type="link" onClick={onSwitchToRegister} style={{ color: '#38b000', fontWeight: 600 }}>Don't have an account? Register</Button>
        </Form.Item>
      </Form>
    </>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Login"
        placement="right"
        closable={true}
        onClose={onClose || onSwitchToRegister}
        open={visible}
        width={window.innerWidth - 32}
        styles={{ body: { padding: 16 } }}
      >
        {formContent}
      </Drawer>
    );
  }
  return (
    <Card style={{ maxWidth: 500, margin: '0 auto', boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      {formContent}
    </Card>
  );
};

export default Login;
