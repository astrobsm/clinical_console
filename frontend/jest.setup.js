// Global Jest setup for all frontend tests
// Mock window.matchMedia for Ant Design
if (!window.matchMedia) {
  window.matchMedia = function(query) {
    return {
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(), // deprecated
      removeListener: jest.fn(), // deprecated
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    };
  };
}
// Mock window.innerWidth for desktop
Object.defineProperty(window, 'innerWidth', { writable: true, configurable: true, value: 1024 });
// Mock HTMLCanvasElement.getContext for jsPDF and canvas
if (!HTMLCanvasElement.prototype.getContext) {
  HTMLCanvasElement.prototype.getContext = () => ({
    fillRect: () => {},
    clearRect: () => {},
    getImageData: () => ({ data: [] }),
    putImageData: () => {},
    createImageData: () => [],
    setTransform: () => {},
    drawImage: () => {},
    getTransform: () => ({ a:1, b:0, c:0, d:1, e:0, f:0 }),
    resetTransform: () => {},
    scale: () => {},
    rotate: () => {},
    translate: () => {},
    save: () => {},
    restore: () => {},
    beginPath: () => {},
    moveTo: () => {},
    lineTo: () => {},
    closePath: () => {},
    stroke: () => {},
    arc: () => {},
    fill: () => {},
    measureText: () => ({ width: 0 }),
    transform: () => {},
    rect: () => {},
    clip: () => {},
  });
}
