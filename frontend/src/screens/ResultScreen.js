import React from 'react';
import { RotateCcw, CheckCircle } from 'lucide-react';
import './ResultScreen.css';

function ResultScreen({ result, onNewCapture }) {
  if (!result) {
    return null;
  }

  const categoryColor = result.color || '#7f8c8d';
  const confidenceColor = {
    'High': '#2ecc71',
    'Medium': '#f39c12',
    'Low': '#e74c3c'
  }[result.confidence] || '#95a5a6';

  return (
    <div className="result-container">
      <div className="result-card">
        <div className="result-header">
          <h1 className="result-title">Analysis Result</h1>
        </div>

        <div className="result-body">
          {/* Object Identification */}
          <div className="result-section">
            <h2 className="section-title">Object Identified</h2>
            <p className="object-name">{result.object || 'Unable to identify'}</p>
          </div>

          {/* Category Badge */}
          <div className="result-section">
            <h2 className="section-title">Waste Category</h2>
            <div
              className="category-badge"
              style={{ backgroundColor: categoryColor }}
            >
              {result.category}
            </div>
          </div>

          {/* Confidence Level */}
          <div className="result-section">
            <h2 className="section-title">Confidence Level</h2>
            <div
              className="confidence-badge"
              style={{ borderColor: confidenceColor, color: confidenceColor }}
            >
              {result.confidence || 'Medium'}
            </div>
          </div>

          {/* Disposal Instructions */}
          <div className="result-section instructions-section">
            <h2 className="section-title">
              <CheckCircle size={20} />
              Disposal Instructions
            </h2>
            <p className="instruction-text">
              {result.instruction || 'Please refer to local waste management guidelines'}
            </p>
          </div>
        </div>

        <div className="button-group">
          <button className="btn btn-secondary" onClick={onNewCapture}>
            <RotateCcw size={20} />
            Classify Another Item
          </button>
        </div>

        <div className="category-legend">
          <h3>Category Guide</h3>
          <div className="legend-grid">
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#2ecc71' }}></span>
              <span>Wet Waste</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#3498db' }}></span>
              <span>Dry Waste</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#f1c40f' }}></span>
              <span>Plastic</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#95a5a6' }}></span>
              <span>Metal</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#1abc9c' }}></span>
              <span>Glass</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#9b59b6' }}></span>
              <span>E-Waste</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#e74c3c' }}></span>
              <span>Hazardous</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#7f8c8d' }}></span>
              <span>Unknown</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultScreen;
