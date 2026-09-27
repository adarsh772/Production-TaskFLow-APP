import { useCallback, useEffect, useState } from "react";
import { taskApi } from "../api/client";
import { useAuth } from "../context/AuthContext";
import TaskForm from "./TaskForm";
import TaskItem from "./TaskItem";

export default function TaskList() {
  const { token } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    try {
      const data = await taskApi.list(token);
      setTasks(data.tasks);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const handleAdd = async ({ title, description }) => {
    setError("");
    try {
      await taskApi.create(token, { title, description });
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleToggle = async (task, is_completed) => {
    setError("");
    try {
      await taskApi.update(token, task.id, {
        title: task.title,
        description: task.description,
        is_completed,
      });
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    setError("");
    try {
      await taskApi.remove(token, id);
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card">
      <TaskForm onAdd={handleAdd} />
      {error && <p className="msg error">{error}</p>}
      {loading ? (
        <p className="sub">Loading tasks…</p>
      ) : tasks.length === 0 ? (
        <p className="sub">No tasks yet — add one above.</p>
      ) : (
        <div className="tasklist">
          {tasks.map((task) => (
            <TaskItem key={task.id} task={task} onToggle={handleToggle} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
