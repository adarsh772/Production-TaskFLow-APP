export default function TaskItem({ task, onToggle, onDelete }) {
  return (
    <div className={`taskrow${task.is_completed ? " done" : ""}`}>
      <input
        type="checkbox"
        checked={task.is_completed}
        onChange={(e) => onToggle(task, e.target.checked)}
      />
      <div className="grow">
        <div className="title">{task.title}</div>
        {task.description && <div className="desc">{task.description}</div>}
      </div>
      <button type="button" className="danger" onClick={() => onDelete(task.id)}>
        Delete
      </button>
    </div>
  );
}
