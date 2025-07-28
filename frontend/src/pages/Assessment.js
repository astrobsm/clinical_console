import React, { useEffect, useState } from 'react';
import AssessmentForm from '../components/AssessmentForm';
import { authFetch } from '../utils/api';

const Assessment = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [error, setError] = useState('');

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await authFetch('/api/assessments/');
      const data = await res.json();
      if (res.ok) setItems(data);
      else setError(data.msg || 'Failed to fetch assessments');
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
    const res = await authFetch(`/api/assessments/${id}`, { method: 'DELETE' });
    if (res.ok) fetchItems();
  };
  const handleFormSubmit = async (form) => {
    const method = editItem ? 'PUT' : 'POST';
    const url = editItem ? `/api/assessments/${editItem.id}` : '/api/assessments/';
    const res = await authFetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    if (res.ok) { setShowForm(false); fetchItems(); }
  };

  return (
    <div>
      <h2>Assessments</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? <p>Loading...</p> : (
        <>
          <button onClick={handleAdd} style={{ marginBottom: 16 }}>Add Assessment</button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr><th>Title</th><th>Description</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {items.map(i => (
                <tr key={i.id}>
                  <td>{i.title}</td>
                  <td>{i.description}</td>
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
          <AssessmentForm
            initial={editItem}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}
    </div>
  );
};

export default Assessment;
