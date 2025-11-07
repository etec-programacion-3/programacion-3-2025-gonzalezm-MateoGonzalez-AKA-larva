// src/main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// 🔹 Importar el Router aquí 🔹
import { BrowserRouter } from 'react-router-dom'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* 🔹 El ÚNICO BrowserRouter debe estar aquí 🔹 */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)