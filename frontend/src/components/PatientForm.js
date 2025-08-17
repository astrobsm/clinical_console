
import React, { useState, useEffect } from 'react';
import { Form, Input, DatePicker, Select, Button, Row, Col, Typography, Card, Space, Drawer, message } from 'antd';
import { UserOutlined, CalendarOutlined, TeamOutlined, PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { authFetch } from '../utils/api';


const PatientForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  // Helper to fetch users by role
  const fetchUsersByRole = async (role) => {
    try {
      const data = await authFetch(`/api/auth/users?role=${role}`);
      return data || [];
    } catch {
      return [];
    }
  };
  // Staff lists
  const [consultants, setConsultants] = useState([]);
  const [seniorRegistrars, setSeniorRegistrars] = useState([]);
  const [registrars, setRegistrars] = useState([]);
  const [houseOfficers, setHouseOfficers] = useState([]);

  // Auto-assign staff IDs on mount
  useEffect(() => {
    async function fetchStaffAndAssign() {
      // Fetch users for each role
      const [c, sr, r, ho] = await Promise.all([
        fetchUsersByRole('consultant'),
        fetchUsersByRole('senior_registrar'),
        fetchUsersByRole('registrar'),
        fetchUsersByRole('house_officer')
      ]);
      setConsultants(c);
      setSeniorRegistrars(sr);
      setRegistrars(r);
      setHouseOfficers(ho);

      // Fetch all patients
      let patients = [];
      try {
        patients = await authFetch('/api/patients') || [];
      } catch {}

      // Helper: get user with fewest patients for a role
      function getLeastLoadedUser(users, roleKey) {
        if (!users.length) return undefined;
        // Count patients per user
        const counts = {};
        users.forEach(u => { counts[u.id] = 0; });
        patients.forEach(p => {
          if (p[roleKey] && counts.hasOwnProperty(p[roleKey])) counts[p[roleKey]]++;
        });
        // Find user(s) with min count
        let min = Math.min(...Object.values(counts));
        let candidates = users.filter(u => counts[u.id] === min);
        // Pick the first candidate (could randomize for fairness)
        return candidates[0]?.id;
      }

      if (!initial) {
        form.setFieldsValue({
          consultant_id: getLeastLoadedUser(c, 'consultant_id'),
          senior_registrar_id: getLeastLoadedUser(sr, 'senior_registrar_id'),
          registrar_id: getLeastLoadedUser(r, 'registrar_id'),
          house_officer_id: getLeastLoadedUser(ho, 'house_officer_id')
        });
      }
    }
    fetchStaffAndAssign();
  }, [initial, form]);
  const [loading, setLoading] = useState(false);
  const [age, setAge] = useState('');
  const [coUnits, setCoUnits] = useState(initial?.co_units || [{ unit: '', consultant: '' }]);

  // Responsive: show Drawer on mobile, Card on desktop
  const isMobile = window.innerWidth < 700;

  // Calculate age from dob
  const handleDOBChange = (date) => {
    if (date) {
      const years = dayjs().diff(date, 'year');
      setAge(years);
    } else {
      setAge('');
    }
  };

  // Co-managing units handlers
  const handleCoUnitChange = (idx, field, value) => {
    const updated = coUnits.map((item, i) => i === idx ? { ...item, [field]: value } : item);
    setCoUnits(updated);
    form.setFieldsValue({ co_units: updated });
  };
  const addCoUnit = () => {
    const updated = [...coUnits, { unit: '', consultant: '' }];
    setCoUnits(updated);
    form.setFieldsValue({ co_units: updated });
  };
  const removeCoUnit = (idx) => {
    const updated = coUnits.filter((_, i) => i !== idx);
    setCoUnits(updated);
    form.setFieldsValue({ co_units: updated });
  };

  const handleFinish = (values) => {
    setLoading(true);
    const data = {
      ...values,
      dob: values.dob ? values.dob.format('YYYY-MM-DD') : '',
      age,
      co_units: coUnits
    };
    onSubmit(data);
    setLoading(false);
    message.success('Patient saved successfully!');
    if (onClose) onClose();
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{
        ...initial,
        dob: initial?.dob ? dayjs(initial.dob) : null,
        patient_type: initial?.inpatient ? 'inpatient' : 'outpatient',
        route_of_admission: initial?.route_of_admission || undefined,
        admitting_diagnosis: initial?.admitting_diagnosis || '',
        co_units: initial?.co_units || [{ unit: '', consultant: '' }],
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="name" label="Full Name" rules={[{ required: true, message: 'Please enter full name' }]}> 
        <Input prefix={<UserOutlined />} placeholder="Full Name" size="large" />
      </Form.Item>
      <Row gutter={12}>
        <Col xs={24} sm={12}>
          <Form.Item name="dob" label="Date of Birth" rules={[{ required: true, message: 'Please select date of birth' }]}> 
            <DatePicker style={{ width: '100%' }} size="large" format="YYYY-MM-DD" suffixIcon={<CalendarOutlined />} onChange={handleDOBChange} />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12}>
          <Form.Item label="Age (auto)" >
            <Input value={age} disabled size="large" placeholder="Age" />
          </Form.Item>
        </Col>
      </Row>
      <Form.Item name="gender" label="Gender" rules={[{ required: true, message: 'Please select gender' }]}> 
        <Select placeholder="Select Gender" size="large">
          <Select.Option value="male">Male</Select.Option>
          <Select.Option value="female">Female</Select.Option>
          <Select.Option value="other">Other</Select.Option>
        </Select>
      </Form.Item>
      <Form.Item name="patient_type" label="Patient Type" rules={[{ required: true, message: 'Please select patient type' }]}> 
        <Select size="large">
          <Select.Option value="inpatient">Inpatient</Select.Option>
          <Select.Option value="outpatient">Outpatient</Select.Option>
        </Select>
      </Form.Item>
      <Form.Item name="admitting_diagnosis" label="Admitting Diagnosis" rules={[{ required: true, message: 'Please enter admitting diagnosis' }]}> 
        <Input placeholder="Admitting Diagnosis" size="large" />
      </Form.Item>
      <Form.Item name="route_of_admission" label="Route of Admission" rules={[{ required: true, message: 'Please select route of admission' }]}> 
        <Select placeholder="Select Route" size="large">
          <Select.Option value="clinic">Clinic</Select.Option>
          <Select.Option value="emergency">Emergency</Select.Option>
          <Select.Option value="consult">Via Consult</Select.Option>
        </Select>
      </Form.Item>
      <Form.Item label="Other Co-managing Units">
        {coUnits.map((item, idx) => (
          <Space key={idx} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
            <Input
              placeholder="Unit Name"
              value={item.unit}
              onChange={e => handleCoUnitChange(idx, 'unit', e.target.value)}
              prefix={<TeamOutlined />}
              size="large"
              style={{ minWidth: 120 }}
            />
            <Input
              placeholder="Consultant Name"
              value={item.consultant}
              onChange={e => handleCoUnitChange(idx, 'consultant', e.target.value)}
              prefix={<UserOutlined />}
              size="large"
              style={{ minWidth: 120 }}
            />
            {coUnits.length > 1 && (
              <Button icon={<DeleteOutlined />} onClick={() => removeCoUnit(idx)} danger shape="circle" />
            )}
            {idx === coUnits.length - 1 && (
              <Button icon={<PlusOutlined />} onClick={addCoUnit} type="dashed" shape="circle" />
            )}
          </Space>
        ))}
      </Form.Item>
      {/* ...existing consultant/registrar fields... */}
      <Row gutter={12}>
        <Col xs={24} sm={12}>
          <Form.Item name="consultant_id" label="Consultant">
            <Select
              placeholder="Select Consultant"
              size="large"
              options={consultants.map(u => ({ label: u.name, value: u.id }))}
              allowClear
              showSearch
              optionFilterProp="label"
            />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12}>
          <Form.Item name="senior_registrar_id" label="Senior Registrar">
            <Select
              placeholder="Select Senior Registrar"
              size="large"
              options={seniorRegistrars.map(u => ({ label: u.name, value: u.id }))}
              allowClear
              showSearch
              optionFilterProp="label"
            />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={12}>
        <Col xs={24} sm={12}>
          <Form.Item name="registrar_id" label="Registrar">
            <Select
              placeholder="Select Registrar"
              size="large"
              options={registrars.map(u => ({ label: u.name, value: u.id }))}
              allowClear
              showSearch
              optionFilterProp="label"
            />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12}>
          <Form.Item name="house_officer_id" label="House Officer">
            <Select
              placeholder="Select House Officer"
              size="large"
              options={houseOfficers.map(u => ({ label: u.name, value: u.id }))}
              allowClear
              showSearch
              optionFilterProp="label"
            />
          </Form.Item>
        </Col>
      </Row>
      <Form.Item>
        <Button type="primary" htmlType="submit" size="large" loading={loading} style={{ width: 140, marginRight: 8, borderRadius: 24, fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}>Save</Button>
        {onCancel && <Button onClick={onCancel} size="large" style={{ borderRadius: 24 }}>Cancel</Button>}
      </Form.Item>
    </Form>
  );

  // Render Drawer on mobile, Card on desktop
  if (isMobile) {
    return (
      <Drawer
        title="Patient Details"
        placement="right"
        closable={true}
        onClose={onClose || onCancel}
        open={visible}
        width={window.innerWidth - 32}
        styles={{ body: { padding: 16 } }}
      >
        {formContent}
      </Drawer>
    );
  }
  return (
    <Card style={{ maxWidth: 600, margin: '0 auto', boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      <Typography.Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>Patient Details</Typography.Title>
      {formContent}
    </Card>
  );
};

export default PatientForm;
