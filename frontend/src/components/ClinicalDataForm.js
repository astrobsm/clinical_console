
import React, { useState } from 'react';
import { Form, Input, Button, Card, Drawer, DatePicker, message, Typography } from 'antd';
import dayjs from 'dayjs';

const ClinicalDataForm = ({ type, onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const fields = {
    evaluation: [
      { name: 'summary', label: 'Clinical Evaluation Summary', type: 'textarea' }
    ],
    diagnosis: [
      { name: 'diagnosis', label: 'Diagnosis', type: 'text' }
    ],
    treatment: [
      { name: 'plan', label: 'Treatment Plan', type: 'textarea' }
    ],
    lab: [
      { name: 'investigation', label: 'Lab Investigation', type: 'text' },
      { name: 'result', label: 'Result', type: 'textarea' }
    ],
    imaging: [
      { name: 'investigation', label: 'Imaging Investigation', type: 'text' },
      { name: 'result', label: 'Result', type: 'textarea' }
    ],
    wound: [
      { name: 'plan', label: 'Wound Care Plan', type: 'textarea' }
    ],
    surgery: [
      { name: 'surgery_type', label: 'Surgery Type', type: 'text' },
      { name: 'scheduled_date', label: 'Scheduled Date', type: 'date' }
    ],
    appointment: [
      { name: 'date', label: 'Appointment Date', type: 'date' },
      { name: 'purpose', label: 'Purpose', type: 'text' }
    ]
  };

  const handleFinish = (values) => {
    setLoading(true);
    // Convert date fields to string
    const data = { ...values };
    fields[type]?.forEach(f => {
      if (f.type === 'date' && values[f.name]) {
        data[f.name] = dayjs(values[f.name]).format('YYYY-MM-DD');
      }
    });
    onSubmit(data);
    setLoading(false);
    message.success('Saved successfully!');
    if (onClose) onClose();
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{ ...initial }}
      onFinish={handleFinish}
    >
      {fields[type]?.map(f => (
        f.type === 'textarea' ? (
          <Form.Item key={f.name} name={f.name} label={f.label} rules={[{ required: true, message: `Please enter ${f.label.toLowerCase()}` }]}> 
            <Input.TextArea rows={4} placeholder={f.label} />
          </Form.Item>
        ) : f.type === 'date' ? (
          <Form.Item key={f.name} name={f.name} label={f.label} rules={[{ required: true, message: `Please select ${f.label.toLowerCase()}` }]}> 
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
        ) : (
          <Form.Item key={f.name} name={f.name} label={f.label} rules={[{ required: true, message: `Please enter ${f.label.toLowerCase()}` }]}> 
            <Input placeholder={f.label} />
          </Form.Item>
        )
      ))}
      <Form.Item>
        <Button type="primary" htmlType="submit" size="large" loading={loading} style={{ width: 140, marginRight: 8, borderRadius: 24, fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}>Save</Button>
        {onCancel && <Button onClick={onCancel} size="large" style={{ borderRadius: 24 }}>Cancel</Button>}
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title={fields[type]?.[0]?.label || 'Form'}
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
      <Typography.Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>{fields[type]?.[0]?.label || 'Form'}</Typography.Title>
      {formContent}
    </Card>
  );
};

export default ClinicalDataForm;
