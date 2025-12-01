from models import Contract
from database import SessionLocal

def create_contract(title, content):
    db = SessionLocal()
    contract = Contract(title=title, content=content)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

def get_contracts():
    db = SessionLocal()
    contracts = db.query(Contract).all()
    return contracts