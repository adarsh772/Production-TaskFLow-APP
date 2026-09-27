# TaskFlow — React frontend

A React (Vite) frontend for the TaskFlow FastAPI backend: register/login,
JWT stored in `localStorage`, and full task CRUD.

## Structure

```
src/
├── api/client.js            # fetch wrapper + typed calls (auth + tasks)
├── context/AuthContext.jsx  # token/user state, login/register/logout
├── components/
│   ├── AuthPage.jsx          # toggles between Login/Register
│   ├── LoginForm.jsx
│   ├── RegisterForm.jsx
│   ├── Dashboard.jsx         # header + task list, shown once logged in
│   ├── TaskForm.jsx          # add-task input row
│   ├── TaskList.jsx          # fetches/refreshes tasks, wires up actions
│   └── TaskItem.jsx          # one task row (toggle complete / delete)
├── App.jsx
├── main.jsx
└── index.css
```

## Setup

1. Point it at your backend:

   ```bash
   cp .env.example .env
   # edit VITE_API_BASE_URL if your API isn't on http://localhost:8000
   ```

2. Install and run:

   ```bash
   npm install
   npm run dev
   ```

   This assumes the `Complete-TaskManager` backend is already running (see its
   own README) and its `ALLOWED_ORIGINS` includes this dev server's origin
   (default Vite dev server: `http://localhost:5173`).

3. Build for production:

   ```bash
   npm run build   # outputs to dist/
   npm run preview # serve the production build locally
   ```

## Notes

- Auth: on login, the JWT is stored in `localStorage` and attached as
  `Authorization: Bearer <token>` on every task request. On load, if a token
  is present it's validated against `GET /user/me`; if that fails (expired/
  invalid) the user is dropped back to the login screen.
- Tasks are always scoped to the logged-in user by the backend, so this
  frontend never needs to filter anything client-side.
- No external UI or state libraries — just React hooks and Context, to keep
  the codebase easy to read and extend.
