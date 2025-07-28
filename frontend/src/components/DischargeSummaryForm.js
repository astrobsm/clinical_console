
import React, { useState } from 'react';
import { Form, Input, Button, Card, Drawer, message, Typography } from 'antd';

const DischargeSummaryForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = async (values) => {
    setLoading(true);
    try {
      await onSubmit(values);
      form.resetFields();
      // Only show success if parent does not show it
      if (!onClose) message.success('Discharge summary saved!');
      if (onClose) onClose();
    } catch (err) {
      message.error(err?.message || 'Failed to save discharge summary');
    }
    setLoading(false);
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{ summary_text: initial?.summary_text || '' }}
      onFinish={handleFinish}
    >
      <Form.Item name="summary_text" label="Discharge Summary" rules={[{ required: true, message: 'Please enter summary' }]}> 
        <Input.TextArea rows={6} placeholder="Discharge Summary" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" size="large" loading={loading} style={{ width: 140, marginRight: 8, borderRadius: 24, fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}>Save</Button>
        {onCancel && <Button onClick={onCancel} size="large" style={{ borderRadius: 24 }}>Cancel</Button>}
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Discharge Summary"
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
      <Typography.Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>Discharge Summary</Typography.Title>
      {formContent}
    </Card>
  );
};

export default DischargeSummaryForm;
