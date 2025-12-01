from fastapi import FastAPI, HTTPException
from service import create_contract, get_contracts
from utils.file_parser import parse_pdf, parse_docx

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: bytes = File(...), file_type: str = Form(...)):
    if file_type == "pdf":
        content = parse_pdf(file)
    elif file_type == "docx":
        content = parse_docx(file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    contract = create_contract(title=file.filename, content=content)
    return {"id": contract.id, "title": contract.title}

@app.get("/contracts/")
async def get_all_contracts():
    contracts = get_contracts()
    return [{"id": contract.id, "title": contract.title} for contract in contracts]