import React, { useState } from "react";

export default function Register({ onRegistered = () => {} }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [autoValidate, setAutoValidate] = useState(true);
  const [error, setError] = useState("");

  // Normalize base so trailing "/api" in env doesn't cause double "/api/api"
  const API_BASE = (process.env.REACT_APP_API_URL || "http://localhost:8000").replace(/\/api\/?$/, "") + "/api";

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${API_BASE}/auth/register?auto_validate=${autoValidate}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, is_admin: isAdmin })
      });
      if (!res.ok) {
        const text = await res.text();
        setError(`Register failed: ${res.status} ${text}`);
        return;
      }
      const data = await res.json();
      // store token and consider user logged in immediately (auto-login)
      localStorage.setItem("token", data.access_token);
      onRegistered();
    } catch (err) {
      setError(String(err));
    }
  };

  return (
    <div style={{padding:20}}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input type="password" name="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <label>
          <input type="checkbox" checked={isAdmin} onChange={e=>setIsAdmin(e.target.checked)} /> Register as admin
        </label>
        <label>
          <input type="checkbox" checked={autoValidate} onChange={e=>setAutoValidate(e.target.checked)} /> Auto-validate account (skip verification)
        </label>
        <button type="submit">Register</button>
        {error ? <div className="error">{error}</div> : null}
      </form>
    </div>
  );
}