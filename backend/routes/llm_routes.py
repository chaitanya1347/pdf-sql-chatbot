from fastapi import APIRouter, Query, HTTPException
from services.s3_service import list_files
from services.llm_pdf_service import get_pdf_text_from_s3, get_text_chunks, get_vector_store, user_input
from services.llm_sql_service import get_response

router = APIRouter()

@router.get("/get_all_files")
async def get_all_files(fileName: str = Query(..., description="Comma-separated file names to match")):
    try:

        files = list_files(fileName)
        if not files:
            raise HTTPException(status_code=404, detail="No files found in the S3 bucket")
        # Extract text from PDF files
        raw_text = get_pdf_text_from_s3(files)
        
        if not raw_text:
            raise HTTPException(status_code=500, detail="Failed to extract text from PDFs")
        
        # Split text into chunks for processing
        text_chunks = get_text_chunks(raw_text)
        if not text_chunks:
            raise HTTPException(status_code=500, detail="Failed to generate text chunks")
        
        # Store text chunks in a vector store for later retrieval
        get_vector_store(text_chunks)
        
        return {"files": files}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint to get a response to a user query
@router.get("/ask_query")
async def ask_query(question: str = Query(..., description="The question to ask")):
    try:
        # Get a response for the provided user query
        response = user_input(question)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to get a response from the service")
        
        return {"answer": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the query")


# Endpoint to get a response to a SQL query
@router.get("/ask_sql_query")
async def ask_sql_query(question: str = Query(..., description="The SQL query to ask")):
    try:
        # Get a response for the provided SQL query
        response = get_response(question, [])
        if not response:
            raise HTTPException(status_code=500, detail="Failed to get a response for the SQL query")
        
        return {"answer": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the query")
