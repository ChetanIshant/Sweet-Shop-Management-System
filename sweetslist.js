import React from 'react';

export default function SweetsList({ sweets = [], onPurchase = () => {} }) {
  return (
    <div style={{padding:20}}>
      <h2>Available Sweets</h2>
      {sweets.length === 0 ? (
        <p>No sweets available.</p>
      ) : (
        <ul>
          {sweets.map(s => (
            <li key={s.id}>
              {s.name} — {s.category} — ${s.price} — qty: {s.quantity}
              <button style={{marginLeft:10}} disabled={s.quantity === 0} onClick={() => onPurchase(s.id)}>Purchase</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}