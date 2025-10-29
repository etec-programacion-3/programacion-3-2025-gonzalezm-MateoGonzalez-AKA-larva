// frontend/src/pages/DashboardPage.jsx
import React, { useState, useEffect, useCallback } from "react";
import ProductTable from "../components/ProductTable"; // Ajusta la ruta
import ProductForm from "../components/ProductForm"; // Ajusta la ruta
import StockMovementForm from "../components/StockMovementForm"; // Ajusta la ruta
import { useAuth } from "../context/AuthContext"; // Importamos el auth

const API_URL = "http://127.0.0.1:8000/api/products";

// Esta será la lógica de la app principal
export default function DashboardPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentProduct, setCurrentProduct] = useState(null);
  const { token, logout } = useAuth(); // 🔹 Traemos el token y logout

  // Criterio 5: Enviar el token en las cabeceras
  const getHeaders = useCallback(() => {
    return {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    }
  }, [token]);


  const fetchProducts = useCallback(() => {
    setLoading(true);
    fetch(API_URL, { headers: getHeaders() }) // 🔹 Usamos headers
      .then((res) => {
        if (res.status === 401) logout(); // Si el token es inválido, desloguear
        return res.json();
      })
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error al obtener productos:", err);
        setLoading(false);
      });
  }, [getHeaders, logout]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleProductFormSubmit = () => {
    fetchProducts();
    setCurrentProduct(null);
  };

  const handleEdit = (product) => {
    setCurrentProduct(product);
  };

  const handleDelete = async (productId) => {
    if (window.confirm("¿Seguro que quieres eliminar este producto?")) {
      try {
        await fetch(`${API_URL}/${productId}`, { 
            method: "DELETE",
            headers: getHeaders() // 🔹 Usamos headers
        });
        fetchProducts(); 
      } catch (err) {
        console.error("Error al eliminar producto:", err);
      }
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <button onClick={logout} style={{ float: 'right' }}>Cerrar Sesión</button>
      
      <StockMovementForm 
        products={products}
        onMovementSubmit={fetchProducts}
      />
      <hr />
      <h2>{currentProduct ? "Editar Producto" : "Nuevo Producto"}</h2>
      <ProductForm 
        product={currentProduct} 
        onSubmit={handleProductFormSubmit} 
      />
      <hr />
      <h1>Lista de Productos</h1>
      {loading ? (
        <p>Cargando productos...</p>
      ) : (
        <ProductTable 
          products={products} 
          onEdit={handleEdit} 
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}