import React, { useState, useEffect } from "react";
import ProductTable from "./ProductTable";
import ProductForm from "./ProductForm";
import StockMovementForm from "./StockMovementForm"; // 1. Importar el nuevo componente

const API_URL = "http://127.0.0.1:8000/api/products";

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentProduct, setCurrentProduct] = useState(null);

  const fetchProducts = () => {
    setLoading(true);
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error al obtener productos:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleProductFormSubmit = () => {
    fetchProducts(); // Refresca la tabla tras Crear/Editar
    setCurrentProduct(null);
  };

  const handleEdit = (product) => {
    setCurrentProduct(product);
  };

  const handleDelete = async (productId) => {
    if (window.confirm("¿Seguro que quieres eliminar este producto?")) {
      try {
        await fetch(`${API_URL}/${productId}`, { method: "DELETE" });
        fetchProducts(); // Refresca la tabla tras Eliminar
      } catch (err) {
        console.error("Error al eliminar producto:", err);
      }
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      
      {/* 2. Renderizar el nuevo formulario */}
      <StockMovementForm 
        products={products}
        onMovementSubmit={fetchProducts} // 3. Le pasamos los productos y la función de refresco
      />

      <hr />

      {/* Formulario de Crear/Editar Producto */}
      <h2>{currentProduct ? "Editar Producto" : "Nuevo Producto"}</h2>
      <ProductForm 
        product={currentProduct} 
        onSubmit={handleProductFormSubmit} 
      />
      
      <hr />

      {/* Tabla de Productos */}
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

export default App;