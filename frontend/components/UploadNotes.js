import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function UploadNotes() {
  const [message, setMessage] = useState('');

  const handleUpload = async (event) => {
    event.preventDefault();
    const file = event.target.notes.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', 'demo-user');

    const response = await fetch(`${API_BASE}/api/upload/notes`, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    setMessage(`Uploaded ${data.filename}; indexed chunks: ${data.chunks_indexed}`);
  };

  return (
    <section style={{ border: '1px solid #ddd', borderRadius: 12, padding: 16 }}>
      <h3>Upload Notes</h3>
      <form onSubmit={handleUpload}>
        <input name="notes" type="file" accept=".txt,.md" />
        <button type="submit" style={{ marginLeft: 8 }}>Upload</button>
      </form>
      {message && <p>{message}</p>}
    </section>
  );
}
