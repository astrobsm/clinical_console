
import React, { useState } from 'react';
import { Form, Input, Button, DatePicker, Drawer, Card, Select, Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import PatientSelect from './PatientSelect';

const SurgeryBookingForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;


  const [imageList, setImageList] = useState(initial?.clinical_images ? initial.clinical_images.split(',').map((url, idx) => ({ uid: idx, name: url.split('/').pop(), status: 'done', url })) : []);

  const handleImageChange = ({ fileList }) => {
    setImageList(fileList.map(f => f.originFileObj || f.url));
  };

  const handleFinish = (values) => {
    setLoading(true);
    const data = {
      ...values,
      date_booked: values.date_booked ? values.date_booked.format('YYYY-MM-DD') : '',
      scheduled_date: values.scheduled_date ? values.scheduled_date.format('YYYY-MM-DD') : '',
      clinical_images: imageList.map(f => typeof f === 'string' ? f : f.name), // For now, just store names/urls
    };
    onSubmit(data);
    setLoading(false);
    if (onClose) onClose();
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{
        ...initial,
        date_booked: initial?.date_booked ? dayjs(initial.date_booked) : null,
        scheduled_date: initial?.scheduled_date ? dayjs(initial.scheduled_date) : null,
        patient_id: initial?.patient_id || undefined,
        surgery_type: initial?.surgery_type || '',
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Please select patient' }]}> 
        <PatientSelect />
      </Form.Item>
      <Form.Item name="surgery_type" label="Surgery Type" rules={[{ required: true }]}> 
        <Input />
      </Form.Item>

      <Form.Item name="indications" label="Indications" rules={[{ required: true, message: 'Please enter indications' }]}> 
        <Input.TextArea rows={2} placeholder="Enter indications for surgery" />
      </Form.Item>

      <Form.Item name="requirements" label="Requirements" rules={[{ required: true, message: 'Select requirements' }]}> 
        <Select mode="multiple" placeholder="Select requirements">
          <Select.Option value="blood">Blood</Select.Option>
          <Select.Option value="diathermy">Diathermy</Select.Option>
          <Select.Option value="tourniquet">Tourniquet</Select.Option>
          <Select.Option value="stirrup">Stirrup</Select.Option>
          <Select.Option value="other_specialty">Other Surgical Specialty Needed</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item name="anaesthesia_type" label="Type of Anaesthesia" rules={[{ required: true, message: 'Select anaesthesia type' }]}> 
        <Select placeholder="Select type of anaesthesia">
          <Select.Option value="general">General</Select.Option>
          <Select.Option value="regional">Regional</Select.Option>
          <Select.Option value="local">Local</Select.Option>
          <Select.Option value="sedation">Sedation</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item name="position" label="Position" rules={[{ required: true, message: 'Select position' }]}> 
        <Select placeholder="Select position">
          <Select.Option value="prone">Prone</Select.Option>
          <Select.Option value="supine">Supine</Select.Option>
          <Select.Option value="right_lateral">Right Lateral</Select.Option>
          <Select.Option value="left_lateral">Left Lateral</Select.Option>
          <Select.Option value="lithotomy">Lithotomy</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item name="estimated_duration" label="Estimated Duration (hours)" rules={[{ required: true, message: 'Enter estimated duration' }]}> 
        <Input type="number" min={0} step={0.1} placeholder="e.g. 2.5" />
      </Form.Item>

      <Form.Item name="comorbidities" label="Comorbidities"> 
        <Select mode="multiple" placeholder="Select comorbidities">
          <Select.Option value="diabetes">Diabetes</Select.Option>
          <Select.Option value="hypertension">Hypertension</Select.Option>
          <Select.Option value="sickle_cell">Sickle Cell Disease</Select.Option>
          <Select.Option value="hiv">HIV</Select.Option>
          <Select.Option value="hcv">HCV</Select.Option>
          <Select.Option value="hbv">HBV</Select.Option>
          <Select.Option value="copd">COPD</Select.Option>
          <Select.Option value="renal_impairment">Renal Impairment</Select.Option>
        </Select>
      </Form.Item>
      <Form.Item name="date_booked" label="Date Booked" rules={[{ required: true }]}> 
        <DatePicker style={{ width: '100%' }} />
      </Form.Item>
      <Form.Item name="scheduled_date" label="Scheduled Date"> 
        <DatePicker style={{ width: '100%' }} />
      </Form.Item>
      <Form.Item name="admission_type" label="Admission Type" rules={[{ required: true, message: 'Select admission type' }]}> 
        <Select placeholder="Select admission type">
          <Select.Option value="day_case">Day Case</Select.Option>
          <Select.Option value="inpatient">Inpatient</Select.Option>
        </Select>
      </Form.Item>
      <Form.Item name="ward" label="Ward (if admitted)">
        <Input placeholder="Enter ward name or number" />
      </Form.Item>
      <Form.Item name="clinical_images" label="Clinical Images">
        <Upload
          listType="picture"
          multiple
          beforeUpload={() => false}
          onChange={handleImageChange}
          fileList={imageList.map((img, idx) => ({
            uid: idx,
            name: typeof img === 'string' ? img.split('/').pop() : img.name,
            status: 'done',
            url: typeof img === 'string' ? img : undefined,
            originFileObj: typeof img === 'string' ? undefined : img,
          }))}
        >
          <Button icon={<UploadOutlined />}>Upload Images</Button>
        </Upload>
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>Save</Button>
        <Button type="link" onClick={onCancel}>Cancel</Button>
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Surgery Booking"
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
    <Card style={{ maxWidth: 500, margin: '0 auto', boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      {formContent}
    </Card>
  );
};

export default SurgeryBookingForm;
