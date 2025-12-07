from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json
from pathlib import Path

app = FastAPI(title="Invoice Lookup Service")

# -----------------------
# Load JSON On Startup
# -----------------------
INVOICE_DATA = {}

#@app.on_event("startup")
def load_invoice_data():
    global INVOICE_DATA
    json_path = Path("test_invoice_data.json")  # uploaded file path

    if not json_path.exists():
        raise FileNotFoundError("Invoice data JSON not found")

    with open(json_path, "r") as f:
        data = json.load(f)

    # Convert list → dict for O(1) lookup
    INVOICE_DATA = {inv["invoice_no"]: inv for inv in data["invoices"]}

    print(f"Loaded {len(INVOICE_DATA)} invoices into memory.")


# -----------------------
# 1. Get Invoice Details
# -----------------------
@app.get("/invoices/{invoice_no}")
def get_invoice_details(invoice_no: str):
    invoice = INVOICE_DATA.get(invoice_no)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


# -----------------------
# 2. Get Invoice Status
# -----------------------
@app.get("/invoices/{invoice_no}/status")
def get_invoice_status(invoice_no: str):
    invoice = INVOICE_DATA.get(invoice_no)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        "invoice_no": invoice_no,
        "status": invoice["status"]
    }


@app.get("/invoices/{invoice_no}/pdf")
def download_invoice_pdf(invoice_no: str):
    file_path = f"./invoicepdf/{invoice_no}.pdf"
    
    # Check if file exists
    # if not file_path.exists():
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"Invoice PDF for invoice {invoice_no} not found"
    #     )
    
    # Return the file
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{invoice_no}.pdf",
        headers={
            "Content-Disposition": f"attachment; filename={invoice_no}.pdf"
        }
    )

# -----------------------
# Health Check Endpoint
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}
