
import React, { useEffect, useState } from 'react';
import logo from '../clinical_console.png';
import { Card, Statistic, Row, Col, Grid } from 'antd';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { authFetch } from '../utils/api';

const Dashboard = () => {
  const [stats, setStats] = useState({ patients: 0, appointments: 0, notifications: 0, assessments: 0 });
  const [patientTrends, setPatientTrends] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    // Fetch stats
    authFetch('/api/dashboard/summary')
      .then(data => setStats(data));
    // Fetch patient trends
    authFetch('/api/dashboard/patient_trends')
      .then(data => setPatientTrends(data));
    // Fetch recent activity
    authFetch('/api/dashboard/recent_activity')
      .then(data => setRecentActivity(data));
  }, []);

  const screens = Grid.useBreakpoint();
  // Defensive: ensure patientTrends is always an array
  const safePatientTrends = Array.isArray(patientTrends) ? patientTrends : [];
  // Defensive: ensure recentActivity is always an array
  const safeRecentActivity = Array.isArray(recentActivity) ? recentActivity : [];
  return (
    <div>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <h2 style={{ marginBottom: 24, textAlign: 'center' }}>Dashboard</h2>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={12} sm={12} md={6}><Card><Statistic title="Patients" value={stats.patients} /></Card></Col>
        <Col xs={12} sm={12} md={6}><Card><Statistic title="Appointments" value={stats.appointments} /></Card></Col>
        <Col xs={12} sm={12} md={6}><Card><Statistic title="Notifications" value={stats.notifications} /></Card></Col>
        <Col xs={12} sm={12} md={6}><Card><Statistic title="Assessments" value={stats.assessments} /></Card></Col>
      </Row>
      <Row gutter={[16, 16]}>
        <Col xs={24} md={16}>
          <Card title="Patient Trends (Last 6 Months)" style={{ height: screens.xs ? 300 : 350 }}>
            <ResponsiveContainer width="100%" height={screens.xs ? 180 : 250}>
              <LineChart data={safePatientTrends} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="patients" stroke="#38b000" activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card title="Recent Activity" style={{ height: screens.xs ? 200 : 350, overflowY: 'auto' }}>
            <ul style={{ padding: 0, listStyle: 'none' }}>
              {safeRecentActivity.length === 0 ? <li>No recent activity.</li> : safeRecentActivity.map((a, i) => (
                <li key={i} style={{ marginBottom: 12 }}>
                  <span style={{ fontWeight: 500 }}>{a.type}:</span> {a.message}
                  <div style={{ fontSize: 12, color: '#888' }}>{a.time}</div>
                </li>
              ))}
            </ul>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
