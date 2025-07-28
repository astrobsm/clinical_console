
import React, { useState } from 'react';
import { Form, Input, Button, DatePicker, Drawer, Card, Select, InputNumber, Checkbox, Divider, Typography, Row, Col, Alert } from 'antd';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { foodTable } from '../utils/nigeriaFoodTable';
import dayjs from 'dayjs';
import PatientSelect from './PatientSelect';

const ClinicalForm = ({ onSubmit, initial, onCancel, visible = true, onClose }) => {
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


  // GFR State
  const [gfrParams, setGfrParams] = useState({
    creatinine: '', age: '', sex: '', ethnicity: '', weight: ''
  });
  const calcGFR = () => {
    // CKD-EPI formula (mg/dL, age in years, sex, ethnicity)
    const { creatinine, age, sex, ethnicity, weight } = gfrParams;
    if (!creatinine || !age || !sex) return '';
    let k = sex === 'female' ? 0.7 : 0.9;
    let a = sex === 'female' ? -0.329 : -0.411;
    let min = Math.min(creatinine / k, 1);
    let max = Math.max(creatinine / k, 1);
    let gfr = 141 * Math.pow(min, a) * Math.pow(max, -1.209) * Math.pow(0.993, age);
    if (sex === 'female') gfr *= 1.018;
    if (ethnicity === 'black') gfr *= 1.159;
    return gfr ? gfr.toFixed(1) : '';
  };

  // Braden Scale State
  const [braden, setBraden] = useState({
    sensory: 1, moisture: 1, activity: 1, mobility: 1, nutrition: 1, friction: 1
  });
  const bradenTotal = Object.values(braden).reduce((a, b) => a + Number(b), 0);
  let bradenRisk = '';
  let bradenAction = '';
  if (bradenTotal <= 9) { bradenRisk = 'Very high'; bradenAction = 'Frequent repositioning, foam dressing, consult wound care nurse, nutritional intervention'; }
  else if (bradenTotal <= 12) { bradenRisk = 'High'; bradenAction = 'Frequent repositioning, foam dressing, consult wound care nurse, nutritional intervention'; }
  else if (bradenTotal <= 14) { bradenRisk = 'Moderate'; bradenAction = 'Pressure-relieving mattress, skin inspection, nutrition support'; }
  else if (bradenTotal <= 18) { bradenRisk = 'Mild'; bradenAction = 'Reposition q2–4h, protective dressing'; }
  else { bradenRisk = 'Low'; bradenAction = 'Routine care'; }

  // DVT Wells Score State
  const wellsList = [
    { key: 'cancer', label: 'Active cancer (treatment ongoing or within 6 months)', pts: 1 },
    { key: 'calf', label: 'Calf swelling ≥3 cm compared to other leg', pts: 1 },
    { key: 'unilateral', label: 'Swollen unilateral leg', pts: 1 },
    { key: 'edema', label: 'Pitting edema (in symptomatic leg only)', pts: 1 },
    { key: 'veins', label: 'Swollen superficial veins (non-varicose)', pts: 1 },
    { key: 'entire', label: 'Entire leg swollen', pts: 1 },
    { key: 'tenderness', label: 'Localized tenderness along deep venous system', pts: 1 },
    { key: 'paralysis', label: 'Paralysis, paresis, or recent cast immobilization', pts: 1 },
    { key: 'bedridden', label: 'Bedridden recently (>3 days) or major surgery <12 weeks', pts: 1 },
    { key: 'alt_diag', label: 'Alternative diagnosis at least as likely as DVT', pts: -2 },
  ];
  const [wells, setWells] = useState({});
  const wellsScore = wellsList.reduce((sum, item) => sum + (wells[item.key] ? item.pts : 0), 0);
  let wellsRisk = '';
  let wellsAction = '';
  if (wellsScore >= 3) { wellsRisk = 'High'; wellsAction = 'Immediate Doppler Ultrasound + Anticoagulation'; }
  else if (wellsScore >= 1) { wellsRisk = 'Moderate'; wellsAction = 'D-dimer + Ultrasound if positive'; }
  else { wellsRisk = 'Low'; wellsAction = 'D-dimer test; if negative, no further testing needed'; }

  // Nutrition State
  const [nutrition, setNutrition] = useState({ weight: '', illness: '' });
  let calReq = '', protReq = '', calMin = 0, calMax = 0, protMin = 0, protMax = 0;
  if (nutrition.weight && nutrition.illness) {
    const w = Number(nutrition.weight);
    if (nutrition.illness === 'normal') { calMin = w*27.5; calMax = w*30; protMin = w*0.8; protMax = w*1.0; }
    if (nutrition.illness === 'moderate') { calMin = w*30; calMax = w*35; protMin = w*1.0; protMax = w*1.2; }
    if (nutrition.illness === 'critical') { calMin = w*25; calMax = w*30; protMin = w*1.2; protMax = w*2.0; }
    if (nutrition.illness === 'burn') { calMin = w*35; calMax = w*50; protMin = w*2.0; protMax = w*2.5; }
    calReq = `${calMin.toFixed(0)}–${calMax.toFixed(0)}`;
    protReq = `${protMin.toFixed(1)}–${protMax.toFixed(1)}`;
  }

  // Meal Plan Generator
  const [mealPlan, setMealPlan] = useState(null);
  const [mealPlanError, setMealPlanError] = useState('');
  // Co-morbidities options
  const comorbidityOptions = [
    'Diabetes',
    'Hypertension',
    'Heart Failure',
    'Renal Impairment',
    'Burns',
    'Pressure Sores',
    'Asthma',
    'Tuberculosis',
    'Protein Energy Malnutrition',
    'Sickle Cell Disease',
    'Malignancy'
  ];

  const [comorbidities, setComorbidities] = useState([]);

  function filterFoodsByComorbidities(foods, comorbidities) {
    let filtered = foods;
    if (comorbidities.includes('Diabetes')) {
      filtered = filtered.filter(f => f.kcal < 300 && (!/rice|yam|fufu|garri|plantain|sweet potato|pap|amala/i.test(f.name) || f.protein > 5)); // prefer low GI, high protein
    }
    if (comorbidities.includes('Hypertension') || comorbidities.includes('Heart Failure')) {
      filtered = filtered.filter(f => !/beef|salt|stew|egusi|groundnut/i.test(f.name)); // avoid salty/fatty foods
    }
    if (comorbidities.includes('Renal Impairment')) {
      filtered = filtered.filter(f => f.protein < 15 && f.kcal < 300); // restrict protein and potassium
    }
    if (comorbidities.includes('Burns') || comorbidities.includes('Protein Energy Malnutrition')) {
      filtered = filtered.filter(f => f.protein > 5); // high protein
    }
    if (comorbidities.includes('Pressure Sores')) {
      filtered = filtered.filter(f => f.protein > 3); // high protein
    }
    if (comorbidities.includes('Asthma') || comorbidities.includes('Tuberculosis') || comorbidities.includes('Sickle Cell Disease') || comorbidities.includes('Malignancy')) {
      filtered = filtered.filter(f => f.protein > 2); // general high protein, high kcal
    }
    return filtered.length ? filtered : foods; // fallback to all if too restrictive
  }

  function generateMealPlan() {
    if (!calMin || !calMax || !protMin || !protMax) {
      setMealPlanError('Enter weight and illness type to generate meal plan.');
      return;
    }
    let plan = [];
    const mealTimes = ['Breakfast', 'Lunch', 'Dinner', 'Snack'];
    for (let day = 0; day < 7; day++) {
      let dayKcal = 0, dayProt = 0;
      let meals = { Breakfast: [], Lunch: [], Dinner: [], Snack: [] };
      let foods = filterFoodsByComorbidities([...foodTable].sort(() => Math.random() - 0.5), comorbidities);
      // Distribute foods into meals
      let mealTargets = [0.25, 0.35, 0.3, 0.1]; // % of daily kcal/protein for each meal
      let mealKcalTargets = mealTargets.map(frac => Math.round(calMin * frac));
      let mealProtTargets = mealTargets.map(frac => +(protMin * frac).toFixed(1));
      let used = new Set();
      mealTimes.forEach((meal, idx) => {
        let mKcal = 0, mProt = 0;
        for (let i = 0; i < foods.length && (mKcal < mealKcalTargets[idx] || mProt < mealProtTargets[idx]); i++) {
          if (used.has(i)) continue;
          let f = foods[i];
          meals[meal].push(f);
          mKcal += f.kcal;
          mProt += f.protein;
          used.add(i);
        }
        dayKcal += mKcal;
        dayProt += mProt;
      });
      plan.push({ day: day+1, meals, kcal: dayKcal, protein: dayProt });
    }
    setMealPlan(plan);
    setMealPlanError('');
  }

  function exportMealPlanPDF() {
    if (!mealPlan) return;
    const doc = new jsPDF();
    doc.text('Comprehensive 7-Day Meal Plan (Nigeria)', 10, 10);
    mealPlan.forEach((d, idx) => {
      doc.text(`Day ${d.day}: Total kcal: ${d.kcal}, Protein: ${d.protein}g`, 10, 20 + idx*40);
      autoTable(doc, {
        startY: 25 + idx*40,
        head: [['Food', 'Portion', 'kcal', 'Protein (g)']],
        body: d.meals.map(m => [m.name, m.portion, m.kcal, m.protein]),
        theme: 'grid',
        styles: { fontSize: 8 },
      });
    });
    doc.save('meal_plan.pdf');
  }

  const micronutrients = [
    { name: 'Vitamin C', dose: '500–1000 mg/day', role: 'Collagen synthesis, immunity' },
    { name: 'Vitamin A', dose: '5000–10000 IU/day', role: 'Epithelial healing, immunity' },
    { name: 'Zinc', dose: '15–40 mg/day', role: 'Wound healing, enzyme function' },
    { name: 'Iron', dose: '10–20 mg/day', role: 'Hemoglobin production' },
    { name: 'Magnesium', dose: '—', role: 'Enzymatic and neuromuscular activity' },
    { name: 'Calcium & Vitamin D', dose: '—', role: 'Bone health, immune function' },
    { name: 'Selenium', dose: '50–200 mcg/day', role: 'Antioxidant defense' },
    { name: 'B-complex vitamins', dose: '—', role: 'Metabolic support, energy generation' },
  ];

  const formContent = (
    <Form
      form={form}
      layout="vertical"
      initialValues={{
        ...initial,
        date: initial?.date ? dayjs(initial.date) : null,
        patient_id: initial?.patient_id || undefined,
        summary: initial?.summary || '',
      }}
      onFinish={handleFinish}
    >
      <Form.Item name="patient_id" label="Patient" rules={[{ required: true, message: 'Please select patient' }]}> 
        <PatientSelect />
      </Form.Item>
      <Form.Item name="summary" label="Summary" rules={[{ required: true }]}> 
        <Input.TextArea />
      </Form.Item>
      <Form.Item name="date" label="Date" rules={[{ required: true }]}> 
        <DatePicker style={{ width: '100%' }} />
      </Form.Item>

      <Divider orientation="left">GFR Calculation</Divider>
      <Row gutter={8}>
        <Col span={8}><Form.Item label="Serum Creatinine (mg/dL)"><InputNumber min={0} step={0.01} value={gfrParams.creatinine} onChange={v => setGfrParams(p => ({ ...p, creatinine: v }))} style={{ width: '100%' }} /></Form.Item></Col>
        <Col span={8}><Form.Item label="Age (years)"><InputNumber min={0} value={gfrParams.age} onChange={v => setGfrParams(p => ({ ...p, age: v }))} style={{ width: '100%' }} /></Form.Item></Col>
        <Col span={8}><Form.Item label="Sex"><Select value={gfrParams.sex} onChange={v => setGfrParams(p => ({ ...p, sex: v }))}><Select.Option value="male">Male</Select.Option><Select.Option value="female">Female</Select.Option></Select></Form.Item></Col>
      </Row>
      <Row gutter={8}>
        <Col span={8}><Form.Item label="Ethnicity"><Select value={gfrParams.ethnicity} onChange={v => setGfrParams(p => ({ ...p, ethnicity: v }))}><Select.Option value="">Other</Select.Option><Select.Option value="black">Black</Select.Option></Select></Form.Item></Col>
        <Col span={8}><Form.Item label="Body Weight (kg)"><InputNumber min={0} value={gfrParams.weight} onChange={v => setGfrParams(p => ({ ...p, weight: v }))} style={{ width: '100%' }} /></Form.Item></Col>
        <Col span={8}><Alert type="info" showIcon message={`eGFR: ${calcGFR() || '--'} mL/min/1.73m²`} /></Col>
      </Row>


      <Divider orientation="left">Braden Scale (Pressure Sore Risk)</Divider>
      <Row gutter={8}>
        <Col span={8}>
          <Form.Item label={<span>Sensory Perception<br /><small>Ability to respond meaningfully to pressure-related discomfort</small></span>}>
            <Select value={braden.sensory} onChange={v => setBraden(b => ({ ...b, sensory: v }))}>
              <Select.Option value={1}>Completely limited</Select.Option>
              <Select.Option value={2}>Very limited</Select.Option>
              <Select.Option value={3}>Slightly limited</Select.Option>
              <Select.Option value={4}>No impairment</Select.Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={8}>
          <Form.Item label={<span>Moisture<br /><small>Degree to which skin is exposed to moisture</small></span>}>
            <Select value={braden.moisture} onChange={v => setBraden(b => ({ ...b, moisture: v }))}>
              <Select.Option value={1}>Constantly moist</Select.Option>
              <Select.Option value={2}>Very moist</Select.Option>
              <Select.Option value={3}>Occasionally moist</Select.Option>
              <Select.Option value={4}>Rarely moist</Select.Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={8}>
          <Form.Item label={<span>Activity<br /><small>Degree of physical activity</small></span>}>
            <Select value={braden.activity} onChange={v => setBraden(b => ({ ...b, activity: v }))}>
              <Select.Option value={1}>Bedfast</Select.Option>
              <Select.Option value={2}>Chairfast</Select.Option>
              <Select.Option value={3}>Walks occasionally</Select.Option>
              <Select.Option value={4}>Walks frequently</Select.Option>
            </Select>
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={8}>
        <Col span={8}>
          <Form.Item label={<span>Mobility<br /><small>Ability to change and control body position</small></span>}>
            <Select value={braden.mobility} onChange={v => setBraden(b => ({ ...b, mobility: v }))}>
              <Select.Option value={1}>Completely immobile</Select.Option>
              <Select.Option value={2}>Very limited</Select.Option>
              <Select.Option value={3}>Slightly limited</Select.Option>
              <Select.Option value={4}>No limitations</Select.Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={8}>
          <Form.Item label={<span>Nutrition<br /><small>Usual food intake pattern</small></span>}>
            <Select value={braden.nutrition} onChange={v => setBraden(b => ({ ...b, nutrition: v }))}>
              <Select.Option value={1}>Very poor</Select.Option>
              <Select.Option value={2}>Probably inadequate</Select.Option>
              <Select.Option value={3}>Adequate</Select.Option>
              <Select.Option value={4}>Excellent</Select.Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={8}>
          <Form.Item label={<span>Friction/Shear<br /><small>Amount of assistance needed to move and degree of sliding in bed/chair</small></span>}>
            <Select value={braden.friction} onChange={v => setBraden(b => ({ ...b, friction: v }))}>
              <Select.Option value={1}>Problem</Select.Option>
              <Select.Option value={2}>Potential problem</Select.Option>
              <Select.Option value={3}>No apparent problem</Select.Option>
            </Select>
          </Form.Item>
        </Col>
      </Row>
      <Alert type="info" showIcon message={`Braden Total: ${bradenTotal} | Risk: ${bradenRisk}`} description={bradenAction} style={{ marginBottom: 16 }} />

      <Divider orientation="left">DVT Risk (Wells Score)</Divider>
      <Row gutter={8}>
        {wellsList.map(item => (
          <Col span={12} key={item.key} style={{ marginBottom: 8 }}>
            <Checkbox checked={!!wells[item.key]} onChange={e => setWells(w => ({ ...w, [item.key]: e.target.checked }))}>{item.label} ({item.pts > 0 ? '+' : ''}{item.pts})</Checkbox>
          </Col>
        ))}
      </Row>
      <Alert type="info" showIcon message={`Wells Score: ${wellsScore} | Risk: ${wellsRisk}`} description={wellsAction} style={{ marginBottom: 16 }} />

      <Divider orientation="left">Nutritional Requirements</Divider>
      <Row gutter={8}>
        <Col span={6}><Form.Item label="Body Weight (kg)"><InputNumber min={0} value={nutrition.weight} onChange={v => setNutrition(n => ({ ...n, weight: v }))} style={{ width: '100%' }} /></Form.Item></Col>
        <Col span={6}><Form.Item label="Illness Type"><Select value={nutrition.illness} onChange={v => setNutrition(n => ({ ...n, illness: v }))} style={{ width: '100%' }}><Select.Option value="normal">Normal</Select.Option><Select.Option value="moderate">Moderately ill</Select.Option><Select.Option value="critical">Critically ill (ICU)</Select.Option><Select.Option value="burn">Burn patient</Select.Option></Select></Form.Item></Col>
        <Col span={6}><Form.Item label="Co-morbidities"><Select mode="multiple" value={comorbidities} onChange={setComorbidities} style={{ width: '100%' }} placeholder="Select co-morbidities">{comorbidityOptions.map(opt => <Select.Option key={opt} value={opt}>{opt}</Select.Option>)}</Select></Form.Item></Col>
        <Col span={6}><Alert type="info" showIcon message={`Calories: ${calReq || '--'} kcal/day | Protein: ${protReq || '--'} g/day`} /></Col>
      </Row>

      <Typography.Title level={5} style={{ marginTop: 8 }}>Key Micronutrients</Typography.Title>
      <table style={{ width: '100%', marginBottom: 16 }}>
        <thead><tr><th>Name</th><th>Daily Dose</th><th>Role</th></tr></thead>
        <tbody>
          {micronutrients.map(m => <tr key={m.name}><td>{m.name}</td><td>{m.dose}</td><td>{m.role}</td></tr>)}
        </tbody>
      </table>

      <Divider orientation="left">7-Day Meal Plan (Nigeria)</Divider>
      <Button type="primary" onClick={generateMealPlan} style={{ marginBottom: 8 }}>Generate Meal Plan</Button>
      {mealPlanError && <Alert type="error" message={mealPlanError} style={{ marginBottom: 8 }} />}
      {mealPlan && mealPlan.map(day => (
        <div key={day.day} style={{ marginBottom: 12 }}>
          <Typography.Text strong>Day {day.day}:</Typography.Text> Total kcal: {day.kcal}, Protein: {day.protein}g
          {['Breakfast', 'Lunch', 'Dinner', 'Snack'].map(mealType => (
            <div key={mealType} style={{ margin: '8px 0' }}>
              <Typography.Text underline>{mealType}</Typography.Text>
              <table style={{ width: '100%', fontSize: 12, marginTop: 2, marginBottom: 2 }}>
                <thead><tr><th>Food</th><th>Portion</th><th>kcal</th><th>Protein (g)</th></tr></thead>
                <tbody>
                  {day.meals[mealType].map((m, idx) => <tr key={idx}><td>{m.name}</td><td>{m.portion}</td><td>{m.kcal}</td><td>{m.protein}</td></tr>)}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      ))}
      {mealPlan && <Button onClick={exportMealPlanPDF} style={{ marginBottom: 16 }}>Export Meal Plan as PDF</Button>}

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>Save</Button>
        <Button type="link" onClick={onCancel}>Cancel</Button>
      </Form.Item>
    </Form>
  );

  if (isMobile) {
    return (
      <Drawer
        title="Clinical Evaluation"
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

export default ClinicalForm;
