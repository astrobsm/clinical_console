import React, { useEffect, useState } from 'react';
import logo from '../clinical_console.png';
import ClinicalForm from '../components/ClinicalForm';
import { authFetch } from '../utils/api';
import { Button } from 'antd';

const Clinical = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [error, setError] = useState('');

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await authFetch('/api/clinical/evaluations');
      setItems(data);
    } catch (err) {
      setError('Server error');
    }
    setLoading(false);
  };

  useEffect(() => { fetchItems(); }, []);

  const handleAdd = () => { setEditItem(null); setShowForm(true); };
  const handleEdit = (item) => { setEditItem(item); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!window.confirm('Delete?')) return;
    await authFetch(`/api/clinical/evaluations/${id}`, { method: 'DELETE' });
    fetchItems();
  };
  const handleFormSubmit = async (form) => {
    const method = editItem ? 'PUT' : 'POST';
    const url = editItem ? `/api/clinical/evaluations/${editItem.id}` : '/api/clinical/evaluations';
    await authFetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    setShowForm(false); fetchItems();
  };

  return (
    <div>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <h2 style={{ textAlign: 'center' }}>Clinical Evaluations</h2>
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
            Add Clinical Evaluation
          </Button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr><th>Patient</th><th>Summary</th><th>Date</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {items.map(i => (
                <tr key={i.id}>
                  <td>{i.patient_id}</td>
                  <td>{i.summary}</td>
                  <td>{i.date}</td>
                  <td>
                    <Button
                      type="default"
                      shape="round"
                      size="small"
                      onClick={() => handleEdit(i)}
                      style={{ fontWeight: 500, marginRight: 8 }}
                    >
                      Edit
                    </Button>
                    <Button
                      type="primary"
                      danger
                      shape="round"
                      size="small"
                      onClick={() => handleDelete(i.id)}
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
          <ClinicalForm
            initial={editItem}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}
    </div>
  );
};

export default Clinical;
