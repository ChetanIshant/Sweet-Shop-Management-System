import React, { useState } from 'react';

export default function SweetForm({ onAdded = () => {} }) {
  const [form, setForm] = useState({ name: '', category: '', price: '', quantity: '' });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = e => {
    e.preventDefault();
    onAdded({
      id: Date.now(),
      name: form.name,
      category: form.category,
      price: parseFloat(form.price || 0),
      quantity: parseInt(form.quantity || 0, 10)
    });
    setForm({ name: '', category: '', price: '', quantity: '' });
  };

  return (
    <div style={{padding:20}}>
      <h3>Add / Edit Sweet</h3>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
        <input name="category" placeholder="Category" value={form.category} onChange={handleChange} />
        <input name="price" placeholder="Price" value={form.price} onChange={handleChange} />
        <input name="quantity" placeholder="Quantity" value={form.quantity} onChange={handleChange} />
        <button type="submit">Save</button>
      </form>
    </div>
  );
}