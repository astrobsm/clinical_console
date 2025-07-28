import React, { useEffect, useState } from 'react';
import logo from '../clinical_console.png';
import SurgeryBookingForm from '../components/SurgeryBookingForm';
import { authFetch } from '../utils/api';

const SurgeryBooking = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [error, setError] = useState('');

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await authFetch('/api/surgery-bookings/');
      const data = await res.json();
      if (res.ok) setItems(data);
      else setError(data.msg || 'Failed to fetch surgery bookings');
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
    const res = await authFetch(`/api/surgery-bookings/${id}`, { method: 'DELETE' });
    if (res.ok) fetchItems();
  };
  const handleFormSubmit = async (form) => {
    const method = editItem ? 'PUT' : 'POST';
    const url = editItem ? `/api/surgery-bookings/${editItem.id}` : '/api/surgery-bookings/';
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
      <h2 style={{ textAlign: 'center' }}>Surgery Bookings</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? <p>Loading...</p> : (
        <>
          <button onClick={handleAdd} style={{ marginBottom: 16 }}>Add Surgery Booking</button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Patient</th>
                <th>Surgery Type</th>
                <th>Date Booked</th>
                <th>Scheduled Date</th>
                <th>Admission Type</th>
                <th>Ward</th>
                <th>Images</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map(i => (
                <tr key={i.id}>
                  <td>{i.patient_id}</td>
                  <td>{i.surgery_type}</td>
                  <td>{i.date_booked}</td>
                  <td>{i.scheduled_date}</td>
                  <td>{i.admission_type === 'day_case' ? 'Day Case' : i.admission_type === 'inpatient' ? 'Inpatient' : ''}</td>
                  <td>{i.ward || ''}</td>
                  <td>{i.clinical_images ? i.clinical_images.split(',').length : 0}</td>
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
          <SurgeryBookingForm
            initial={editItem}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
            onClose={() => setShowForm(false)}
          />
        </div>
      )}
    </div>
  );
};

export default SurgeryBooking;
