import { useAuth, AuthProvider } from "./context/AuthContext";
import AuthPage from "./components/AuthPage";
import Dashboard from "./components/Dashboard";
import "./index.css";

function Shell() {
  const { token, user, loading } = useAuth();

  if (loading) {
    return (
      <div className="wrap">
        <p className="sub">Loading…</p>
      </div>
    );
  }

  return token && user ? <Dashboard /> : <AuthPage />;
}

export default function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  );
}
