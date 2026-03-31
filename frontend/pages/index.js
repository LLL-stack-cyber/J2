import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ fontFamily: 'Inter, Arial', maxWidth: 920, margin: '0 auto', padding: 24 }}>
      <h1>Jarvis AI Study Agent</h1>
      <p>Smart tutoring with RAG notes retrieval, quizzes, and exam analysis.</p>
      <p>
        <Link href="/login">Login</Link> · <Link href="/dashboard">Open Dashboard</Link>
      </p>
    </main>
  );
}
