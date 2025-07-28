import React, { useState } from 'react';
import './App.css';

import PageBackground from './components/PageBackground';

import { Button } from 'antd';

import AppLayout from './components/AppLayout';
import Notifications from './components/Notifications';
import AssessmentsComponent from './components/Assessments';


import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Appointments from './pages/Appointments';

import Login from './pages/Login';
import Register from './pages/Register';
import Clinical from './pages/Clinical';
import Diagnosis from './pages/Diagnosis';
import Treatment from './pages/Treatment';
import LabInvestigation from './pages/LabInvestigation';
import ImagingInvestigation from './pages/ImagingInvestigation';
import WoundCare from './pages/WoundCare';
import SurgeryBooking from './pages/SurgeryBooking';
import NotificationsPage from './pages/Notifications';
import AcademicEvent from './pages/AcademicEvent';
import Assessment from './pages/Assessment';
import CBT from './pages/CBT';
import Discharge from './pages/Discharge';
import DischargeSummary from './pages/DischargeSummary';
import Score from './pages/Score';





function App() {
  const [selected, setSelected] = useState('dashboard');
  const [auth, setAuth] = useState(() => {
    // Try to load token from localStorage
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    return token && user ? { token, user: JSON.parse(user) } : null;
  });
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = (data) => {
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    setAuth({ token: data.access_token, user: data.user });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setAuth(null);
  };

  const handleSwitchToRegister = () => setShowRegister(true);
  const handleSwitchToLogin = () => setShowRegister(false);


  let PageComponent;
  switch (selected) {
    case 'patients':
      PageComponent = Patients;
      break;
    case 'appointments':
      PageComponent = Appointments;
      break;
    case 'clinical':
      PageComponent = Clinical;
      break;
    case 'diagnosis':
      PageComponent = Diagnosis;
      break;
    case 'treatment':
      PageComponent = Treatment;
      break;
    case 'lab':
      PageComponent = LabInvestigation;
      break;
    case 'imaging':
      PageComponent = ImagingInvestigation;
      break;
    case 'woundcare':
      PageComponent = WoundCare;
      break;
    case 'surgery':
      PageComponent = SurgeryBooking;
      break;
    case 'notifications':
      PageComponent = NotificationsPage;
      break;
    case 'events':
      PageComponent = AcademicEvent;
      break;
    case 'assessments':
      PageComponent = Assessment;
      break;
    case 'cbt':
      PageComponent = CBT;
      break;
    case 'discharge':
      PageComponent = Discharge;
      break;
    case 'discharge_summary':
      PageComponent = DischargeSummary;
      break;
    case 'score':
      PageComponent = Score;
      break;
    case 'dashboard':
    default:
      PageComponent = Dashboard;
  }



  if (!auth) {
    if (showRegister) {
      return (
        <PageBackground>
          <Register onRegister={handleSwitchToLogin} onSwitchToLogin={handleSwitchToLogin} />
        </PageBackground>
      );
    }
    return (
      <PageBackground>
        <Login onLogin={handleLogin} onSwitchToRegister={handleSwitchToRegister} />
      </PageBackground>
    );
  }

  // Role-based UI helpers
  const userRole = auth.user?.role;
  const canEditPatients = ['consultant', 'admin', 'senior_registrar'].includes(userRole);

  const handleMenuSelect = ({ key }) => {
    setSelected(key);
  };

  return (
    <PageBackground>
      <AppLayout selected={selected} onMenuSelect={handleMenuSelect}>
        <div style={{ position: 'absolute', top: 16, right: 32, zIndex: 200 }}>
          <Notifications />
        </div>
        {/* Assessments page uses custom component */}
        {selected === 'assessments' ? (
          <AssessmentsComponent />
        ) : (
          <PageComponent canEdit={canEditPatients} userRole={userRole} />
        )}
        <Button type="primary" danger style={{ marginTop: 32 }} onClick={handleLogout}>Logout</Button>
      </AppLayout>
    </PageBackground>
  );
}

export default App;
