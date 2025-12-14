const API_BASE = (process.env.REACT_APP_API_URL || "http://localhost:8000").replace(/\/api\/?$/, "") + "/api";

export async function register(payload) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form.toString(),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } : { "Content-Type": "application/json" };
}

export async function fetchSweets() {
  const res = await fetch(`${API_BASE}/sweets`, { headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function addSweet(payload) {
  const res = await fetch(`${API_BASE}/sweets`, { method: "POST", headers: authHeaders(), body: JSON.stringify(payload) });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function purchaseSweet(id, quantity=1) {
  const res = await fetch(`${API_BASE}/sweets/${id}/purchase?quantity=${quantity}`, { method: "POST", headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function restockSweet(id, quantity=1) {
  const res = await fetch(`${API_BASE}/sweets/${id}/restock?quantity=${quantity}`, { method: "POST", headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function deleteSweet(id) {
  const res = await fetch(`${API_BASE}/sweets/${id}`, { method: "DELETE", headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function searchSweets(query) {
  const params = new URLSearchParams(query).toString();
  const res = await fetch(`${API_BASE}/sweets/search?${params}`, { headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}