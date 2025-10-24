from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# Asegúrate de que schemas.py tenga Producto, ProductoCreate y ProductoUpdate
# (Lo corregimos en el paso anterior)
from .. import models, schemas, database

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

# ----------------------------------------------
# GET / (Listar) - AHORA CON FILTROS Y PAGINACIÓN
# ----------------------------------------------
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
# POST / (Crear) - (Ya lo tenías)
# ----------------------------------------------
@router.post("/", response_model=schemas.Producto, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    # Opcional: Verificar si el SKU ya existe
    db_product_sku = db.query(models.Producto).filter(models.Producto.sku == product.sku).first()
    if db_product_sku:
        raise HTTPException(status_code=400, detail="SKU ya registrado")

    db_product = models.Producto(**product.model_dump()) # Pydantic v2 usa .model_dump()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------------------------------------
# GET /{id} (Leer uno) - (AÑADIDO)
# ----------------------------------------------
@router.get("/{product_id}", response_model=schemas.Producto)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

# ----------------------------------------------
# PUT /{id} (Actualizar) - (AÑADIDO)
# ----------------------------------------------
@router.put("/{product_id}", response_model=schemas.Producto)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Actualizar solo los campos enviados (actualización parcial)
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------------------------------------
# DELETE /{id} (Eliminar) - (AÑADIDO)
# ----------------------------------------------
@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_product)
    db.commit()
    # 204 No Content no debe devolver cuerpo
    return