import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Clinical Console title', () => {
  render(<App />);
  // Look for the main title from Login page
  const title = screen.getByText(/clinical console/i);
  expect(title).toBeInTheDocument();
});
