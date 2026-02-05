import React, { useRef } from 'react';
import { Camera, Upload } from 'lucide-react';
import './CaptureScreen.css';

function CaptureScreen({ onCapture, loading }) {
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onCapture(file);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="capture-container">
      <div className="capture-card">
        <h1 className="title">TrashCollector AI</h1>
        <p className="subtitle">Smart Waste Segregation</p>

        <div className="capture-area">
          <div className="icon-wrapper">
            <Camera size={64} />
          </div>
          <p className="instruction">
            Capture or upload an image of the waste item
          </p>
        </div>

        <div className="button-group">
          <button
            className="btn btn-primary"
            onClick={handleUploadClick}
            disabled={loading}
          >
            <Upload size={20} />
            {loading ? 'Processing...' : 'Upload Image'}
          </button>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />

        <div className="tips">
          <h3>📌 Tips for best results:</h3>
          <ul>
            <li>Use clear, well-lit images</li>
            <li>Capture a single item at a time</li>
            <li>Avoid blurry or cluttered backgrounds</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default CaptureScreen;
