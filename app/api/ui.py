# app/api/ui.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["UI"])

@router.get("/", response_class=HTMLResponse)
async def home():
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Berlin Weather Forecast 🌤️</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * { 
      box-sizing: border-box; 
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      color: #e4e4e7;
      min-height: 100vh;
      padding: 40px 20px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .container {
      max-width: 800px;
      width: 100%;
    }
    
    .header {
      text-align: center;
      margin-bottom: 40px;
    }
    
    .header h1 {
      font-size: 48px;
      font-weight: 700;
      color: #60a5fa;
      margin-bottom: 12px;
      text-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
      animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
      0%, 100% { text-shadow: 0 0 20px rgba(96, 165, 250, 0.3); }
      50% { text-shadow: 0 0 30px rgba(96, 165, 250, 0.6); }
    }
    
    .header .subtitle {
      font-size: 18px;
      color: #94a3b8;
      font-weight: 400;
    }
    
    .controls {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      margin-bottom: 30px;
    }
    
    .btn {
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      color: white;
      border: none;
      padding: 16px 40px;
      font-size: 18px;
      font-weight: 600;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
      font-family: 'Poppins', sans-serif;
      position: relative;
      overflow: hidden;
    }
    
    .btn::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      width: 0;
      height: 0;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.3);
      transform: translate(-50%, -50%);
      transition: width 0.6s, height 0.6s;
    }
    
    .btn:hover:not(:disabled)::before {
      width: 300px;
      height: 300px;
    }
    
    .btn:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }
    
    .btn:active:not(:disabled) {
      transform: translateY(0);
    }
    
    .btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      background: #64748b;
    }
    
    .status {
      color: #94a3b8;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 120px;
    }
    
    /* Spinner */
    .spinner {
      width: 20px;
      height: 20px;
      border: 3px solid rgba(148, 163, 184, 0.3);
      border-top-color: #60a5fa;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      display: none;
    }
    
    .spinner.active {
      display: inline-block;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    /* Card */
    .card {
      background: rgba(30, 41, 59, 0.8);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 20px;
      padding: 40px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
      min-height: 250px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }
    
    .card:hover {
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.5);
      transform: translateY(-2px);
    }
    
    .forecast {
      font-size: 20px;
      line-height: 1.9;
      color: #e4e4e7;
      text-align: left;
      width: 100%;
    }
    
    .forecast.empty {
      text-align: center;
      color: #64748b;
      font-style: italic;
      font-size: 18px;
    }
    
    .forecast.error {
      color: #ef4444;
      text-align: center;
    }
    
    /* Fade-in animation */
    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(15px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    .fade-in {
      animation: fadeIn 0.6s ease-out;
    }
    
    /* Success state */
    .status.success {
      color: #10b981;
    }
    
    .status.error {
      color: #ef4444;
    }
    
    /* Footer */
    .footer {
      text-align: center;
      margin-top: 30px;
      color: #64748b;
      font-size: 14px;
    }
    
    .footer a {
      color: #60a5fa;
      text-decoration: none;
      transition: color 0.2s;
    }
    
    .footer a:hover {
      color: #93c5fd;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🌤️ Berlin Weather</h1>
      <div class="subtitle">2-Day Forecast</div>
    </div>

    <div class="controls">
      <button id="fetchBtn" class="btn">
        <span id="btnText">Get Forecast</span>
      </button>
      <div class="status" id="status">
        <span id="statusText">Ready</span>
        <div id="spinner" class="spinner"></div>
      </div>
    </div>

    <div class="card">
      <div id="forecast" class="forecast empty">
        👆 Click "Get Forecast" to load Berlin's weather
      </div>
    </div>

    <div class="footer">
      Data from <a href="https://open-meteo.com" target="_blank">Open-Meteo</a>
    </div>
  </div>

  <script>
    const fetchBtn = document.getElementById('fetchBtn');
    const btnText = document.getElementById('btnText');
    const statusEl = document.getElementById('status');
    const statusText = document.getElementById('statusText');
    const spinner = document.getElementById('spinner');
    const forecastDiv = document.getElementById('forecast');

    async function loadForecast() {
      try {
        // Change status to loading in UI
        fetchBtn.disabled = true;
        btnText.textContent = 'Loading...';
        statusText.textContent = 'Fetching data...';
        statusEl.classList.remove('success', 'error');
        spinner.classList.add('active');
        
        forecastDiv.textContent = '';
        forecastDiv.classList.add('empty');
        forecastDiv.classList.remove('error', 'fade-in');

        
        const response = await fetch('/nl-forecast', { 
          cache: 'no-store',
          headers: {
            'Accept': 'text/plain'
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const text = await response.text();

        // Successful - show data
        forecastDiv.textContent = text;
        forecastDiv.classList.remove('empty');
        forecastDiv.classList.add('fade-in');
        
        statusText.textContent = 'Success!';
        statusEl.classList.add('success');
        btnText.textContent = 'Refresh';

      } catch (error) {
        console.error('Error loading forecast:', error);
        
        forecastDiv.textContent = ` Failed to load forecast\n\n${error.message}`;
        forecastDiv.classList.remove('empty');
        forecastDiv.classList.add('error');
        
        statusText.textContent = 'Error';
        statusEl.classList.add('error');
        btnText.textContent = 'Retry';
        
      } finally {
        // Turn off the loading state
        fetchBtn.disabled = false;
        spinner.classList.remove('active');
      }
    }

    //Fetch data when button clicked
    fetchBtn.addEventListener('click', loadForecast);

    // Delete this line if not want to load automatically
    // window.addEventListener('load', loadForecast);
  </script>
</body>
</html>
"""