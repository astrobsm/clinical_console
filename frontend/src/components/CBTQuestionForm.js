import React, { useState } from 'react';
import { Form, Input, Button, Card, Drawer } from 'antd';

const CBTQuestionForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = (values) => {
    setLoading(true);
    onSubmit(values);
    setLoading(false);
    if (onClose) onClose();
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={initial || {}}
      onFinish={handleFinish}
    >
      <Form.Item name="question" label="Question" rules={[{ required: true }]}> 
        <Input.TextArea />
      </Form.Item>
      <Form.Item name="answer" label="Answer" rules={[{ required: true }]}> 
        <Input />
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
        title="CBT Question"
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

export default CBTQuestionForm;
