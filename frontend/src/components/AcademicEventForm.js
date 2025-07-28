import React, { useState } from 'react';
import { Form, Input, Button, DatePicker, Drawer, Card } from 'antd';
import dayjs from 'dayjs';

const AcademicEventForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = (values) => {
    setLoading(true);
    const data = {
      ...values,
      event_date: values.event_date ? values.event_date.format('YYYY-MM-DD') : '',
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
        event_date: initial?.event_date ? dayjs(initial.event_date) : null,
        title: initial?.title || '',
        description: initial?.description || '',
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="title" label="Title" rules={[{ required: true }]}> 
        <Input />
      </Form.Item>
      <Form.Item name="description" label="Description"> 
        <Input.TextArea />
      </Form.Item>
      <Form.Item name="topics" label="Discussion Topics (comma or newline separated)">
        <Input.TextArea placeholder="e.g. Topic 1, Topic 2, ..." autoSize={{ minRows: 2, maxRows: 6 }} />
      </Form.Item>
      <Form.Item name="event_date" label="Event Date" rules={[{ required: true }]}> 
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
        title="Academic Event"
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

export default AcademicEventForm;
