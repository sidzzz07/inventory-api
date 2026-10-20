from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory API")


class Item(BaseModel):
    sku: str = Field(min_length=3)
    name: str
    quantity: int = Field(ge=0)
    reorder_level: int = Field(default=5, ge=0)


inventory: dict[str, Item] = {}


@app.post("/items", status_code=201)
def add_item(item: Item) -> Item:
    if item.sku in inventory:
        raise HTTPException(status_code=409, detail=f"SKU {item.sku} already exists")
    inventory[item.sku] = item
    return item


@app.post("/items/{sku}/sell")
def sell_item(sku: str, amount: int) -> Item:
    item = inventory.get(sku)
    if item is None:
        raise HTTPException(status_code=404, detail="Unknown SKU")
    if amount <= 0 or amount > item.quantity:
        raise HTTPException(status_code=400, detail="Invalid sale quantity")
    item.quantity -= amount
    return item


@app.get("/items/low-stock")
def low_stock() -> list[Item]:
    return [item for item in inventory.values() if item.quantity <= item.reorder_level]
    
#reviewed
