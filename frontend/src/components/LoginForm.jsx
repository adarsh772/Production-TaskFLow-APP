import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function LoginForm({ onSwitchToRegister }) {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login({ username, password });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>Log in</h2>
      <div className="field">
        <label htmlFor="login-username">Username</label>
        <input id="login-username" value={username} onChange={(e) => setUsername(e.target.value)} required />
      </div>
      <div className="field">
        <label htmlFor="login-password">Password</label>
        <input
          id="login-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={submitting}>
        {submitting ? "Logging in…" : "Log in"}
      </button>
      {error && <p className="msg error">{error}</p>}
      <p className="switch">
        No account? <button type="button" className="link" onClick={onSwitchToRegister}>Register</button>
      </p>
    </form>
  );
}
