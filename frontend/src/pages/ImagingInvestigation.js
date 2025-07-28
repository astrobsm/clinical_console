import React, { useEffect, useState } from 'react';
import logo from '../clinical_console.png';
import { authFetch } from '../utils/api';
import { Select, Form, Button, message, Input } from 'antd';
import PatientSelect from '../components/PatientSelect';

const ImagingInvestigation = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await authFetch('/api/imaging-investigations/');
      setItems(data);
    } catch (err) {
      setError('Server error');
    }
    setLoading(false);
  };

  useEffect(() => { fetchItems(); }, []);

  const handleFinish = async (values) => {
    setSubmitting(true);
    try {
      await authFetch('/api/imaging-investigations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      message.success('Imaging investigation added');
      form.resetFields();
      fetchItems();
    } catch (err) {
      message.error(err?.message || 'Failed to add investigation');
    }
    setSubmitting(false);
  };

  const imagingOptions = [
    {
      label: 'X-Ray / Plain Radiography',
      options: [
        { value: 'abdominal_xray', label: 'Abdominal X-ray' },
        { value: 'barium_enema', label: 'Barium Enema' },
        { value: 'barium_meal_follow_through', label: 'Barium Meal and Follow Through' },
        { value: 'barium_swallow', label: 'Barium Swallow' },
        { value: 'bone_age', label: 'Bone Age Assessment' },
        { value: 'bone_xray', label: 'Bone X-ray (any region: limb, spine, skull, pelvis, etc.)' },
        { value: 'chest_xray', label: 'Chest X-ray (CXR) – PA, Lateral, Portable' },
        { value: 'cystourethrogram', label: 'Cystourethrogram (MCUG)' },
        { value: 'hsg', label: 'Hysterosalpingography (HSG)' },
        { value: 'ivu_ivp', label: 'Intravenous Urography (IVU) / Intravenous Pyelogram (IVP)' },
        { value: 'kub_xray', label: 'KUB X-ray (Kidney, Ureter, Bladder)' },
        { value: 'lumbosacral_spine_xray', label: 'Lumbosacral Spine X-ray' },
        { value: 'pelvimetry', label: 'Pelvimetry' },
        { value: 'sinus_xray', label: 'Sinus X-ray' },
        { value: 'skeletal_survey', label: 'Skeletal Survey' },
        { value: 'skull_xray', label: 'Skull X-ray' },
        { value: 'soft_tissue_neck_xray', label: 'Soft Tissue Neck X-ray' },
        { value: 'spine_xray', label: 'Spine X-ray (Cervical, Thoracic, Lumbar)' },
        { value: 'urethrogram', label: 'Urethrogram (Ascending/Descending)' },
        { value: 'xray_fb', label: 'X-ray Foreign Body (FB)' },
      ]
    },
    {
      label: 'Computed Tomography (CT) Scan',
      options: [
        { value: 'ct_abdomen', label: 'CT Abdomen' },
        { value: 'ct_angiography', label: 'CT Angiography (Brain, Chest, Peripheral, etc.)' },
        { value: 'ct_brain', label: 'CT Brain (Plain and Contrast)' },
        { value: 'ct_chest', label: 'CT Chest (HRCT, Contrast)' },
        { value: 'ct_colonography', label: 'CT Colonography (Virtual Colonoscopy)' },
        { value: 'ct_coronary_angiography', label: 'CT Coronary Angiography' },
        { value: 'ct_enterography', label: 'CT Enterography' },
        { value: 'ct_kub', label: 'CT KUB' },
        { value: 'ct_neck', label: 'CT Neck' },
        { value: 'ct_paranasal_sinuses', label: 'CT Paranasal Sinuses' },
        { value: 'ct_pelvis', label: 'CT Pelvis' },
        { value: 'ct_pulmonary_angiography', label: 'CT Pulmonary Angiography (CTPA)' },
        { value: 'ct_spine', label: 'CT Spine (Cervical, Thoracic, Lumbar)' },
        { value: 'ct_temporal_bone', label: 'CT Temporal Bone' },
        { value: 'ct_urography', label: 'CT Urography' },
        { value: 'whole_body_ct', label: 'Whole Body CT Scan (for trauma or staging)' },
      ]
    },
    {
      label: 'Magnetic Resonance Imaging (MRI)',
      options: [
        { value: 'mra', label: 'MR Angiography (MRA – brain, renal, peripheral)' },
        { value: 'mrcp', label: 'MR Cholangiopancreatography (MRCP)' },
        { value: 'mri_abdomen', label: 'MRI Abdomen' },
        { value: 'mri_brain', label: 'MRI Brain' },
        { value: 'mri_breast', label: 'MRI Breast' },
        { value: 'mri_cervical_spine', label: 'MRI Cervical Spine' },
        { value: 'mri_knee', label: 'MRI Knee' },
        { value: 'mri_lumbosacral_spine', label: 'MRI Lumbosacral Spine' },
        { value: 'mri_orbit', label: 'MRI Orbit' },
        { value: 'mri_pelvis', label: 'MRI Pelvis' },
        { value: 'mri_prostate', label: 'MRI Prostate' },
        { value: 'mri_shoulder', label: 'MRI Shoulder' },
        { value: 'mri_soft_tissue_mass', label: 'MRI Soft Tissue Mass' },
        { value: 'mri_temporal_bone', label: 'MRI Temporal Bone' },
        { value: 'whole_spine_mri', label: 'Whole Spine MRI' },
        { value: 'whole_body_mri', label: 'Whole Body MRI (for staging/metastasis)' },
      ]
    },
    {
      label: 'Ultrasound (US / Sonography)',
      options: [
        { value: 'abdominal_us', label: 'Abdominal Ultrasound' },
        { value: 'anomaly_scan', label: 'Anomaly Scan (Obstetric)' },
        { value: 'breast_us', label: 'Breast Ultrasound' },
        { value: 'carotid_doppler', label: 'Carotid Doppler' },
        { value: 'cranial_us', label: 'Cranial Ultrasound (Neonatal)' },
        { value: 'dvt_doppler', label: 'Deep Vein Thrombosis (DVT) Doppler' },
        { value: 'echo', label: 'Echocardiography (Transthoracic and Transesophageal)' },
        { value: 'fast_scan', label: 'FAST Scan (Focused Assessment with Sonography in Trauma)' },
        { value: 'fetal_biometry', label: 'Fetal Biometry' },
        { value: 'fetal_doppler', label: 'Fetal Doppler' },
        { value: 'follicular_monitoring', label: 'Follicular Monitoring' },
        { value: 'obstetric_scan', label: 'Obstetric Scan' },
        { value: 'pelvic_us', label: 'Pelvic Ultrasound (Transabdominal & Transvaginal)' },
        { value: 'prostate_us', label: 'Prostate Ultrasound' },
        { value: 'renal_us', label: 'Renal Ultrasound' },
        { value: 'scrotal_us', label: 'Scrotal/Testicular Ultrasound' },
        { value: 'soft_tissue_us', label: 'Soft Tissue Ultrasound' },
        { value: 'thyroid_us', label: 'Thyroid Ultrasound' },
        { value: 'transfontanelle_us', label: 'Transfontanelle Ultrasound' },
        { value: 'trus', label: 'Transrectal Ultrasound (TRUS)' },
        { value: 'vascular_doppler', label: 'Vascular Doppler (Arterial and Venous)' },
        { value: 'whole_abdomen_us', label: 'Whole Abdomen Ultrasound' },
      ]
    },
    {
      label: 'Fluoroscopy-Based Investigations',
      options: [
        { value: 'barium_enema', label: 'Barium Enema' },
        { value: 'barium_meal_follow_through', label: 'Barium Meal & Follow Through' },
        { value: 'barium_swallow', label: 'Barium Swallow' },
        { value: 'cystourethrogram', label: 'Cystourethrogram (MCUG)' },
        { value: 'hsg', label: 'Hysterosalpingography (HSG)' },
        { value: 'sinogram', label: 'Sinogram' },
        { value: 'sialography', label: 'Sialography' },
        { value: 'urethrogram', label: 'Urethrogram' },
        { value: 'video_swallow', label: 'Video Swallow Study (Modified Barium Swallow)' },
      ]
    },
    {
      label: 'Nuclear Medicine / Functional Imaging',
      options: [
        { value: 'bone_scan', label: 'Bone Scan (Technetium-99m)' },
        { value: 'dmsa_scan', label: 'DMSA Scan (Renal Cortical Imaging)' },
        { value: 'gallium_scan', label: 'Gallium Scan' },
        { value: 'hida_scan', label: 'HIDA Scan (Hepatobiliary Iminodiacetic Acid)' },
        { value: 'pet_scan', label: 'PET Scan (Positron Emission Tomography)' },
        { value: 'spect_scan', label: 'SPECT Scan (Single Photon Emission Computed Tomography)' },
        { value: 'thyroid_scan', label: 'Thyroid Scan (Iodine or Technetium)' },
        { value: 'vq_scan', label: 'Ventilation-Perfusion (V/Q) Scan' },
        { value: 'whole_body_petct', label: 'Whole Body PET-CT (Staging, Metastasis)' },
      ]
    },
    {
      label: 'Interventional Radiology Procedures',
      options: [
        { value: 'angiography', label: 'Angiography (Diagnostic and Therapeutic)' },
        { value: 'biopsy', label: 'Biopsy (US or CT-guided)' },
        { value: 'central_line', label: 'Central Line Placement under Ultrasound' },
        { value: 'drainage_abscess', label: 'Drainage of Abscesses (US/CT-guided)' },
        { value: 'embolization', label: 'Embolization Procedures' },
        { value: 'nephrostomy', label: 'Nephrostomy Tube Placement' },
        { value: 'picc_line', label: 'PICC Line Insertion' },
        { value: 'rfa', label: 'Radiofrequency Ablation (RFA)' },
        { value: 'stent_placement', label: 'Stent Placement (Biliary, Vascular, Ureteric)' },
        { value: 'thrombolysis', label: 'Thrombolysis' },
        { value: 'vertebroplasty', label: 'Vertebroplasty / Kyphoplasty' },
      ]
    },
    {
      label: 'Obstetric & Gynaecological Imaging',
      options: [
        { value: 'anomaly_scan', label: 'Anomaly Scan' },
        { value: 'dating_scan', label: 'Dating Scan' },
        { value: 'early_pregnancy_scan', label: 'Early Pregnancy Scan' },
        { value: 'follicular_study', label: 'Follicular Study' },
        { value: 'nuchal_translucency', label: 'Nuchal Translucency Scan' },
        { value: 'obstetric_ultrasound', label: 'Obstetric Ultrasound' },
        { value: 'pelvic_ultrasound', label: 'Pelvic Ultrasound' },
        { value: 'sonohysterography', label: 'Sonohysterography' },
        { value: 'transvaginal_ultrasound', label: 'Transvaginal Ultrasound' },
        { value: 'hsg', label: 'Hysterosalpingography (HSG)' },
      ]
    },
  ];

  return (
    <div>
      <img src={logo} alt="Clinical Console Logo" style={{ height: 60, margin: '24px auto 8px', display: 'block' }} />
      <h2 style={{ textAlign: 'center' }}>Imaging Investigations</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? <p>Loading...</p> : (
        <Form layout="vertical" form={form} onFinish={handleFinish} style={{ maxWidth: 500 }}>
          <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Please select patient' }]}> 
            <PatientSelect />
          </Form.Item>
          <Form.Item name="investigation" label="Investigation" rules={[{ required: true, message: 'Please select investigation' }]}> 
            <Select
              showSearch
              placeholder="Select Investigation"
              options={imagingOptions}
              optionFilterProp="label"
              size="large"
            />
          </Form.Item>
          <Form.Item name="result" label="Result">
            <Select placeholder="Pending/Normal/Abnormal" options={[
              { value: 'pending', label: 'Pending' },
              { value: 'normal', label: 'Normal' },
              { value: 'abnormal', label: 'Abnormal' }
            ]} allowClear size="large" />
          </Form.Item>
          <Form.Item name="date" label="Date">
            <Input type="date" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={submitting}>Add Investigation</Button>
          </Form.Item>
        </Form>
      )}
      <div style={{ marginTop: 32 }}>
        <h3>All Imaging Investigations</h3>
        <ul>
          {items.map(i => (
            <li key={i.id}>
              {i.patient && i.patient.name ? `${i.patient.name} (ID: ${i.patient.id})` : `Patient ID: ${i.patient_id}`}
              {' - '}{i.investigation}{' - '}{i.result || 'No result'}{' - '}{i.date ? i.date.split('T')[0] : ''}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ImagingInvestigation;
