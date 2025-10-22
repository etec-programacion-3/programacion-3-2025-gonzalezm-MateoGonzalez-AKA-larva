from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True  # Cambio: era orm_mode en Pydantic V1