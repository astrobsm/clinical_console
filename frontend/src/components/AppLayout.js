import React, { useState } from 'react';
import { Layout, Menu, Drawer, Button, Grid } from 'antd';
import {
  HomeOutlined, UserOutlined, CalendarOutlined, NotificationOutlined
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;
const { useBreakpoint } = Grid;

const menuItems = [
  { key: 'dashboard', icon: <HomeOutlined />, label: 'Dashboard' },
  { key: 'patients', icon: <UserOutlined />, label: 'Patients' },
  { key: 'appointments', icon: <CalendarOutlined />, label: 'Appointments' },
  { key: 'clinical', icon: <UserOutlined />, label: 'Clinical Evaluations' },
  { key: 'diagnosis', icon: <UserOutlined />, label: 'Diagnoses' },
  { key: 'treatment', icon: <UserOutlined />, label: 'Treatment Plans' },
  { key: 'lab', icon: <UserOutlined />, label: 'Lab Investigations' },
  { key: 'imaging', icon: <UserOutlined />, label: 'Imaging Investigations' },
  { key: 'woundcare', icon: <UserOutlined />, label: 'Wound Care' },
  { key: 'surgery', icon: <UserOutlined />, label: 'Surgery Bookings' },
  { key: 'notifications', icon: <NotificationOutlined />, label: 'Notifications' },
  { key: 'events', icon: <UserOutlined />, label: 'Academic Events' },
  { key: 'assessments', icon: <UserOutlined />, label: 'Assessments' },
  { key: 'cbt', icon: <UserOutlined />, label: 'CBT Questions' },
  { key: 'discharge', icon: <UserOutlined />, label: 'Discharges' },
  { key: 'discharge_summary', icon: <UserOutlined />, label: 'Discharge Summaries' },
  { key: 'score', icon: <UserOutlined />, label: 'Scores' },
];

const AppLayout = ({ children, selected, onMenuSelect }) => {
  const screens = useBreakpoint();
  const [drawerVisible, setDrawerVisible] = useState(false);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {screens.md ? (
        <Sider breakpoint="md" collapsedWidth="0">
          <div className="logo" style={{ margin: 16, textAlign: 'center' }}>
            <div style={{ fontWeight: 700, fontSize: 22, color: '#38b000', letterSpacing: 1 }}>CLINICAL CONSOLE</div>
            <div style={{ color: '#888', fontWeight: 500, fontSize: 13 }}>powered by astrobsm</div>
          </div>
          <Menu
            theme="dark"
            mode="inline"
            items={menuItems}
            selectedKeys={[selected]}
            onClick={onMenuSelect}
          />
        </Sider>
      ) : (
        <>
          <Header style={{ background: '#fff', padding: 0 }}>
            <Button
              icon={<HomeOutlined />}
              onClick={() => setDrawerVisible(true)}
              style={{ margin: 16 }}
            />
            <span style={{ display: 'inline-block', marginLeft: 16 }}>
              <span style={{ fontWeight: 700, fontSize: 20, color: '#38b000', letterSpacing: 1 }}>CLINICAL CONSOLE</span>
              <span style={{ color: '#888', fontWeight: 500, fontSize: 13, marginLeft: 8 }}>powered by astrobsm</span>
            </span>
          </Header>
          <Drawer
            title={<span><span style={{ fontWeight: 700, fontSize: 20, color: '#38b000', letterSpacing: 1 }}>CLINICAL CONSOLE</span><br /><span style={{ color: '#888', fontWeight: 500, fontSize: 13 }}>powered by astrobsm</span></span>}
            placement="left"
            onClose={() => setDrawerVisible(false)}
            open={drawerVisible}
            styles={{ body: { padding: 0 } }}
          >
            <Menu
              mode="inline"
              items={menuItems}
              selectedKeys={[selected]}
              onClick={e => {
                setDrawerVisible(false);
                onMenuSelect && onMenuSelect(e);
              }}
            />
          </Drawer>
        </>
      )}
      <Layout>
        {!screens.md && <div style={{ height: 48 }} />} {/* Spacer for mobile header */}
        <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
