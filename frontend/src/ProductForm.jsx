import React, { useState, useEffect } from "react";

export default function ProductForm({ product, onSubmit }) {
  const [nombre, setNombre] = useState("");
  const [sku, setSku] = useState("");
  const [precioCompra, setPrecioCompra] = useState("");
  const [precioVenta, setPrecioVenta] = useState("");
  const [stockActual, setStockActual] = useState("");

  useEffect(() => {
    if (product) {
      setNombre(product.nombre);
      setSku(product.sku);
      setPrecioCompra(product.precio_compra);
      setPrecioVenta(product.precio_venta);
      setStockActual(product.stock_actual);
    }
  }, [product]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nombre || !sku || !precioCompra || !precioVenta) {
      alert("Todos los campos son obligatorios.");
      return;
    }

    const url = product
      ? `http://127.0.0.1:8000/api/products/${product.id}`
      : "http://127.0.0.1:8000/api/products";
    const method = product ? "PUT" : "POST";

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre,
        sku,
        precio_compra: parseFloat(precioCompra),
        precio_venta: parseFloat(precioVenta),
        stock_actual: parseInt(stockActual),
      }),
    });

    setNombre("");
    setSku("");
    setPrecioCompra("");
    setPrecioVenta("");
    setStockActual("");

    onSubmit(); // 🔹 refresca tabla en App.jsx
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <input placeholder="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />
      <input placeholder="SKU" value={sku} onChange={(e) => setSku(e.target.value)} />
      <input placeholder="Precio Compra" type="number" value={precioCompra} onChange={(e) => setPrecioCompra(e.target.value)} />
      <input placeholder="Precio Venta" type="number" value={precioVenta} onChange={(e) => setPrecioVenta(e.target.value)} />
      <input placeholder="Stock Actual" type="number" value={stockActual} onChange={(e) => setStockActual(e.target.value)} />
      <button type="submit">{product ? "Actualizar" : "Crear"}</button>
    </form>
  );
}
