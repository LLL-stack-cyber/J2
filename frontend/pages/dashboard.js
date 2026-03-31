import UploadNotes from '../components/UploadNotes';
import QuizPanel from '../components/QuizPanel';
import MentorChat from '../components/MentorChat';

export default function Dashboard() {
  return (
    <main style={{ fontFamily: 'Inter, Arial', maxWidth: 980, margin: '0 auto', padding: 24 }}>
      <h1>Study Dashboard</h1>
      <p>Upload notes, generate quizzes, and chat with your Jarvis mentor.</p>
      <div style={{ display: 'grid', gap: 16 }}>
        <UploadNotes />
        <QuizPanel />
        <MentorChat />
      </div>
    </main>
  );
}
