from fastapi import UploadFile
from PIL import Image
import io
import os
import PyPDF2

class FileProcessor:
    """Process uploaded files for Gemini consumption."""
    
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.pdf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    async def process_upload(file: UploadFile):
        """
        Process uploaded file.
        
        Steps:
        1. Validate file type and size
        2. For images: compress if needed
        3. For PDFs: extract text or convert to images
        4. Return bytes ready for Gemini
        """
        
        # Validate
        filename = file.filename or ""
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in FileProcessor.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        content = await file.read()
        if len(content) > FileProcessor.MAX_FILE_SIZE:
            raise ValueError("File too large (max 10MB)")
        
        # Process based on type
        if file_ext == '.pdf':
            return FileProcessor._process_pdf(content)
        else:
            return FileProcessor._process_image(content)
    
    @staticmethod
    def _process_image(image_bytes: bytes):
        """Compress/optimize image if needed."""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # Resize if too large (Gemini limit: 20MB, keeping it smaller for latency)
            max_dimension = 2048
            if max(img.size) > max_dimension:
                img.thumbnail((max_dimension, max_dimension))
            
            # Convert to RGB if needed
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Save optimized version
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            return {"mime_type": "image/jpeg", "data": output.getvalue()}
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")
    
    @staticmethod
    def _process_pdf(pdf_bytes: bytes):
        """
        Extract text from PDF (Simplest approach for now).
        If needed, we can convert pages to images, but text is cheaper/faster if accessible.
        Gemini 2.0 Flash is multimodal, but passing text extracted from PDF is often easier unless it's image-heavy.
        However, for "document uploads (screenshots...)" often implies visual.
        But for PDF, let's stick to text extraction for now or return the bytes if Gemini supports PDF bytes directly (it does via File API, but here we are sending parts inline).
        Inline PDF support in Gemini 2.0 Flash? It supports it via `parts`.
        Let's try to send as PDF part if possible, otherwise text.
        
        Actually, Gemini API `Pro` supports PDF, let's assume `Flash` does too or we fallback to text_extraction.
        Let's use text extraction for safety and token efficiency unless user requested visuals.
        """
        try:
             # Try text extraction first
             reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
             text = ""
             for page in reader.pages:
                 text += page.extract_text() + "\n"
             
             if not text.strip():
                 # TODO: If no text, might be scanned PDF. Handle that later.
                 raise ValueError("Could not extract text from PDF (Scanned PDFs not fully supported yet)")
            
             return {"mime_type": "text/plain", "data": text.encode('utf-8')} # Gemini treats text as... text.
             # Wait, if we return bytes, the caller expects something. 
             # In `gemini_service`, we append `file_data`.
             # If it's text, we should probably just append it as a string part?
             # Let's make `gemini_service` handle it. 
             # Or better: return the text directly.
             
        except Exception as e:
             raise ValueError(f"Error processing PDF: {str(e)}")

        # Refinement for gemini_service compatibility:
        # If we return a dict with mime_type, gemini_service needs to handle it.
        # For image: mime_type: image/jpeg.
        # For text: mime_type: text/plain.
