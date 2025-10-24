from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# Importamos los módulos (los nombres de schema deben coincidir)
from .. import models, schemas, database

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

# ----------------------------------------------
# GET / (Listar)
# ----------------------------------------------
# 🔹 CORREGIDO: response_model=List[schemas.Producto] (en Español)
@router.get("/", response_model=List[schemas.Producto])
def get_products(
    db: Session = Depends(database.get_db), 
    nombre: str | None = None,
    skip: int = 0, 
    limit: int = 100
):
    query = db.query(models.Producto)
    
    if nombre:
        query = query.filter(models.Producto.nombre.contains(nombre))
        
    productos = query.offset(skip).limit(limit).all()
    return productos

# ----------------------------------------------
# POST / (Crear)
# ----------------------------------------------
# 🔹 CORREGIDO: response_model=schemas.Producto
# 🔹 CORREGIDO: product: schemas.ProductoCreate (en Español)
@router.post("/", response_model=schemas.Producto, status_code=201)
def create_product(product: schemas.ProductoCreate, db: Session = Depends(database.get_db)):
    db_product_sku = db.query(models.Producto).filter(models.Producto.sku == product.sku).first()
    if db_product_sku:
        raise HTTPException(status_code=400, detail="SKU ya registrado")

    db_product = models.Producto(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------------------------------------
# GET /{id} (Leer uno)
# ----------------------------------------------
# 🔹 CORREGIDO: response_model=schemas.Producto (en Español)
@router.get("/{product_id}", response_model=schemas.Producto)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

# ----------------------------------------------
# PUT /{id} (Actualizar)
# ----------------------------------------------
# 🔹 CORREGIDO: response_model=schemas.Producto
# 🔹 CORREGIDO: product: schemas.ProductoUpdate (en Español)
@router.put("/{product_id}", response_model=schemas.Producto)
def update_product(product_id: int, product: schemas.ProductoUpdate, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------------------------------------
# DELETE /{id} (Eliminar)
# ----------------------------------------------
@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_product)
    db.commit()
    return