import { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function AuthPage() {
  const [mode, setMode] = useState("login");

  return (
    <div className="wrap">
      <h1>TaskFlow</h1>
      <p className="sub">Sign in to manage your tasks.</p>
      {mode === "login" ? (
        <LoginForm onSwitchToRegister={() => setMode("register")} />
      ) : (
        <RegisterForm onSwitchToLogin={() => setMode("login")} />
      )}
    </div>
  );
}
