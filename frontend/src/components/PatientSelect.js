import React, { useEffect, useState } from 'react';
import { Select, Button, Modal, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import PatientForm from './PatientForm';
import { authFetch } from '../utils/api';

const PatientSelect = ({ value, onChange }) => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const res = await authFetch('/api/patients/');
      const data = await res.json();
      if (res.ok) setPatients(data);
      else message.error('Failed to fetch patients');
    } catch {
      message.error('Server error');
    }
    setLoading(false);
  };

  useEffect(() => { fetchPatients(); }, [showModal]);

  const handleAddPatient = async (patient) => {
    setShowModal(false);
    await fetchPatients();
    if (patient && patient.id) onChange(patient.id);
  };

  return (
    <>
      <Select
        showSearch
        value={value}
        onChange={onChange}
        loading={loading}
        placeholder="Select Patient"
        style={{ width: '100%' }}
        optionFilterProp="children"
        filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        }
        dropdownRender={menu => (
          <>
            {menu}
            <div style={{ display: 'flex', justifyContent: 'center', padding: 8 }}>
              <Button icon={<PlusOutlined />} type="link" onClick={() => setShowModal(true)}>
                Add New Patient
              </Button>
            </div>
          </>
        )}
      >
        {patients.map(p => (
          <Select.Option key={p.id} value={p.id}>
            {p.name} (ID: {p.id})
          </Select.Option>
        ))}
      </Select>
      <Modal
        open={showModal}
        onCancel={() => setShowModal(false)}
        footer={null}
        destroyOnClose
        title="Add New Patient"
      >
        <PatientForm onSubmit={handleAddPatient} onCancel={() => setShowModal(false)} />
      </Modal>
    </>
  );
};

export default PatientSelect;
