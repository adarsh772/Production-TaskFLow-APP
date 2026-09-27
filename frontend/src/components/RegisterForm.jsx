import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function RegisterForm({ onSwitchToLogin }) {
  const { register } = useAuth();
  const [form, setForm] = useState({ name: "", username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register(form);
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (success) {
    return (
      <div className="card">
        <h2>Account created</h2>
        <p className="msg ok">You can log in now.</p>
        <button type="button" onClick={onSwitchToLogin}>Go to login</button>
      </div>
    );
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>Register</h2>
      <div className="field">
        <label htmlFor="reg-name">Name</label>
        <input id="reg-name" value={form.name} onChange={update("name")} required />
      </div>
      <div className="field">
        <label htmlFor="reg-username">Username</label>
        <input id="reg-username" value={form.username} onChange={update("username")} required />
      </div>
      <div className="field">
        <label htmlFor="reg-email">Email</label>
        <input id="reg-email" type="email" value={form.email} onChange={update("email")} required />
      </div>
      <div className="field">
        <label htmlFor="reg-password">Password (min 8 chars)</label>
        <input
          id="reg-password"
          type="password"
          minLength={8}
          value={form.password}
          onChange={update("password")}
          required
        />
      </div>
      <button type="submit" disabled={submitting}>
        {submitting ? "Creating…" : "Create account"}
      </button>
      {error && <p className="msg error">{error}</p>}
      <p className="switch">
        Already have an account? <button type="button" className="link" onClick={onSwitchToLogin}>Log in</button>
      </p>
    </form>
  );
}
