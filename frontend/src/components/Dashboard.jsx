import { useAuth } from "../context/AuthContext";
import TaskList from "./TaskList";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="wrap">
      <div className="row header-row">
        <div className="grow">
          <h1>TaskFlow</h1>
          <p className="sub">Signed in as <b>{user?.username}</b></p>
        </div>
        <button type="button" className="secondary" onClick={logout}>Log out</button>
      </div>
      <TaskList />
    </div>
  );
}
