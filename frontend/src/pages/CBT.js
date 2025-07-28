import React, { useEffect, useState, useRef, useCallback } from 'react';
import { Button, Typography, message } from 'antd';
import { authFetch } from '../utils/api';

const CBT = () => {
  const [questions, setQuestions] = useState([]);
  const [idx, setIdx] = useState(0);
  const [score, setScore] = useState(0);
  const [result, setResult] = useState(null); // { percentage, recommendation, advice }
  const [countdown, setCountdown] = useState(30);
  const [selected, setSelected] = useState(null);
  const timer = useRef();

  useEffect(() => {
    // Fetch diagnoses, then generate MCQs
    const fetchQuestions = async () => {
      try {
        const diagData = await authFetch('/api/cbt/weekly-diagnoses');
        console.log('diagData:', diagData); // Debug log
        let diagnoses = [];
        if (Array.isArray(diagData)) {
          diagnoses = diagData.map(d => d.diagnosis);
        } else if (Array.isArray(diagData.diagnoses)) {
          diagnoses = diagData.diagnoses.map(d => d.diagnosis);
        }
        if (!diagnoses.length) {
          message.info('No weekly diagnoses found. Using default diagnosis for testing.');
          diagnoses = ['Test Diagnosis'];
        }
        const data = await authFetch('/api/cbt/generate-mcqs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ diagnoses }),
        });
        setQuestions(data.questions);
      } catch (err) {
        message.error('Failed to generate MCQs. Please check your backend or try again later.');
        setQuestions([]);
      }
    };
    fetchQuestions();
  }, []);








  const handleNext = useCallback(() => {
    if (selected && selected === questions[idx].answer) setScore(s => s + 4);
    setSelected(null);
    setIdx(i => i + 1);
  }, [selected, questions, idx]);

  useEffect(() => {
    if (idx >= questions.length) return;
    setCountdown(30);
    timer.current = setInterval(() => {
      setCountdown(c => {
        if (c <= 1) {
          handleNext();
          return 30;
        }
        return c - 1;
      });
    }, 1000);
    return () => clearInterval(timer.current);
  }, [idx, questions, handleNext]);

  const handleSelect = (option) => setSelected(option);

  const handleFinish = async () => {
    try {
      const res = await authFetch('/api/cbt/submit-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score }),
      });
      setResult(res);
      message.success(`Test complete! Your score: ${score}`);
    } catch (err) {
      message.error('Failed to submit score.');
    }
  };

  if (!questions.length) return <div>Loading questions...</div>;
  if (idx >= questions.length) return (
    <div>
      <Typography.Title level={3}>Test complete!</Typography.Title>
      <div style={{ fontSize: 20, margin: '12px 0' }}>Your score: {score}</div>
      {result && (
        <div style={{ marginTop: 16 }}>
          <div><b>Percentage:</b> {result.percentage?.toFixed(1)}%</div>
          <div><b>Recommendation:</b> {result.recommendation}</div>
          <div><b>Advice:</b> {result.advice}</div>
        </div>
      )}
    </div>
  );

  const q = questions[idx];
  return (
    <div>
      <Typography.Title level={3}>CBT Test</Typography.Title>
      <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 8 }}>Time left: {countdown}s</div>
      <div style={{ marginBottom: 16 }}>{q.question}</div>
      {['a','b','c','d','e'].map(opt => (
        <Button
          key={opt}
          type={selected === opt ? 'primary' : 'default'}
          onClick={() => handleSelect(opt)}
          style={{ display: 'block', margin: '8px 0', width: 200 }}
        >
          {opt}. {q.options[opt]}
        </Button>
      ))}
      <Button type="primary" onClick={handleNext} style={{ marginTop: 16 }}>Next</Button>
      {idx === questions.length - 1 && (
        <Button type="primary" onClick={handleFinish} style={{ marginLeft: 16 }}>Finish</Button>
      )}
    </div>
  );
};

export default CBT;
