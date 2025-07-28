import React, { useState } from 'react';
import { Form, Input, Button, DatePicker, Drawer, Card, Select } from 'antd';
import dayjs from 'dayjs';
import PatientSelect from './PatientSelect';

const LabInvestigationForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const isMobile = window.innerWidth < 700;

  const handleFinish = (values) => {
    setLoading(true);
    const data = {
      ...values,
      date: values.date ? values.date.format('YYYY-MM-DD') : '',
    };
    onSubmit(data);
    setLoading(false);
    if (onClose) onClose();
  };

  const investigationOptions = [
    {
      label: 'Hematology',
      options: [
        { value: 'cbc', label: 'Complete Blood Count (CBC) / Full Blood Count (FBC)' },
        { value: 'coagulation_profile_pt', label: 'Prothrombin Time (PT)' },
        { value: 'coagulation_profile_inr', label: 'International Normalized Ratio (INR)' },
        { value: 'coagulation_profile_aptt', label: 'Activated Partial Thromboplastin Time (aPTT)' },
        { value: 'coagulation_profile_bt', label: 'Bleeding Time (BT)' },
        { value: 'coagulation_profile_ct', label: 'Clotting Time (CT)' },
        { value: 'coagulation_profile_ddimer', label: 'D-Dimer' },
        { value: 'coagulation_profile_fibrinogen', label: 'Fibrinogen Assay' },
        { value: 'bone_marrow', label: 'Bone Marrow Aspiration and Biopsy' },
        { value: 'esr', label: 'Erythrocyte Sedimentation Rate (ESR)' },
        { value: 'hb_electrophoresis', label: 'Hemoglobin Electrophoresis' },
        { value: 'pbf', label: 'Peripheral Blood Film (PBF)' },
        { value: 'platelet_function', label: 'Platelet Function Tests' },
        { value: 'reticulocyte', label: 'Reticulocyte Count' },
      ]
    },
    {
      label: 'Microbiology',
      options: [
        // Bacteriology
        { value: 'blood_culture', label: 'Blood Culture and Sensitivity (C/S)' },
        { value: 'urine_culture', label: 'Urine Culture and Sensitivity' },
        { value: 'sputum_culture', label: 'Sputum Culture and Sensitivity' },
        { value: 'wound_swab_culture', label: 'Wound/Swab Culture' },
        { value: 'stool_culture', label: 'Stool Culture' },
        { value: 'csf_culture', label: 'CSF Culture' },
        // Mycology
        { value: 'fungal_culture', label: 'Fungal Culture' },
        { value: 'koh_prep', label: 'KOH Prep for fungi' },
        { value: 'skin_nail_scrapings', label: 'Skin/Nail Scrapings' },
        // Virology
        { value: 'hepatitis_panel', label: 'Hepatitis Panel (HAV, HBV, HCV, HEV)' },
        { value: 'hiv', label: 'HIV 1/2 (Antigen/Antibody Combo)' },
        { value: 'covid19', label: 'COVID-19 PCR / Antigen Test' },
        { value: 'ebv_cmv', label: 'EBV, CMV serology' },
        { value: 'hsv', label: 'Herpes Simplex Virus (HSV) testing' },
        // Parasitology
        { value: 'malaria', label: 'Malaria Parasite Microscopy/RDT' },
        { value: 'stool_ova', label: 'Stool Microscopy for Ova and Parasites' },
        { value: 'blood_film_trypanosomes', label: 'Blood Film for Trypanosomes/Microfilaria' },
        { value: 'skin_snip_oncho', label: 'Skin snip for Onchocerciasis' },
      ]
    },
    {
      label: 'Immunology / Serology',
      options: [
        { value: 'aso', label: 'Antistreptolysin O (ASO) Titer' },
        { value: 'anti_ccp', label: 'Anti-CCP (Cyclic Citrullinated Peptide)' },
        { value: 'anti_dsDNA', label: 'Anti-dsDNA' },
        { value: 'ana', label: 'Antinuclear Antibody (ANA)' },
        { value: 'crp', label: 'C-Reactive Protein (CRP)' },
        { value: 'h_pylori_ab', label: 'H. pylori Antibody' },
        { value: 'rapid_tests', label: 'Rapid Diagnostic Tests (Typhoid, Dengue, etc.)' },
        { value: 'rf', label: 'Rheumatoid Factor (RF)' },
        { value: 'vdrl', label: 'VDRL / RPR (for Syphilis)' },
        { value: 'widal', label: 'Widal Test' },
      ]
    },
    {
      label: 'Clinical Chemistry',
      options: [
        // Renal
        { value: 'serum_urea', label: 'Serum Urea' },
        { value: 'serum_creatinine', label: 'Serum Creatinine' },
        { value: 'electrolytes', label: 'Electrolytes (Na+, K+, Cl-, HCO3-)' },
        { value: 'egfr', label: 'eGFR' },
        // Liver
        { value: 'ast', label: 'AST (SGOT)' },
        { value: 'alt', label: 'ALT (SGPT)' },
        { value: 'alp', label: 'ALP' },
        { value: 'ggt', label: 'GGT' },
        { value: 'bilirubin', label: 'Total and Direct Bilirubin' },
        { value: 'serum_albumin', label: 'Serum Albumin' },
        { value: 'total_protein', label: 'Total Protein' },
        // Glucose
        { value: 'fbs', label: 'Fasting Blood Sugar (FBS)' },
        { value: 'rbs', label: 'Random Blood Sugar (RBS)' },
        { value: 'ogtt', label: 'Oral Glucose Tolerance Test (OGTT)' },
        { value: 'hba1c', label: 'HbA1c (Glycated Hemoglobin)' },
        // Lipid
        { value: 'total_cholesterol', label: 'Total Cholesterol' },
        { value: 'ldl_hdl', label: 'LDL, HDL' },
        { value: 'triglycerides', label: 'Triglycerides' },
        // Cardiac
        { value: 'troponin', label: 'Troponin I/T' },
        { value: 'ckmb', label: 'Creatine Kinase-MB (CK-MB)' },
        { value: 'ldh', label: 'LDH (Lactate Dehydrogenase)' },
        { value: 'bnp', label: 'BNP or NT-proBNP' },
        // Others
        { value: 'amylase_lipase', label: 'Serum Amylase and Lipase' },
        { value: 'serum_calcium', label: 'Serum Calcium, Phosphate, Magnesium' },
        { value: 'uric_acid', label: 'Uric Acid' },
        { value: 'serum_iron', label: 'Serum Iron, Ferritin, TIBC' },
      ]
    },
    {
      label: 'Endocrinology',
      options: [
        { value: 'tft', label: 'Thyroid Function Tests (TSH, T3, T4)' },
        { value: 'cortisol', label: 'Cortisol (AM/PM)' },
        { value: 'acth', label: 'ACTH' },
        { value: 'prolactin', label: 'Serum Prolactin' },
        { value: 'fsh_lh', label: 'FSH, LH' },
        { value: 'sex_hormones', label: 'Estrogen, Progesterone, Testosterone' },
        { value: 'pth', label: 'Parathyroid Hormone (PTH)' },
        { value: 'vitamin_d', label: 'Vitamin D (25-OH)' },
        { value: 'insulin', label: 'Insulin Level' },
        { value: 'c_peptide', label: 'C-Peptide' },
      ]
    },
    {
      label: 'Pathology / Histology',
      options: [
        { value: 'fnac', label: 'Fine Needle Aspiration Cytology (FNAC)' },
        { value: 'tissue_biopsy', label: 'Tissue Biopsy (Histopathology)' },
        { value: 'pap_smear', label: 'Pap Smear' },
        { value: 'cervical_cytology', label: 'Cervical/Vaginal Cytology' },
        { value: 'ihc', label: 'Immunohistochemistry (IHC)' },
      ]
    },
    {
      label: 'Urinalysis',
      options: [
        { value: 'routine_urinalysis', label: 'Routine Urinalysis (Physical, Chemical, Microscopy)' },
        { value: 'urine_pregnancy', label: 'Urine Pregnancy Test' },
        { value: 'urine_24h_protein', label: '24-Hour Urine Protein' },
        { value: 'urine_electrolytes', label: 'Urine Electrolytes' },
        { value: 'urine_bence_jones', label: 'Urine Bence-Jones Protein' },
      ]
    },
    {
      label: 'Stool Analysis',
      options: [
        { value: 'routine_stool', label: 'Routine Stool Microscopy' },
        { value: 'occult_blood', label: 'Occult Blood Test' },
        { value: 'reducing_substances', label: 'Reducing Substances' },
        { value: 'fat_globules', label: 'Fat Globules' },
        { value: 'stool_ph', label: 'Stool pH' },
      ]
    },
    {
      label: 'Fluid Analysis',
      options: [
        { value: 'csf_analysis', label: 'Cerebrospinal Fluid (CSF) Analysis' },
        { value: 'ascitic_fluid', label: 'Ascitic Fluid Analysis' },
        { value: 'pleural_fluid', label: 'Pleural Fluid Analysis' },
        { value: 'synovial_fluid', label: 'Synovial Fluid Analysis' },
        { value: 'pericardial_fluid', label: 'Pericardial Fluid Analysis' },
        { value: 'semen_analysis', label: 'Semen Analysis' },
      ]
    },
    {
      label: 'Blood Bank / Transfusion',
      options: [
        { value: 'blood_grouping', label: 'Blood Grouping and Rh Typing' },
        { value: 'crossmatching', label: 'Crossmatching' },
        { value: 'coombs', label: 'Direct and Indirect Coombs Test' },
        { value: 'antibody_screening', label: 'Antibody Screening' },
        { value: 'tti_screening', label: 'Screening for TTIs (HIV, HBV, HCV, Syphilis, Malaria)' },
      ]
    },
    {
      label: 'Specialized / Advanced',
      options: [
        { value: 'pcr', label: 'PCR (for TB, COVID-19, HPV, etc.)' },
        { value: 'flow_cytometry', label: 'Flow Cytometry (for leukemia/lymphoma)' },
        { value: 'elisa', label: 'ELISA Tests' },
        { value: 'autoantibody_panels', label: 'Autoantibody Panels' },
        { value: 'psa', label: 'Tumor Marker: PSA (Prostate)' },
        { value: 'cea', label: 'Tumor Marker: CEA (Colon)' },
        { value: 'ca_125', label: 'Tumor Marker: CA-125 (Ovary)' },
        { value: 'ca_19_9', label: 'Tumor Marker: CA 19-9 (Pancreas)' },
        { value: 'afp', label: 'Tumor Marker: AFP (Liver/Testis)' },
        { value: 'genetic_testing', label: 'Genetic Testing / Karyotyping' },
        { value: 'hla_typing', label: 'HLA Typing' },
      ]
    },
  ];

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{
        ...initial,
        date: initial?.date ? dayjs(initial.date) : null,
        patient_id: initial?.patient_id || undefined,
        investigation: initial?.investigation || '',
        result: initial?.result || '',
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Please select patient' }]}> 
        <PatientSelect />
      </Form.Item>
      <Form.Item name="investigation" label="Investigation" rules={[{ required: true, message: 'Please select investigation' }]}> 
        <Select
          showSearch
          placeholder="Select Investigation"
          options={investigationOptions}
          optionFilterProp="label"
          size="large"
        />
      </Form.Item>
      <Form.Item name="result" label="Result"> 
        <Input.TextArea />
      </Form.Item>
      <Form.Item name="date" label="Date" rules={[{ required: true }]}> 
        <DatePicker style={{ width: '100%' }} />
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
        title="Lab Investigation"
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

export default LabInvestigationForm;
