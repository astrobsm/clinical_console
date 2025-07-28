
import React from 'react';
import { Card, Drawer, Typography } from 'antd';

const Assessments = ({ visible = true, onClose }) => {
  const isMobile = window.innerWidth < 700;
  const content = (
    <div>
      <Typography.Title level={3} style={{ marginBottom: 16 }}>Assessments</Typography.Title>
      <Typography.Paragraph>View and take clinical assessments here.</Typography.Paragraph>
    </div>
  );
  if (isMobile) {
    return (
      <Drawer
        title="Assessments"
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

export default Assessments;
