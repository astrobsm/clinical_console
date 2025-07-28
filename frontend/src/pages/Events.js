
import React, { useState } from 'react';
import logo from '../clinical_console.png';
import { Card, Drawer, Typography, Button, message } from 'antd';
import { authFetch } from '../utils/api';

const Events = ({ visible = true, onClose }) => {
  const isMobile = window.innerWidth < 700;
  const [loading, setLoading] = useState(false);
  const handleAutoGenerate = async () => {
    setLoading(true);
    try {
      const data = await authFetch('/api/academic-events/auto-generate', {
        method: 'POST',
        body: JSON.stringify({
          topics: [
            'DIABETIC FOOT',
            'CHRONIC LEG ULCER',
            'NEUROFIBROMATOSIS'
          ],
          meet_link: 'https://meet.google.com/ojm-qqae-wfo'
        })
      });
      message.success(data.msg || 'Events auto-generated');
    } catch (err) {
      message.error(err.message || 'Failed to auto-generate events');
    }
    setLoading(false);
  };
  const content = (
    <div>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <Typography.Title level={3} style={{ marginBottom: 16, textAlign: 'center' }}>Academic Events</Typography.Title>
      <Typography.Paragraph>View and upload unit academic events here.</Typography.Paragraph>
      <Button type="primary" onClick={handleAutoGenerate} loading={loading} style={{ marginBottom: 16 }}>
        Auto-generate Weekly Events
      </Button>
    </div>
  );
  if (isMobile) {
    return (
      <Drawer
        title="Academic Events"
        placement="right"
        closable={true}
        onClose={onClose}
        open={visible}
        width={window.innerWidth - 32}
        styles={{ body: { padding: 16 } }}
      >
        {content}
      </Drawer>
    );
  }
  return (
    <Card style={{ maxWidth: 600, margin: '0 auto', boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      {content}
    </Card>
  );
};

export default Events;
