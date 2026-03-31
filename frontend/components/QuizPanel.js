import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function QuizPanel() {
  const [topic, setTopic] = useState('Operating Systems');
  const [questions, setQuestions] = useState([]);

  const generateQuiz = async () => {
    const response = await fetch(`${API_BASE}/api/quiz/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, difficulty: 'medium', count: 3 })
    });
    const data = await response.json();
    setQuestions(data.questions || []);
  };

  return (
    <section style={{ border: '1px solid #ddd', borderRadius: 12, padding: 16 }}>
      <h3>Quiz Generator</h3>
      <input value={topic} onChange={(e) => setTopic(e.target.value)} />
      <button onClick={generateQuiz} style={{ marginLeft: 8 }}>Generate</button>
      <ol>
        {questions.map((q) => (
          <li key={q.id}>{q.question}</li>
        ))}
      </ol>
    </section>
  );
}
