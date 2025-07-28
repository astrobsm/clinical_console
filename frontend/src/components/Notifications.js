import React, { useEffect, useState } from 'react';
import { authFetch } from '../utils/api';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const data = await authFetch('/api/notifications/');
      setNotifications(data);
    } catch (err) {
      setNotifications([]);
    }
    setLoading(false);
  };

  useEffect(() => { fetchNotifications(); }, []);

  const markRead = async (id) => {
    await authFetch(`/api/notifications/${id}/read`, {
      method: 'POST',
    });
    fetchNotifications();
  };

  return (
    <div>
      <h3>Notifications</h3>
      {loading ? <p>Loading...</p> : notifications.length === 0 ? <p>No notifications.</p> : (
        <ul>
          {notifications.map(n => (
            <li key={n.id} style={{ marginBottom: 8 }}>
              <span style={{ fontWeight: n.is_read ? 'normal' : 'bold' }}>{n.message}</span>
              {!n.is_read && <button style={{ marginLeft: 8 }} onClick={() => markRead(n.id)}>Mark as read</button>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Notifications;
