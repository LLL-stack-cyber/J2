import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function Login() {
  const [email, setEmail] = useState('student@example.com');
  const [password, setPassword] = useState('password123');
  const [token, setToken] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    const response = await fetch(`${API_BASE}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    setToken(data.access_token || data.detail || 'Login failed');
  };

  return (
    <main style={{ fontFamily: 'Inter, Arial', maxWidth: 460, margin: '0 auto', padding: 24 }}>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <br /><br />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <br /><br />
        <button type="submit">Login</button>
      </form>
      {token && <p>Token: {token}</p>}
    </main>
  );
}
