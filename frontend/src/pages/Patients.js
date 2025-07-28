
import React, { useEffect, useState } from 'react';
import PatientForm from '../components/PatientForm';
import { authFetch } from '../utils/api';
import { Button } from 'antd';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editPatient, setEditPatient] = useState(null);
  const [error, setError] = useState('');

  const fetchPatients = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await authFetch('/api/patients/');
      setPatients(data);
    } catch (err) {
      setError('Server error');
    }
    setLoading(false);
  };

  useEffect(() => { fetchPatients(); }, []);

  const handleAdd = () => {
    setEditPatient(null);
    setShowForm(true);
  };

  const handleEdit = (patient) => {
    setEditPatient(patient);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this patient?')) return;
    try {
      await authFetch(`/api/patients/${id}`, {
        method: 'DELETE',
      });
      fetchPatients();
    } catch (err) {
      alert('Delete failed');
    }
  };

  const handleFormSubmit = async (form) => {
    const method = editPatient ? 'PUT' : 'POST';
    const url = editPatient ? `/api/patients/${editPatient.id}` : '/api/patients/';
    try {
      await authFetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      setShowForm(false);
      fetchPatients();
    } catch (err) {
      alert('Save failed');
    }
  };

  return (
    <div>
      <img src={require('../clinical_console.png')} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <h2 style={{ textAlign: 'center' }}>Patients</h2>
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
            Add Patient
          </Button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Name</th>
                <th>DOB</th>
                <th>Gender</th>
                <th>Inpatient</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {patients.map(p => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>{p.dob || ''}</td>
                  <td>{p.gender}</td>
                  <td>{p.inpatient ? 'Yes' : 'No'}</td>
                  <td>
                    <Button
                      type="default"
                      shape="round"
                      size="small"
                      onClick={() => handleEdit(p)}
                      style={{ fontWeight: 500, marginRight: 8 }}
                    >
                      Edit
                    </Button>
                    <Button
                      type="primary"
                      danger
                      shape="round"
                      size="small"
                      onClick={() => handleDelete(p.id)}
                      style={{ fontWeight: 500 }}
                    >
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
      {showForm && (
        <div style={{ marginTop: 24 }}>
          <PatientForm
            initial={editPatient}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}
    </div>
  );
};

export default Patients;
