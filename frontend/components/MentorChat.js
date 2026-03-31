import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function MentorChat() {
  const [question, setQuestion] = useState('How can I revise faster for finals?');
  const [answer, setAnswer] = useState('');

  const askMentor = async () => {
    const response = await fetch(`${API_BASE}/api/mentor/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'demo-user', question, context: 'final exam in 2 weeks' })
    });
    const data = await response.json();
    setAnswer(data.answer || 'No response.');
  };

  return (
    <section style={{ border: '1px solid #ddd', borderRadius: 12, padding: 16 }}>
      <h3>AI Mentor</h3>
      <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={3} style={{ width: '100%' }} />
      <button onClick={askMentor}>Ask Jarvis</button>
      {answer && <pre style={{ whiteSpace: 'pre-wrap' }}>{answer}</pre>}
    </section>
  );
}
