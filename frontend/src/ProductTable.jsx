import React, { useEffect, useState } from "react";

export default function ProductTable() {
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
        console.error(err);
        setLoading(false);
      });
  }, []);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/products")
        .then((res) => res.json())
        .then((data) => setProducts(data))
        .catch((err) => console.error(err));
}, []);


  if (loading) return <p>Cargando productos...</p>;

  if (!products.length) return <p>No hay productos para mostrar.</p>;

  return (
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>SKU</th>
          <th>Precio Compra</th>
          <th>Precio Venta</th>
          <th>Stock</th>
        </tr>
      </thead>
      <tbody>
        {products.map((p) => (
          <tr key={p.id}>
            <td>{p.id}</td>
            <td>{p.nombre}</td>
            <td>{p.sku}</td>
            <td>{p.precio_compra}</td>
            <td>{p.precio_venta}</td>
            <td>{p.stock_actual}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
