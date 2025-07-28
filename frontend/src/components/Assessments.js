import React, { useEffect, useState } from 'react';
import { authFetch } from '../utils/api';

const Assessments = () => {
  const [assessments, setAssessments] = useState([]);
  const [cbt, setCbt] = useState(null);
  const [score, setScore] = useState(null);
  const [result, setResult] = useState(null); // { percentage, recommendation, advice }
  const [loading, setLoading] = useState(true);

  const fetchAssessments = async () => {
    setLoading(true);
    const res = await authFetch('/api/assessments/');
    const data = await res.json();
    if (res.ok) setAssessments(data);
    setLoading(false);
  };

  useEffect(() => { fetchAssessments(); }, []);

  const startCBT = async () => {
    const res = await authFetch('/api/assessments/cbt');
    const data = await res.json();
    if (res.ok) setCbt(data);
  };

  const submitScore = async (assessment_id, value) => {
    try {
      const res = await authFetch('/api/assessments/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ assessment_id, value })
      });
      setScore(value);
      setResult(res);
      fetchAssessments();
    } catch (err) {
      setResult(null);
    }
  };

  return (
    <div>
      <h3>Assessments</h3>
      {loading ? <p>Loading...</p> : (
        <ul>
          {assessments.map(a => (
            <li key={a.id}>
              Scheduled: {a.scheduled_date} | Completed: {a.completed ? 'Yes' : 'No'} | Score: {a.score || '-'}
              {!a.completed && <button style={{ marginLeft: 8 }} onClick={startCBT}>Take CBT</button>}
            </li>
          ))}
        </ul>
      )}
      {cbt && (
        <div style={{ marginTop: 24 }}>
          <h4>CBT Questions</h4>
          <ol>
            {cbt.map((q, i) => (
              <li key={q.id} style={{ marginBottom: 12 }}>
                <div>{q.question}</div>
                <div>
                  {[q.option_a, q.option_b, q.option_c, q.option_d, q.option_e].map((opt, idx) => (
                    <label key={idx} style={{ marginRight: 12 }}>
                      <input type="radio" name={`q${i}`} value={String.fromCharCode(97+idx)} /> {opt}
                    </label>
                  ))}
                </div>
              </li>
            ))}
          </ol>
          <button onClick={() => submitScore(assessments[0]?.id, 100)}>Submit (Demo: 100%)</button>
        </div>
      )}
      {score && (
        <div style={{ color: '#38b000', marginTop: 16 }}>
          Score submitted: {score}
          {result && (
            <div style={{ marginTop: 8 }}>
              <div><b>Percentage:</b> {result.percentage?.toFixed(1)}%</div>
              <div><b>Recommendation:</b> {result.recommendation}</div>
              <div><b>Advice:</b> {result.advice}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Assessments;
