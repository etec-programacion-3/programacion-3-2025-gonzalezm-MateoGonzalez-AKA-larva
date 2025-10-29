// frontend/src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();

  if (!token) {
    // Criterio 4: Redirigir al login si no está autenticado
    return <Navigate to="/login" replace />;
  }

  return children;
}