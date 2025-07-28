
import React, { useState } from 'react';
import { Form, Input, Button, Card, Drawer, message, Typography, Select, Upload } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import PatientSelect from './PatientSelect';

const woundPhases = [
  { value: 'acute', label: 'Acute Wound' },
  { value: 'extension', label: 'Extension Phase' },
  { value: 'transition', label: 'Transition Phase' },
  { value: 'repair', label: 'Repair Phase' },
  { value: 'indolent', label: 'Indolent Phase' },
];

const comorbidityOptions = [
  { value: "addisons_disease", label: "Addison’s disease" },
  { value: "alcohol_use_disorder", label: "Alcohol use disorder" },
  { value: "alzheimers_disease", label: "Alzheimer’s disease" },
  { value: "als", label: "Amyotrophic lateral sclerosis (ALS)" },
  { value: "anemia_chronic", label: "Anemia (chronic)" },
  { value: "ankylosing_spondylitis", label: "Ankylosing spondylitis" },
  { value: "anxiety_disorders", label: "Anxiety disorders" },
  { value: "asthma", label: "Asthma" },
  { value: "atrial_fibrillation", label: "Atrial fibrillation" },
  { value: "adhd", label: "Attention-deficit/hyperactivity disorder (ADHD)" },
  { value: "autism_spectrum_disorder", label: "Autism spectrum disorder" },
  { value: "autoimmune_hepatitis", label: "Autoimmune hepatitis" },
  { value: "behcets_disease", label: "Behçet’s disease" },
  { value: "bph", label: "Benign prostatic hyperplasia (BPH)" },
  { value: "bipolar_disorder", label: "Bipolar disorder" },
  { value: "bronchiectasis", label: "Bronchiectasis" },
  { value: "cancer", label: "Cancer (any type)" },
  { value: "cardiomyopathy", label: "Cardiomyopathy" },
  { value: "celiac_disease", label: "Celiac disease" },
  { value: "cerebral_palsy", label: "Cerebral palsy" },
  { value: "chronic_fatigue_syndrome", label: "Chronic fatigue syndrome" },
  { value: "ckd", label: "Chronic kidney disease (CKD)" },
  { value: "chronic_liver_disease", label: "Chronic liver disease (e.g., cirrhosis)" },
  { value: "copd", label: "Chronic obstructive pulmonary disease (COPD)" },
  { value: "chronic_pancreatitis", label: "Chronic pancreatitis" },
  { value: "chronic_sinusitis", label: "Chronic sinusitis" },
  { value: "chronic_utis", label: "Chronic urinary tract infections (UTIs)" },
  { value: "chf", label: "Congestive heart failure (CHF)" },
  { value: "cad", label: "Coronary artery disease (CAD)" },
  { value: "crohns_disease", label: "Crohn’s disease" },
  { value: "cushings_syndrome", label: "Cushing’s syndrome" },
  { value: "cystic_fibrosis", label: "Cystic fibrosis" },
  { value: "dementia", label: "Dementia" },
  { value: "depression", label: "Depression (Major Depressive Disorder)" },
  { value: "dermatomyositis", label: "Dermatomyositis" },
  { value: "diabetes_insipidus", label: "Diabetes insipidus" },
  { value: "diabetes_mellitus", label: "Diabetes mellitus (Type 1 and Type 2)" },
  { value: "diverticular_disease", label: "Diverticular disease" },
  { value: "down_syndrome", label: "Down syndrome" },
  { value: "dyslipidemia", label: "Dyslipidemia" },
  { value: "ehlers_danlos", label: "Ehlers-Danlos syndrome" },
  { value: "epilepsy", label: "Epilepsy" },
  { value: "fibromyalgia", label: "Fibromyalgia" },
  { value: "gerd", label: "Gastroesophageal reflux disease (GERD)" },
  { value: "glaucoma", label: "Glaucoma" },
  { value: "gout", label: "Gout" },
  { value: "guillain_barre", label: "Guillain-Barré syndrome" },
  { value: "hemophilia", label: "Hemophilia" },
  { value: "hepatitis_b_c", label: "Hepatitis B/C (chronic)" },
  { value: "hiv_aids", label: "HIV/AIDS" },
  { value: "hyperparathyroidism", label: "Hyperparathyroidism" },
  { value: "hypertension", label: "Hypertension" },
  { value: "hyperthyroidism", label: "Hyperthyroidism" },
  { value: "hypothyroidism", label: "Hypothyroidism" },
  { value: "idiopathic_pulmonary_fibrosis", label: "Idiopathic pulmonary fibrosis" },
  { value: "ibd", label: "Inflammatory bowel disease (IBD)" },
  { value: "insomnia", label: "Insomnia (chronic)" },
  { value: "interstitial_cystitis", label: "Interstitial cystitis" },
  { value: "ibs", label: "Irritable bowel syndrome (IBS)" },
  { value: "ischemic_heart_disease", label: "Ischemic heart disease" },
  { value: "kidney_stones", label: "Kidney stones (recurrent)" },
  { value: "lupus", label: "Lupus (Systemic Lupus Erythematosus)" },
  { value: "lymphedema", label: "Lymphedema" },
  { value: "major_organ_transplant", label: "Major organ transplant recipient" },
  { value: "malabsorption_syndromes", label: "Malabsorption syndromes" },
  { value: "metabolic_syndrome", label: "Metabolic syndrome" },
  { value: "migraine", label: "Migraine (chronic)" },
  { value: "motor_neuron_disease", label: "Motor neuron disease" },
  { value: "multiple_sclerosis", label: "Multiple sclerosis" },
  { value: "muscular_dystrophy", label: "Muscular dystrophy" },
  { value: "myasthenia_gravis", label: "Myasthenia gravis" },
  { value: "myelofibrosis", label: "Myelofibrosis" },
  { value: "obesity", label: "Obesity" },
  { value: "ocd", label: "Obsessive-compulsive disorder (OCD)" },
  { value: "osteoarthritis", label: "Osteoarthritis" },
  { value: "osteoporosis", label: "Osteoporosis" },
  { value: "parkinsons_disease", label: "Parkinson’s disease" },
  { value: "peptic_ulcer_disease", label: "Peptic ulcer disease" },
  { value: "pad", label: "Peripheral artery disease (PAD)" },
  { value: "peripheral_neuropathy", label: "Peripheral neuropathy" },
  { value: "pcos", label: "Polycystic ovary syndrome (PCOS)" },
  { value: "ptsd", label: "Post-traumatic stress disorder (PTSD)" },
  { value: "primary_biliary_cholangitis", label: "Primary biliary cholangitis" },
  { value: "primary_sclerosing_cholangitis", label: "Primary sclerosing cholangitis" },
  { value: "psoriasis", label: "Psoriasis" },
  { value: "psoriatic_arthritis", label: "Psoriatic arthritis" },
  { value: "pulmonary_hypertension", label: "Pulmonary hypertension" },
  { value: "rheumatoid_arthritis", label: "Rheumatoid arthritis" },
  { value: "sarcoidosis", label: "Sarcoidosis" },
  { value: "schizophrenia", label: "Schizophrenia" },
  { value: "scleroderma", label: "Scleroderma" },
  { value: "seizure_disorder", label: "Seizure disorder" },
  { value: "severe_anemia", label: "Severe anemia" },
  { value: "sickle_cell_disease", label: "Sickle cell disease" },
  { value: "sjogrens_syndrome", label: "Sjögren's syndrome" },
  { value: "sleep_apnea", label: "Sleep apnea (obstructive or central)" },
  { value: "spinal_cord_injury", label: "Spinal cord injury (chronic)" },
  { value: "stroke", label: "Stroke / Cerebrovascular accident (CVA)" },
  { value: "systemic_sclerosis", label: "Systemic sclerosis" },
  { value: "thalassemia", label: "Thalassemia (major and intermedia)" },
  { value: "thyroid_disorders", label: "Thyroid disorders (chronic)" },
  { value: "tuberculosis", label: "Tuberculosis (chronic/latent)" },
  { value: "ulcerative_colitis", label: "Ulcerative colitis" },
  { value: "urinary_incontinence", label: "Urinary incontinence (chronic)" },
  { value: "vasculitis", label: "Vasculitis" },
  { value: "vertigo", label: "Vertigo (chronic)" },
];

const WoundCareForm = ({ onSubmit, initial, onCancel, visible = true, onClose, comorbiditiesOptions = [] }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [imageList, setImageList] = useState(initial?.images || []);
  const isMobile = window.innerWidth < 700;

  const handleFinish = async (values) => {
    setLoading(true);
    try {
      await onSubmit({ ...values, images: imageList });
      form.resetFields();
      setImageList([]);
      if (!onClose) message.success('Wound care plan saved!');
      if (onClose) onClose();
    } catch (err) {
      message.error(err?.message || 'Failed to save wound care plan');
    }
    setLoading(false);
  };

  const handleImageChange = ({ fileList }) => {
    setImageList(fileList.map(f => f.originFileObj || f.url));
  };

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={initial || {}}
      onFinish={handleFinish}
    >
      <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Select patient' }]}> 
        <PatientSelect />
      </Form.Item>
      <Form.Item name="images" label="Clinical Images">
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
      <Form.Item name="comorbidities" label="Co-morbidities">
        <Select
          mode="multiple"
          showSearch
          options={comorbiditiesOptions}
          placeholder="Select co-morbidities"
          filterOption={(input, option) =>
            option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0
          }
        />
      </Form.Item>

      <Form.Item label="Wound Dimensions (cm)">
        <Input.Group compact>
          <Form.Item name="length_cm" noStyle rules={[{ required: true, message: 'Length required' }]}> 
            <Input style={{ width: '33%' }} type="number" min={0} step={0.1} placeholder="Length" addonAfter="L" />
          </Form.Item>
          <Form.Item name="width_cm" noStyle rules={[{ required: true, message: 'Width required' }]}> 
            <Input style={{ width: '33%' }} type="number" min={0} step={0.1} placeholder="Width" addonAfter="W" />
          </Form.Item>
          <Form.Item name="depth_cm" noStyle rules={[{ required: true, message: 'Depth required' }]}> 
            <Input style={{ width: '34%' }} type="number" min={0} step={0.1} placeholder="Depth" addonAfter="D" />
          </Form.Item>
        </Input.Group>
      </Form.Item>
      <Form.Item name="phase" label="Clinical Phase" rules={[{ required: true, message: 'Select phase' }]}> 
        <Select options={woundPhases} placeholder="Select clinical phase" />
      </Form.Item>
      <Form.Item name="dressing_protocol" label="Dressing Protocol" rules={[{ required: true, message: 'Enter dressing protocol' }]}> 
        <Input.TextArea rows={3} placeholder="Dressing protocol" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" size="large" loading={loading} style={{ width: 140, marginRight: 8, borderRadius: 24, fontWeight: 600, boxShadow: '0 2px 8px #38b00033' }}>Save</Button>
        {onCancel && <Button onClick={onCancel} size="large" style={{ borderRadius: 24 }}>Cancel</Button>}
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Wound Care Plan"
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
      <Typography.Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>Wound Care Plan</Typography.Title>
      {formContent}
    </Card>
  );
};

export default WoundCareForm;
