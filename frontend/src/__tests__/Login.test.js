import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from '../pages/Login';

// Mock window.innerWidth to always be desktop
beforeAll(() => {
  Object.defineProperty(window, 'innerWidth', { writable: true, configurable: true, value: 1024 });
});

// Capture console errors for debugging
beforeEach(() => {
  jest.spyOn(console, 'error').mockImplementation((...args) => {
    // Print errors to help debug
    process.stdout.write(`console.error: ${args.join(' ')}\n`);
  });
});
afterEach(() => {
  jest.restoreAllMocks();
});

describe('Login Component', () => {
  it('renders login form and validates required fields', async () => {
    let renderError = null;
    try {
      render(<Login onLogin={jest.fn()} onSwitchToRegister={jest.fn()} />);
    } catch (err) {
      renderError = err;
      // Print the error for debugging
      // eslint-disable-next-line no-console
      console.log('Render error:', err);
    }
    expect(renderError).toBeNull();
    expect(screen.getByText(/CLINICAL CONSOLE/i)).toBeInTheDocument();
    // Find the Login button by role and name
    const loginButton = screen.getAllByRole('button', { name: /login/i })[0];
    fireEvent.click(loginButton);
    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid email/i)).toBeInTheDocument();
      expect(screen.getByText(/Please enter password/i)).toBeInTheDocument();
      expect(screen.getByText(/Please select role/i)).toBeInTheDocument();
    });
  });
});
