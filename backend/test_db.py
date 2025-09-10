from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Proveedor, Producto, MovimientoDeStock, TipoMovimiento

# Conectar a la base de datos
engine = create_engine("sqlite:///backend/stock.db")
Session = sessionmaker(bind=engine)
session = Session()

# 1. Crear un proveedor
proveedor = Proveedor(nombre="Proveedor Ejemplo", contacto="contacto@ejemplo.com")
session.add(proveedor)
session.commit()

# 2. Crear un producto asociado al proveedor
producto = Producto(
    sku="SKU001",
    nombre="Producto Ejemplo",
    descripcion="Descripción de prueba",
    precio_compra=10.0,
    precio_venta=15.0,
    stock_actual=100,
    proveedor=proveedor
)
session.add(producto)
session.commit()

# 3. Crear un movimiento de stock asociado al producto
movimiento = MovimientoDeStock(
    tipo=TipoMovimiento.entrada,
    cantidad=50,
    producto=producto
)
session.add(movimiento)
session.commit()

# 4. Consultar y mostrar los datos
productos = session.query(Producto).all()
for p in productos:
    print(f"Producto: {p.nombre}, Proveedor: {p.proveedor.nombre}, Stock: {p.stock_actual}")
    for m in p.movimientos:
        print(f"  Movimiento: {m.tipo.value}, Cantidad: {m.cantidad}, Fecha: {m.fecha}")

session.close()
