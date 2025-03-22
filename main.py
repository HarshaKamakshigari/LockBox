from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware (Allows frontend to communicate with FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# AES Encryption Config (WEAK for Testing, Change in Production)
AES_KEY = b"1234567890abcdef"  # 16-byte key for AES-128
IV = b"0000000000000000"       # 16-byte IV (Initialization Vector)

# Upload folder setup
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🚀 Encrypt File API
@app.post("/encrypt")
async def encrypt_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file uploaded."}

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        # Read and encrypt file
        file_content = await file.read()
        cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
        encrypted_data = cipher.encrypt(pad(file_content, AES.block_size))

        # Save encrypted file
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as f:
            f.write(encrypted_data)

        return {"message": "File encrypted", "filename": file.filename + ".enc"}

    except Exception as e:
        return {"error": str(e)}

# 🔓 Decrypt File API
@app.get("/decrypt")
async def decrypt_file(filename: str = Query(...)):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found."}

    try:
        # Read encrypted data
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        # Decrypt file
        cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # Save decrypted file
        decrypted_file_path = file_path.replace(".enc", ".dec")
        with open(decrypted_file_path, "wb") as f:
            f.write(decrypted_data)

        return FileResponse(decrypted_file_path, filename=filename.replace(".enc", ".dec"))

    except Exception as e:
        return {"error": str(e)}

# Run FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
