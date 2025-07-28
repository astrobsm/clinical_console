const path = require('path');
module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },
  moduleFileExtensions: ['js', 'jsx'],
  setupFilesAfterEnv: ['@testing-library/jest-dom'],
  setupFiles: [
    '<rootDir>/jest.setup.js'
  ],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(png|jpg|jpeg|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '^jspdf$': '<rootDir>/__mocks__/jspdf.js',
    // Force all imports of react and react-dom to resolve to the root node_modules
    '^react$': path.resolve(__dirname, 'node_modules/react'),
    '^react-dom$': path.resolve(__dirname, 'node_modules/react-dom'),
  },
};
