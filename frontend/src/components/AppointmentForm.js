import React, { useState } from 'react';
import { Form, Input, DatePicker, Button, Select, Drawer, Card, message } from 'antd';
import dayjs from 'dayjs';

const AppointmentForm = ({ onSubmit, initial, onCancel, visible = true, onClose, patients }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = (values) => {
    setLoading(true);
    const data = {
      ...values,
      date: values.date ? values.date.format('YYYY-MM-DDTHH:mm') : '',
    };
    onSubmit(data);
    setLoading(false);
    message.success('Appointment saved successfully!');
    if (onClose) onClose();
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{
        ...initial,
        date: initial?.date ? dayjs(initial.date) : null,
        patient_id: initial?.patient_id || undefined,
        purpose: initial?.purpose || '',
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Please select patient' }]}> 
        <Select placeholder="Select Patient" size="large" showSearch optionFilterProp="children">
          {patients.map(p => <Select.Option key={p.id} value={p.id}>{p.name}</Select.Option>)}
        </Select>
      </Form.Item>
      <Form.Item name="date" label="Date & Time" rules={[{ required: true, message: 'Please select date and time' }]}> 
        <DatePicker showTime format="YYYY-MM-DD HH:mm" style={{ width: '100%' }} size="large" />
      </Form.Item>
      <Form.Item name="purpose" label="Purpose" rules={[{ required: true, message: 'Please enter purpose' }]}> 
        <Input placeholder="Purpose" size="large" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" size="large" loading={loading} style={{ width: 120, borderRadius: 24, fontWeight: 600 }}>Save</Button>
        <Button type="link" onClick={onCancel} style={{ marginLeft: 8 }}>Cancel</Button>
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Appointment"
        placement="right"
        closable={true}
        onClose={onClose || onCancel}
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

export default AppointmentForm;
