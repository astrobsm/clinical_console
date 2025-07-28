import React from 'react';
import './Sidebar.css';

const Sidebar = ({ items, onSelect, selected }) => (
  <nav className="sidebar">
    <div className="sidebar-title">BPRS EMR</div>
    <ul>
      {items.map(item => (
        <li
          key={item.label}
          className={selected === item.label ? 'active' : ''}
          onClick={() => onSelect(item.label)}
        >
          <span className="icon">{item.icon}</span>
          {item.label}
        </li>
      ))}
    </ul>
  </nav>
);

export default Sidebar;
