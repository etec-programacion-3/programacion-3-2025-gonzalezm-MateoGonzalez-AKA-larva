import React from "react";

// 1. Recibimos 'products', 'onEdit' y 'onDelete'
export default function ProductTable({ products, onEdit, onDelete }) {
  
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
          <th>Acciones</th> {/* 2. Nueva columna */}
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
            <td>
              {/* 3. Botones con sus respectivos handlers */}
              <button onClick={() => onEdit(p)}>Editar</button>
              <button onClick={() => onDelete(p.id)}>Eliminar</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}