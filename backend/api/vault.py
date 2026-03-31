from fastapi import APIRouter
from backend.services.vault_manager import VaultManager

router = APIRouter()
vault_service = VaultManager()


@router.post("/store")
def store_item(item_id: str, content: str):
    return vault_service.store_item(item_id, content)


@router.get("/retrieve/{item_id}")
def retrieve_item(item_id: str):
    return vault_service.retrieve_item(item_id)
