import React, { useState, useEffect, useCallback } from 'react';

// 1. Importar las funciones de la API (que ya usan el token)
// (Asumiendo que api.js está en src/utils/api.js)
import { getProducts, createProduct, updateProduct, deleteProduct } from '../utils/api'; 

// 2. Importar los componentes visuales
// (Asumiendo que los moviste a src/components/)
import ProductTable from '../components/ProductTable';
import ProductForm from '../components/ProductForm';
// import StockMovementForm from '../components/StockMovementForm'; // Descomenta si también tienes este

export default function Productos() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Estado para saber qué producto estamos editando
  const [currentProduct, setCurrentProduct] = useState(null);

  // Función para cargar productos (usa la API)
  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getProducts(); // Usa getProducts de api.js
      setProducts(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      // Si el error es 401, api.js ya te habrá redirigido al login
    } finally {
      setLoading(false);
    }
  }, []);

  // Carga inicial de productos
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // Handler para el formulario (Crear/Editar)
  const handleFormSubmit = async (productData) => {
    try {
      if (currentProduct) {
        // Actualizar
        await updateProduct(currentProduct.id, productData);
      } else {
        // Crear
        await createProduct(productData);
      }
      fetchProducts(); // Recargar la lista
      setCurrentProduct(null); // Limpiar el formulario
    } catch (err) {
      setError(err.message);
    }
  };
  
  // Handler para el botón 'Editar' de la tabla
  const handleEdit = (product) => {
    setCurrentProduct(product);
  };

  // Handler para 'Eliminar'
  const handleDelete = async (productId) => {
    if (window.confirm("¿Seguro que quieres eliminar este producto?")) {
      try {
        await deleteProduct(productId); // Usa deleteProduct de api.js
        fetchProducts(); // Recargar
      } catch (err) {
        setError(err.message);
      }
    }
  };

  // Renderizado
  if (loading) return <p>Cargando productos...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      {/* <h2>Movimientos de Stock</h2> */}
      {/* <StockMovementForm products={products} onMovementSubmit={fetchProducts} /> */}
      
      <hr />
      
      <h2>{currentProduct ? 'Editar Producto' : 'Nuevo Producto'}</h2>
      <ProductForm 
        product={currentProduct} 
        onSubmit={handleFormSubmit} 
        onCancel={() => setCurrentProduct(null)} // Botón para limpiar/cancelar
      />
      
      <hr />
      
      <h1>Lista de Productos</h1>
      <ProductTable 
        products={products} 
        onEdit={handleEdit} 
        onDelete={handleDelete}
      />
    </div>
  );
}