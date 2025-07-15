import React, { useState } from 'react';
import './App.css';
import Aurora from './Aurora';
import logo from './logo.png';
import RotatingText from './RotatingText'; 

function App() {
  const [showGenerator, setShowGenerator] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [inputMode, setInputMode] = useState('text');
  const [mood, setMood] = useState('');
  const [moodLifting, setMoodLifting] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = () => {
    if (!mood.trim()) {
      setError('Please enter a mood before generating.');
      return;
    }
    setError('');
    // trigger image generation logic
  };

  if (showAbout) {
    return (
      <div className="landing-page">
        <Aurora />
        <nav className="landing-nav">
          <div className="logo-container" onClick={() => setShowAbout(false)}>
            <img src={logo} alt="Logo" className="logo" />
            <span className="app-title">AI Moodboard Generator</span>
          </div>
          <button className="back-btn" onClick={() => setShowAbout(false)}>
            ← Back to Home
          </button>
        </nav>
        <div className="about-section">
          <h1>Our Vision</h1>
          <div className="about-content">
            <p>In a world where emotions are complex and often hard to express, we saw the need for a bridge between feelings and visual representation. Traditional design tools can be intimidating, leaving many without an outlet for emotional creativity.</p>
            
            <p>Our AI-powered platform transforms your mood—whether described in words or captured through expression—into beautiful, meaningful visual collections. We're not just creating images; we're crafting emotional mirrors that help you see and understand your inner state.</p>
            
            <p>Whether you're journaling, seeking self-awareness, exploring creatively, or simply wanting to visualize how you feel, our technology adapts to your emotional needs. The result is a personalized visual experience that's as unique as your mood in that moment.</p>
          </div>
          <button className="cta-btn" onClick={() => setShowAbout(false)}>
            Back to Home
          </button>
        </div>
      </div>
    );
  }

if (!showGenerator) {
  return (
    <div className="landing-page">
      <Aurora />
      <nav className="landing-nav">
        <div className="logo-container" onClick={() => setShowGenerator(false)}>
          <img src={logo} alt="Logo" className="logo" />
          <span className="app-title">AI Moodboard Generator</span>
        </div>
        <button className="about-btn" onClick={() => setShowAbout(true)}>
          About Us
        </button>
      </nav>

      <div className="hero-section">
        <h1 className="hero-title">
          Visualize Your&nbsp;
          <RotatingText
            texts={["Mood", "Emotion", "Vibe", "Style", "Aesthetic"]}
            mainClassName="rotating-text"
            splitLevelClassName="overflow-hidden"
            staggerFrom="last"
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "-120%" }}
            staggerDuration={0.025}
            transition={{ type: "spring", damping: 30, stiffness: 400 }}
            rotationInterval={2000}
          />
        </h1>

        <h2>Create Meaningful Moodboards Instantly</h2>
        <p>
          Transform fleeting feelings into lasting visual expressions with our intuitive AI generator. 
          Perfect for creatives, journalers, and anyone exploring their emotional landscape.
        </p>

        <button className="cta-btn" onClick={() => setShowGenerator(true)}>
          Start Creating →
        </button>
      </div>
    </div>
  );
}

  return (
    <div className="app">
      <Aurora />
      <div className="navbar">
        <div className="logo-container" onClick={() => setShowGenerator(false)}>
          <img src={logo} alt="Logo" className="logo" />
          <span className="app-title">AI Moodboard Generator</span>
        </div>
        <button className="back-btn" onClick={() => setShowGenerator(false)}>
          ← Back to Home
        </button>
      </div>

      <div className="generator-container">
        <div className="generator-card">
          <h2 className="generator-title">Create Your Moodboard</h2>
          <p className="generator-subtitle">How are you feeling today?</p>
          
          <div className="mode-toggle">
            <label className={`mode-option ${inputMode === 'text' ? 'active' : ''}`}>
              <input
                type="radio"
                value="text"
                checked={inputMode === 'text'}
                onChange={() => setInputMode('text')}
              />
              <span>Describe Your Mood</span>
            </label>
            <label className={`mode-option ${inputMode === 'camera' ? 'active' : ''}`}>
              <input
                type="radio"
                value="camera"
                checked={inputMode === 'camera'}
                onChange={() => setInputMode('camera')}
              />
              <span>Capture Your Mood</span>
            </label>
          </div>

          {inputMode === 'text' && (
            <div className="input-group">
              <input
                className="text-input"
                type="text"
                placeholder="Try: 'happy', 'romantic', 'calm'..."
                value={mood}
                onChange={(e) => {
                  setMood(e.target.value);
                  setError('');
                }}
              />
              {error && <div className="error-message">{error}</div>}
            </div>
          )}

          <div className="mood-lift-group">
            <label className="mood-lift-toggle">
              <input
                type="checkbox"
                checked={moodLifting}
                onChange={() => setMoodLifting(!moodLifting)}
              />
              <span>Need a mood boost? We'll add uplifting elements</span>
            </label>
          </div>

          <button className="generate-btn" onClick={handleGenerate}>
            ✨ Generate Moodboard
          </button>
        </div>

        <div className="results-section">
          <div className="results-card">
            <h3>🖼️ Your Moodboard</h3>
            <div className="image-grid">
              <div className="image-placeholder"></div>
              <div className="image-placeholder"></div>
              <div className="image-placeholder"></div>
              <div className="image-placeholder"></div>
            </div>
          </div>
          
          <div className="results-card">
            <h3>🎨 Color Palette</h3>
            <div className="color-palette">
              <div className="color-swatch" style={{backgroundColor: '#9259f2'}}></div>
              <div className="color-swatch" style={{backgroundColor: '#ff7eb9'}}></div>
              <div className="color-swatch" style={{backgroundColor: '#7afcff'}}></div>
              <div className="color-swatch" style={{backgroundColor: '#fff740'}}></div>
              <div className="color-swatch" style={{backgroundColor: '#fe6e00'}}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;