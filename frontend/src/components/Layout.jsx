import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirige al login después de cerrar sesión
  };

  return (
    <div className="layout">
      {/* 1. Un header simple que estará en todas las páginas protegidas */}
      <header style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        padding: '10px 20px', 
        backgroundColor: '#333', 
        color: 'white' 
      }}>
        <h2>Gestión de Stock</h2>
        <button onClick={handleLogout}>Cerrar Sesión</button>
      </header>

      {/* 2. El contenido de la página (ej. Productos.jsx) se renderizará aquí */}
      <main style={{ padding: '20px' }}>
        <Outlet />
      </main>
      
    </div>
  );
}