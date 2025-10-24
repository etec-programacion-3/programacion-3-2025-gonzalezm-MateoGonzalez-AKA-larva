import React, { useState } from "react";

// URL del endpoint que creamos en el backend (main.py)
const MOVEMENT_API_URL = "http://127.0.0.1:8000/api/stock/movements";

export default function StockMovementForm({ products, onMovementSubmit }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [cantidad, setCantidad] = useState(1);
  const [tipo, setTipo] = useState("entrada");
  
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Criterio 1: Buscar producto por nombre o SKU (en la lista local)
  const handleSearch = (e) => {
    e.preventDefault();
    setError("");
    if (!searchTerm) {
      setSelectedProduct(null);
      return;
    }

    // Buscamos en la lista de productos que nos pasó App.jsx
    const found = products.find(
      (p) =>
        p.sku.toLowerCase() === searchTerm.toLowerCase() ||
        p.nombre.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (found) {
      setSelectedProduct(found);
    } else {
      setError("Producto no encontrado.");
      setSelectedProduct(null);
    }
  };

  // Criterio 2 y 3: Enviar el movimiento al API
  const handleSubmitMovement = async (e) => {
    e.preventDefault();
    if (!selectedProduct) return;

    setSubmitting(true);
    setError("");

    try {
      const res = await fetch(MOVEMENT_API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          producto_id: selectedProduct.id,
          cantidad: parseInt(cantidad),
          tipo: tipo,
        }),
      });

      if (!res.ok) {
        // Si el backend da error (ej. "Stock insuficiente"), lo mostramos
        const errData = await res.json();
        throw new Error(errData.detail || "Error al registrar movimiento");
      }

      // Criterio 4: Actualizar la tabla
      // Llamamos a la función que nos pasó App.jsx (que es fetchProducts)
      onMovementSubmit();

      // Limpiar formulario
      setSelectedProduct(null);
      setSearchTerm("");
      setCantidad(1);
      setTipo("entrada");

    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ padding: "10px", border: "1px solid #444", borderRadius: "8px", marginBottom: "20px" }}>
      <h3>Registrar Movimiento de Stock</h3>
      
      {/* Formulario de Búsqueda */}
      <form onSubmit={handleSearch} style={{ marginBottom: "10px" }}>
        <input
          type="text"
          placeholder="Buscar por Nombre o SKU"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Buscar</button>
      </form>

      {/* Mensaje de error (si existe) */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Criterio 2: Formulario de Movimiento (si hay producto) */}
      {selectedProduct && (
        <form
          onSubmit={handleSubmitMovement}
          style={{ borderTop: "1px dashed #555", paddingTop: "10px" }}
        >
          <h4>
            Producto: {selectedProduct.nombre} (Stock actual:{" "}
            {selectedProduct.stock_actual})
          </h4>
          <input
            type="number"
            value={cantidad}
            onChange={(e) => setCantidad(Math.max(1, parseInt(e.target.value)))}
            min="1"
          />
          <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
            <option value="entrada">Entrada</option>
            <option value="salida">Salida</option>
          </select>
          <button type="submit" disabled={submitting}>
            {submitting ? "Registrando..." : "Registrar Movimiento"}
          </button>
        </form>
      )}
    </div>
  );
}