
import React, { useEffect, useState } from 'react';
import { Button, message } from 'antd';
import logo from '../clinical_console.png';
import { authFetch } from '../utils/api';
import WoundCareForm from '../components/WoundCareForm';

const WoundCare = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [comorbidities, setComorbidities] = useState([]);

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await authFetch('/api/wound-care/');
      setItems(data);
    } catch (err) {
      setError('Server error');
    }
    setLoading(false);
  };

  const fetchComorbidities = async () => {
    // Replace with actual API endpoint for comorbidities
    try {
      const data = await authFetch('/api/comorbidities/');
      setComorbidities(data.map(c => ({ label: c.name, value: c.id })));
    } catch {
      setComorbidities([]);
    }
  };

  useEffect(() => {
    fetchItems();
    fetchComorbidities();
  }, []);

  const handleAdd = () => {
    setEditItem(null);
    setShowForm(true);
  };
  const handleEdit = (item) => {
    setEditItem(item);
    setShowForm(true);
  };
  const handleFormSubmit = async (form) => {
    try {
      if (editItem) {
        await authFetch(`/api/wound-care/${editItem.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form),
        });
      } else {
        await authFetch('/api/wound-care/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form),
        });
      }
      setShowForm(false);
      fetchItems();
      message.success('Wound care plan saved!');
    } catch (err) {
      message.error(err?.message || 'Failed to save wound care plan');
    }
  };

  return (
    <div>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <h2 style={{ textAlign: 'center' }}>Wound Care</h2>
      <Button type="primary" onClick={handleAdd} style={{ marginBottom: 16, background: '#38b000', borderColor: '#38b000', fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}>
        Add Wound Care Plan
      </Button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? <p>Loading...</p> : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>Patient</th>
              <th>Phase</th>
              <th>Dressing Protocol</th>
              <th>Wound Dimensions (cm)</th>
              <th>Clinical Photographs</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map(i => (
              <tr key={i.id}>
                <td>{i.patient_id}</td>
                <td>{i.phase}</td>
                <td>{i.dressing_protocol}</td>
                <td>
                  {i.length_cm && i.width_cm && i.depth_cm
                    ? `${i.length_cm} x ${i.width_cm} x ${i.depth_cm}`
                    : 'N/A'}
                </td>
                <td>
                  {i.images
                    ? i.images.split(',').map((img, idx) => (
                        <a key={idx} href={img} target="_blank" rel="noopener noreferrer">Photo {idx + 1}</a>
                      ))
                    : 'No images'}
                </td>
                <td>{i.date ? i.date.split('T')[0] : ''}</td>
                <td>
                  <Button size="small" onClick={() => handleEdit(i)}>Edit</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {showForm && (
        <WoundCareForm
          visible={showForm}
          onSubmit={handleFormSubmit}
          onCancel={() => setShowForm(false)}
          onClose={() => setShowForm(false)}
          initial={editItem}
          comorbiditiesOptions={comorbidities}
          enableWoundProgress={true}
        />
      )}
    </div>
  );
};

export default WoundCare;
