import React from 'react';
import appBackgroundStyle from '../appBackground';

const PageBackground = ({ children }) => (
  <div style={appBackgroundStyle}>
    {children}
  </div>
);

export default PageBackground;
