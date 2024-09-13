import duckdb
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.types import HTTPExceptionHandler
from models import Item


# Criando a aplicação fastapi
app = FastAPI()

# Conecte-se ao duckdb (salvando num arquivo local)
conn = duckdb.connect("database.db")

# Criar tabela
conn.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER,
        name VARCHAR,
        description VARCHAR,
        price FLOAT,
        in_stock BOOLEAN
    )
""")

# Endpoint pra criar um Item
@app.post("/items/")
def create_item(item: Item):
    query = """
    INSERT INTO items (id, name, description, price, in_stock) 
    VALUES (?, ?, ?, ?, ?)
    """
    conn.execute(query, (item.id, item.name, item.description, item.price, item.in_stock))
    return {"message": "Item criado com sucesso"}

# Endpoint para buscar um item por ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    query = "SELECT * FROM items WHERE id = ?"
    result = conn.execute(query, (item_id,)).fetchone()

    if result:
        return {
            "id": result[0],
            "name": result[1],
            "description": result[2],
            "price": result[3],
            "in_stock": result[4]
        }
    else:
        raise HTTPException(status_code=404, detail="Item nao encontrado")

# Endpoint para atualizar um item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    query = """
    UPDATE items
    SET name = ?, description = ?, price = ?, in_stock = ?
    WHERE id = ?
    """
    conn.execute(query, (item.name, item.description, item.price, item.in_stock, item_id))
    return {"message": "Item atualizado com sucesso"}

# Endpoint atualizado para deletar um item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    query = "DELETE FROM items WHERE id = ?"
    conn.execute(query, (item_id,))
    return {"message": "Item deletado com sucesso"}

