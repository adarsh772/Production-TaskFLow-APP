const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, { method = "GET", token, body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    // 204 No Content has no body
  }

  if (!res.ok) {
    const message = (data && (data.detail || data.message)) || `Request failed (${res.status})`;
    throw new Error(typeof message === "string" ? message : "Request failed");
  }

  return data;
}

export const authApi = {
  register: ({ name, username, email, password }) =>
    request("/user/register", { method: "POST", body: { name, username, email, password } }),
  login: ({ username, password }) =>
    request("/user/login", { method: "POST", body: { username, password } }),
  me: (token) => request("/user/me", { token }),
};

export const taskApi = {
  list: (token) => request("/tasks/all_task", { token }),
  create: (token, { title, description, is_completed = false }) =>
    request("/tasks/create", { method: "POST", token, body: { title, description, is_completed } }),
  update: (token, id, { title, description, is_completed }) =>
    request(`/tasks/update/${id}`, { method: "PUT", token, body: { title, description, is_completed } }),
  remove: (token, id) => request(`/tasks/delete/${id}`, { method: "DELETE", token }),
};
