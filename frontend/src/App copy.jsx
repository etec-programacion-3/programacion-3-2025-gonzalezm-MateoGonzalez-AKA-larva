import React, { useState, useEffect } from "react";
import ProductTable from "./ProductTable";

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/products")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error al obtener productos:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando productos...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Lista de Productos</h1>
      <ProductTable products={products} />
    </div>
  );
}

export default App;

