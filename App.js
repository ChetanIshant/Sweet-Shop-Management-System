import React, { useEffect, useState } from "react";
import Login from "./components/login";
import Register from "./components/register";
import SweetsList from "./components/sweetslist";
import SweetForm from "./components/sweetform";

const API_ROOT = (process.env.REACT_APP_API_URL || "http://localhost:8000").replace(/\/api\/?$/, "") + "/api";

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));
  const [isAdmin, setIsAdmin] = useState(false);
  const [sweets, setSweets] = useState([]);

  async function refreshProfileAndSweets() {
    const token = localStorage.getItem("token");
    if (!token) {
      setIsAuthenticated(false);
      return;
    }
    try {
      const res = await fetch(`${API_ROOT}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const me = await res.json();
        setIsAuthenticated(true);
        setIsAdmin(me.is_admin === true);
      } else {
        setIsAuthenticated(false);
        setIsAdmin(false);
      }
    } catch (e) {
      setIsAuthenticated(false);
      setIsAdmin(false);
    }

    // fetch sweets
    try {
      const res2 = await fetch(`${API_ROOT}/sweets`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res2.ok) {
        const data = await res2.json();
        setSweets(data);
      } else {
        setSweets([]);
      }
    } catch (e) {
      setSweets([]);
    }
  }

  useEffect(() => { if (isAuthenticated) refreshProfileAndSweets(); }, [isAuthenticated]);

  function loggedIn() { setIsAuthenticated(true); }
  function registered() { setIsAuthenticated(true); }
  function logout() {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    setIsAdmin(false);
    setSweets([]);
  }

  // handler for adding sweet locally (you should POST to backend in real app)
  function handleAddSweet(s) {
    setSweets(prev => [...prev, s]);
  }

  return (
    <div className="container">
      <header>
        <h1>Sweet Shop</h1>
        <div className="actions">
          {isAuthenticated ? <button onClick={logout}>Logout</button> : null}
        </div>
      </header>
      <main>
        {!isAuthenticated ? (
          <div className="auth-grid">
            <Login onLoggedIn={loggedIn} />
            <Register onRegistered={registered} />
          </div>
        ) : (
          <>
            <div className="top-row">
              <SweetsList sweets={sweets} />
              <div>
                <SweetForm onAdded={handleAddSweet} />
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}


/- contact if you have some other optimized code for the same: ishunara25@gmail.com

