import os
import requests
from typing import Optional

from fastapi import FastAPI, HTTPException

def get_invoice_details(invoice_no:str)->dict:
    
    try:
        url = f"http://127.0.0.1:8080/invoices/{invoice_no}"
        headers = {"Content-Type":"application/json"}
        response = requests.get(url,headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "invoice_no":invoice_no,
                "details": data,
                "message" : f"Successfully retrieved details for invoice {invoice_no}"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "invoice_no": invoice_no,
                "message": f"Invoice {invoice_no} not found"
            }
        else:
            return {
                "success": False,
                "invoice_no": invoice_no,
                "message": f"Error retrieving invoice: {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "invoice_no": invoice_no,
            "message": f"Error: {str(e)}"
        }

def get_invoice_status(invoice_no:str)->dict:
    try:
        url = f"http://127.0.0.1:8080/invoices/{invoice_no}/status"
        headers = {"Content-Type":"application/json"}
        response = requests.get(url,headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "invoice_no": invoice_no,
                "status": data.get("status", "unknown"),
                "last_updated": data.get("last_updated", "N/A"),
                "message": f"Status for invoice {invoice_no}: {data.get('status', 'unknown')}"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "invoice_no": invoice_no,
                "message": f"Invoice {invoice_no} not found"
            }
        else:
            return {
                "success": False,
                "invoice_no": invoice_no,
                "message": f"Error retrieving status: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "invoice_no": invoice_no,
            "message": f"Error: {str(e)}"
        }

def download_invoice_pdf(invoice_no:str, save_path: Optional[str] = None)->dict:
    try:
        if save_path is None:
            save_path = f"./invoices/{invoice_no}.pdf"
        
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else "./invoices", exist_ok=True)

        url=f"http://127.0.0.1:8080/invoices/{invoice_no}/pdf"
        headers = {"Content-Type":"application/json"}
        response = requests.get(url,headers=headers, timeout=10)

        if response.status_code == 200:
            with open(save_path,'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                "success": True,
                "invoice_no": invoice_no,
                "file_path": save_path,
                "message": f"Successfully downloaded invoice {invoice_no} to {save_path}"                
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "invoice_no": invoice_no,
                "message": f"Invoice PDF for {invoice_no} not found"
            }
        else:
            return {
                "success": False,
                "invoice_no": invoice_no,
                "message": f"Error downloading PDF: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "invoice_no": invoice_no,
            "message": f"Error: {str(e)}"
        }       



