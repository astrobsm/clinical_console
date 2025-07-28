

import React, { useEffect, useState } from 'react';
import AppointmentForm from '../components/AppointmentForm';
import { authFetch } from '../utils/api';
import { Button } from 'antd';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editAppointment, setEditAppointment] = useState(null);
  const [error, setError] = useState('');

  const fetchAppointments = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await authFetch('/api/appointments/');
      setAppointments(data);
    } catch (err) {
      setError('Server error');
    }
    setLoading(false);
  };

  const fetchPatients = async () => {
    try {
      const data = await authFetch('/api/patients/');
      setPatients(data);
    } catch {}
  };

  useEffect(() => {
    fetchAppointments();
    fetchPatients();
  }, []);

  const handleAdd = () => {
    setEditAppointment(null);
    setShowForm(true);
  };

  const handleEdit = (appt) => {
    setEditAppointment(appt);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this appointment?')) return;
    try {
      await authFetch(`/api/appointments/${id}`, {
        method: 'DELETE',
      });
      fetchAppointments();
    } catch (err) {
      alert('Delete failed');
    }
  };

  const handleFormSubmit = async (form) => {
    const method = editAppointment ? 'PUT' : 'POST';
    const url = editAppointment ? `/api/appointments/${editAppointment.id}` : '/api/appointments/';
    try {
      await authFetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      setShowForm(false);
      fetchAppointments();
    } catch (err) {
      alert('Save failed');
    }
  };

  return (
    <div>
      <h2>Appointments</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? <p>Loading...</p> : (
        <>
          <Button
            type="primary"
            shape="round"
            size="large"
            onClick={handleAdd}
            style={{ marginBottom: 16, background: '#38b000', borderColor: '#38b000', fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}
          >
            Add Appointment
          </Button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Patient</th>
                <th>Date</th>
                <th>Purpose</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map(a => {
                const patient = patients.find(p => p.id === a.patient_id);
                return (
                  <tr key={a.id}>
                    <td>{patient ? patient.name : a.patient_id}</td>
                    <td>{a.date ? a.date.replace('T', ' ').slice(0, 16) : ''}</td>
                    <td>{a.purpose}</td>
                    <td>
                    <Button
                      type="default"
                      shape="round"
                      size="small"
                      onClick={() => handleEdit(a)}
                      style={{ fontWeight: 500, marginRight: 8 }}
                    >
                      Edit
                    </Button>
                    <Button
                      type="primary"
                      danger
                      shape="round"
                      size="small"
                      onClick={() => handleDelete(a.id)}
                      style={{ fontWeight: 500 }}
                    >
                      Delete
                    </Button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </>
      )}
      {showForm && (
        <div style={{ marginTop: 24 }}>
          <AppointmentForm
            initial={editAppointment}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
            patients={patients}
          />
        </div>
      )}
    </div>
  );
};

export default Appointments;
