import React, { useState } from 'react';
import { Form, Input, Button, DatePicker, Drawer, Card } from 'antd';
import dayjs from 'dayjs';
import PatientSelect from './PatientSelect';

const DiagnosisForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = (values) => {
    setLoading(true);
    const data = {
      ...values,
      date: values.date ? values.date.format('YYYY-MM-DD') : '',
    };
    onSubmit(data);
    setLoading(false);
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
        diagnosis: initial?.diagnosis || '',
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Please select patient' }]}> 
        <PatientSelect />
      </Form.Item>
      <Form.Item name="diagnosis" label="Diagnosis" rules={[{ required: true }]}> 
        <Input />
      </Form.Item>
      <Form.Item name="date" label="Date" rules={[{ required: true }]}> 
        <DatePicker style={{ width: '100%' }} />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>Save</Button>
        <Button type="link" onClick={onCancel}>Cancel</Button>
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Diagnosis"
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

export default DiagnosisForm;
