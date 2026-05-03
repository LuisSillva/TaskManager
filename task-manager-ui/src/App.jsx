import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:8000";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [search, setSearch] = useState("");
  const [filterDone, setFilterDone] = useState("");

  const fetchTasks = async () => {
    const params = {};
    if (search) params.search = search;
    if (filterDone !== "") params.done = filterDone;
    const res = await axios.get(`${API}/tasks`, { params });
    setTasks(res.data);
  };

  useEffect(() => {
    fetchTasks();
  }, [search, filterDone]);

  const createTask = async () => {
    if (!title.trim()) return;
    await axios.post(`${API}/tasks`, { title });
    setTitle("");
    fetchTasks();
  };

  const toggleDone = async (task) => {
    await axios.put(`${API}/tasks/${task.id}`, { done: !task.done });
    fetchTasks();
  };

  const deleteTask = async (id) => {
    await axios.delete(`${API}/tasks/${id}`);
    fetchTasks();
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Task Manager</h1>

      {/* Create task */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="New task..."
          style={{ flex: 1, padding: 8 }}
        />
        <button onClick={createTask}>Add</button>
      </div>

      {/* Filters */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search..."
          style={{ flex: 1, padding: 8 }}
        />
        <select value={filterDone} onChange={e => setFilterDone(e.target.value)}>
          <option value="">All</option>
          <option value="false">Pending</option>
          <option value="true">Done</option>
        </select>
      </div>

      {/* Task list */}
      {tasks.map(task => (
        <div key={task.id} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
          <input
            type="checkbox"
            checked={task.done}
            onChange={() => toggleDone(task)}
          />
          <span style={{ flex: 1, textDecoration: task.done ? "line-through" : "none" }}>
            {task.title}
          </span>
          <button onClick={() => deleteTask(task.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default App;