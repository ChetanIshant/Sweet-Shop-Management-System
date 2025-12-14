import React, { useState } from "react";

export default function Login({ onLoggedIn = () => {} }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Normalize base so trailing "/api" in env doesn't cause double "/api/api"
  const API_BASE = (process.env.REACT_APP_API_URL || "http://localhost:8000").replace(/\/api\/?$/, "") + "/api";

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    try {
      // OAuth2PasswordRequestForm expects form-encoded body
      const body = new URLSearchParams();
      body.append("username", username);
      body.append("password", password);

      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString()
      });

      if (!res.ok) {
        const text = await res.text();
        setError(`Login failed: ${res.status} ${text}`);
        return;
      }
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      onLoggedIn();
    } catch (err) {
      setError(String(err));
    }
  };

  return (
    <div style={{padding:20}}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input type="password" name="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Login</button>
        {error ? <div className="error">{error}</div> : null}
      </form>
    </div>
  );
}