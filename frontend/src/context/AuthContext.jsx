import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { authApi } from "../api/client";

const AuthContext = createContext(null);
const STORAGE_KEY = "taskflow_token";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(STORAGE_KEY));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    authApi
      .me(token)
      .then(setUser)
      .catch(() => {
        // token expired/invalid — drop it
        localStorage.removeItem(STORAGE_KEY);
        setToken(null);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, [token]);

  const login = useCallback(async ({ username, password }) => {
    const { token: newToken } = await authApi.login({ username, password });
    localStorage.setItem(STORAGE_KEY, newToken);
    setToken(newToken);
    const me = await authApi.me(newToken);
    setUser(me);
  }, []);

  const register = useCallback(async (fields) => {
    await authApi.register(fields);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ token, user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
