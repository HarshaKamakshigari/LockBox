from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

app = FastAPI()

AES_KEY = b"1234567890abcdef"  # WEAK AES KEY (For Testing)
IV = b"0000000000000000"       # STATIC IV

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/encrypt")
async def encrypt_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Read and Encrypt File
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(pad(await file.read(), AES.block_size))

    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as f:
        f.write(encrypted_data)

    return {"message": "File encrypted", "filename": file.filename + ".enc"}

@app.get("/decrypt")
async def decrypt_file(filename: str = Query(...)):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    decrypted_file_path = file_path.replace(".enc", ".dec")
    with open(decrypted_file_path, "wb") as f:
        f.write(decrypted_data)

    return FileResponse(decrypted_file_path, filename=filename.replace(".enc", ".dec"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
