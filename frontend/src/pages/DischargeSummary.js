import React, { useEffect, useState } from 'react';
import logo from '../clinical_console.png';
import DischargeSummaryForm from '../components/DischargeSummaryForm';
import { authFetch } from '../utils/api';

const DischargeSummary = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [error, setError] = useState('');

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await authFetch('/api/discharge-summaries/');
      const data = await res.json();
      if (res.ok) setItems(data);
      else setError(data.msg || 'Failed to fetch discharge summaries');
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
    const res = await authFetch(`/api/discharge-summaries/${id}`, { method: 'DELETE' });
    if (res.ok) fetchItems();
  };
  const handleFormSubmit = async (form) => {
    const method = editItem ? 'PUT' : 'POST';
    const url = editItem ? `/api/discharge-summaries/${editItem.id}` : '/api/discharge-summaries/';
    const res = await authFetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    if (res.ok) { setShowForm(false); fetchItems(); }
  };

  return (
    <div>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <h2 style={{ textAlign: 'center' }}>Discharge Summaries</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? <p>Loading...</p> : (
        <>
          <button onClick={handleAdd} style={{ marginBottom: 16 }}>Add Discharge Summary</button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr><th>Patient ID</th><th>Summary Date</th><th>Summary</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {items.map(i => (
                <tr key={i.id}>
                  <td>{i.patient_id}</td>
                  <td>{i.summary_date}</td>
                  <td>{i.summary}</td>
                  <td>
                    <button onClick={() => handleEdit(i)}>Edit</button>
                    <button onClick={() => handleDelete(i.id)} style={{ marginLeft: 8 }}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
      {showForm && (
        <div style={{ marginTop: 24 }}>
          <DischargeSummaryForm
            initial={editItem}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}
    </div>
  );
};

export default DischargeSummary;
