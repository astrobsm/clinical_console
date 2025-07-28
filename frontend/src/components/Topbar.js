import React from 'react';
import './Topbar.css';

const Topbar = ({ user }) => (
  <header className="topbar">
    <div className="topbar-title">Burns, Plastic & Reconstructive Surgery EMR</div>
    <div className="topbar-user">{user && `Welcome, ${user}`}</div>
  </header>
);

export default Topbar;
