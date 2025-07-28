// Mock for jsPDF to avoid canvas errors in Jest
function jsPDF() {}
jsPDF.prototype.save = jest.fn();
module.exports = jsPDF;
module.exports.default = jsPDF;
