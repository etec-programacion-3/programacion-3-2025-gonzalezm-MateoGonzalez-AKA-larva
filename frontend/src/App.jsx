// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Importa los nombres de archivo correctos que solucionamos antes
import Login from './pages/LoginPage';
import Register from './pages/RegisterPage';
import Productos from './pages/Productos'; 
import Layout from './components/Layout'; 

// Componente para rutas protegidas
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Rutas públicas */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* Rutas protegidas */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout /> 
        </ProtectedRoute>
      }>
        <Route index element={<Navigate to="/productos" replace />} />
        <Route path="productos" element={<Productos />} />
      </Route>
      
      {/* Ruta por defecto */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    // 🔹 ERROR CORREGIDO 🔹
    // Quitamos el <BrowserRouter> que estaba duplicado aquí.
    // AuthProvider debe ser el contenedor principal.
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;