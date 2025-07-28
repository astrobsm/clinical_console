
import React, { useEffect, useState } from 'react';
import AcademicEventForm from '../components/AcademicEventForm';
import { authFetch } from '../utils/api';

const AcademicEvent = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [error, setError] = useState('');
  const [topicsInput, setTopicsInput] = useState('');
  const [autoGenLoading, setAutoGenLoading] = useState(false);

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await authFetch('/api/academic-events/');
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
    await authFetch(`/api/academic-events/${id}`, { method: 'DELETE' });
    fetchItems();
  };
  const handleFormSubmit = async (form) => {
    const method = editItem ? 'PUT' : 'POST';
    const url = editItem ? `/api/academic-events/${editItem.id}` : '/api/academic-events/';
    await authFetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    setShowForm(false); fetchItems();
  };

  // Auto-generate events for a list of topics
  const handleAutoGenerate = async () => {
    setAutoGenLoading(true);
    try {
      const topics = topicsInput.split(/,|\n/).map(t => t.trim()).filter(Boolean);
      await authFetch('/api/academic-events/auto-generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topics }),
      });
      setTopicsInput('');
      fetchItems();
    } catch (err) {
      setError('Failed to auto-generate events');
    }
    setAutoGenLoading(false);
  };

  return (
    <div>
      <h2>Academic Events</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <div style={{ margin: '16px 0', padding: 12, background: '#f6f6f6', borderRadius: 8 }}>
        <b>Auto-generate weekly events:</b>
        <div style={{ margin: '8px 0' }}>
          <textarea
            rows={3}
            value={topicsInput}
            onChange={e => setTopicsInput(e.target.value)}
            placeholder="Enter discussion topics, one per line or comma separated"
            style={{ width: '100%', marginBottom: 8 }}
          />
          <button onClick={handleAutoGenerate} disabled={autoGenLoading || !topicsInput.trim()}>
            {autoGenLoading ? 'Generating...' : 'Auto-generate Events'}
          </button>
        </div>
        <div style={{ fontSize: 13, color: '#555' }}>
          Events will be scheduled every Thursday 7–8pm, with automatic assignment of moderator (consultant) and presenter (registrar/senior registrar). Notifications will be sent to assigned users.
        </div>
      </div>
      {loading ? <p>Loading...</p> : (
        <>
          <button onClick={handleAdd} style={{ marginBottom: 16 }}>Add Academic Event</button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Event Date</th>
                <th>Topics</th>
                <th>Moderator</th>
                <th>Presenter</th>
                <th>Meet Link</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map(i => (
                <tr key={i.id}>
                  <td>{i.title}</td>
                  <td>{i.description}</td>
                  <td>{i.event_date}</td>
                  <td>{Array.isArray(i.topics) ? i.topics.join(', ') : i.topics}</td>
                  <td>{i.moderator_id || '-'}</td>
                  <td>{i.presenter_id || '-'}</td>
                  <td>{i.meet_link ? <a href={i.meet_link} target="_blank" rel="noopener noreferrer">Join</a> : '-'}</td>
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
          <AcademicEventForm
            initial={editItem}
            onSubmit={handleFormSubmit}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}
    </div>
  );
};

export default AcademicEvent;
