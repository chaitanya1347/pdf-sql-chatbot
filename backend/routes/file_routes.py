from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.s3_service import upload_files
from services.llm_sql_service import upload_sql_file

router = APIRouter()

@router.post("/uploadFiles")
async def upload_file(file: UploadFile = File(...), fileType: str = Form(...)):
    try:
        if fileType == "pdf":
            upload_files(file)
            return {"info": f"PDF file '{file.filename}' uploaded successfully."}
        
        elif fileType == "sql":
            result = await upload_sql_file(file)
            return {"info": f"SQL file '{file.filename}' uploaded and processed successfully.", "result": result}
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a 'pdf' or 'sql' file.")
    
    except Exception as e:
        # Handle unexpected exceptions and log them
        print(f"An error occurred while uploading the file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

