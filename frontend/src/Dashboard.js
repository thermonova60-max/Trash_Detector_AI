import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import CaptureScreen from './screens/CaptureScreen';
import ResultScreen from './screens/ResultScreen';

function Dashboard() {
  const [showClassifier, setShowClassifier] = useState(false);
  const [apiStatus, setApiStatus] = useState(null);
  const [currentScreen, setCurrentScreen] = useState('capture');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch API status on mount
  useEffect(() => {
    fetch('http://localhost:8000/')
      .then(r => r.json())
      .then(data => setApiStatus(data))
      .catch(err => console.error(err));
  }, []);

  const handleImageCapture = async (file) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/classify', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        setResult(data.data);
        setCurrentScreen('result');
      } else {
        alert('Classification failed: ' + data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error communicating with API');
    } finally {
      setLoading(false);
    }
  };

  const handleNewCapture = () => {
    setResult(null);
    setCurrentScreen('capture');
  };

  // Show classifier if requested
  if (showClassifier) {
    return (
      <div className="app">
        <button className="back-btn" onClick={() => setShowClassifier(false)}>
          ← Back to Dashboard
        </button>
        {currentScreen === 'capture' ? (
          <CaptureScreen onCapture={handleImageCapture} loading={loading} />
        ) : (
          <ResultScreen result={result} onNewCapture={handleNewCapture} />
        )}
      </div>
    );
  }

  // Show dashboard
  return (
    <div className="dashboard">
      <div className="dashboard-container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h1 className="title">TrashCollector AI</h1>
            <p className="subtitle">Smart Waste Segregation System</p>
          </div>
        </header>

        {/* API Status Card */}
        {apiStatus && (
          <div className="status-card">
            <h2 className="card-title">System Status</h2>
            <div className="status-grid">
              <div className="status-item">
                <span className="status-label">Service</span>
                <span className="status-value">{apiStatus.name}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Version</span>
                <span className="status-value">{apiStatus.version}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Status</span>
                <span className="status-value active">{apiStatus.status}</span>
              </div>
            </div>
          </div>
        )}

        {/* Features */}
        <section className="features">
          <h2>Key Features</h2>
          <div className="features-grid">
            <div className="feature">
              <div className="feature-icon">🎯</div>
              <h3>AI-Powered Classification</h3>
              <p>Uses advanced vision-language models for accurate waste identification</p>
            </div>
            <div className="feature">
              <div className="feature-icon">📸</div>
              <h3>Image Recognition</h3>
              <p>Upload any waste item image for instant classification</p>
            </div>
            <div className="feature">
              <div className="feature-icon">♻️</div>
              <h3>Smart Segregation</h3>
              <p>Automatically categorizes into 8 waste types</p>
            </div>
            <div className="feature">
              <div className="feature-icon">🚀</div>
              <h3>Offline Processing</h3>
              <p>All processing happens locally with Ollama</p>
            </div>
          </div>
        </section>

        {/* Waste Categories */}
        <section className="categories">
          <h2>Waste Categories</h2>
          <div className="categories-grid">
            <div className="category" style={{ borderLeftColor: '#2ecc71' }}>
              <span className="category-icon">🟢</span>
              <span className="category-name">Wet</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#3498db' }}>
              <span className="category-icon">🔵</span>
              <span className="category-name">Dry</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#f1c40f' }}>
              <span className="category-icon">🟡</span>
              <span className="category-name">Plastic</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#95a5a6' }}>
              <span className="category-icon">⚫</span>
              <span className="category-name">Metal</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#1abc9c' }}>
              <span className="category-icon">🔷</span>
              <span className="category-name">Glass</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#9b59b6' }}>
              <span className="category-icon">🟣</span>
              <span className="category-name">E-Waste</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#e74c3c' }}>
              <span className="category-icon">🔴</span>
              <span className="category-name">Hazardous</span>
            </div>
            <div className="category" style={{ borderLeftColor: '#7f8c8d' }}>
              <span className="category-icon">⚪</span>
              <span className="category-name">Unknown</span>
            </div>
          </div>
        </section>

        {/* CTA Button */}
        <section className="cta-section">
          <button 
            className="cta-button"
            onClick={() => setShowClassifier(true)}
          >
            Start Classifying Waste
          </button>
        </section>

        {/* Footer */}
        <footer className="footer">
          <p>TrashCollector AI v1.0.0 | Vision-based waste segregation</p>
        </footer>
      </div>
    </div>
  );
}

export default Dashboard;
