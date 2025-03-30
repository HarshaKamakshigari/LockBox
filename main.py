# from fastapi import FastAPI, UploadFile, File, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# import os

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],  
#     allow_headers=["*"], 
# )


# AES_KEY = b"1234567890abcdef"  
# IV = b"0000000000000000"       

# UPLOAD_FOLDER = "uploads/"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.post("/encrypt")
# async def encrypt_file(file: UploadFile = File(...)):
#     if not file:
#         return {"error": "No file uploaded."}

#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     try:
#         file_content = await file.read()
#         cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
#         encrypted_data = cipher.encrypt(pad(file_content, AES.block_size))

#         encrypted_file_path = file_path + ".enc"
#         with open(encrypted_file_path, "wb") as f:
#             f.write(encrypted_data)

#         return {"message": "File encrypted", "filename": file.filename + ".enc"}

#     except Exception as e:
#         return {"error": str(e)}

# @app.get("/decrypt")
# async def decrypt_file(filename: str = Query(...)):
#     file_path = os.path.join(UPLOAD_FOLDER, filename)

#     if not os.path.exists(file_path):
#         return {"error": "File not found."}

#     try:
#         # Read encrypted data
#         with open(file_path, "rb") as f:
#             encrypted_data = f.read()

#         # Decrypt file
#         cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
#         decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

#         # Save decrypted file
#         decrypted_file_path = file_path.replace(".enc", ".dec")
#         with open(decrypted_file_path, "wb") as f:
#             f.write(decrypted_data)

#         return FileResponse(decrypted_file_path, filename=filename.replace(".enc", ".dec"))

#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import io
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Weak AES keys (5 numeric + 5 alphabetic)
AES_KEYS = [
    b"0000000000000000",  # Weak numeric key
    b"1111111111111111",
    b"2222222222222222",
    b"3333333333333333",
    b"4444444444444444",
    b"AAAAAAAAAAAAAAAA",  # Weak alphabetic key
    b"BBBBBBBBBBBBBBBB",
    b"CCCCCCCCCCCCCCCC",
    b"DDDDDDDDDDDDDDDD",
    b"EEEEEEEEEEEEEEEE"
]

IV = b"0000000000000000"  # Static IV (weak)
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/encrypt")
async def encrypt_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file uploaded."}

    try:
        file_content = await file.read()

        key_index = random.randint(0, len(AES_KEYS) - 1)  # Pick a random weak key
        selected_key = AES_KEYS[key_index]

        cipher = AES.new(selected_key, AES.MODE_CBC, IV)
        encrypted_data = cipher.encrypt(pad(file_content, AES.block_size))

        encrypted_filename = f"{file.filename}.enc_{key_index}"  # Store key index in filename
        encrypted_file_path = os.path.join(UPLOAD_FOLDER, encrypted_filename)

        with open(encrypted_file_path, "wb") as f:
            f.write(encrypted_data)

        return {"message": "File encrypted", "filename": encrypted_filename}

    except Exception as e:
        return {"error": str(e)}

@app.post("/decrypt")
async def decrypt_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file uploaded."}

    try:
        # Extract the key index from the filename
        filename = file.filename
        if not filename.endswith(tuple(f".enc_{i}" for i in range(len(AES_KEYS)))):
            return {"error": "Invalid file format. Missing key index."}

        key_index = int(filename.split("_")[-1])  # Extract the stored key index
        selected_key = AES_KEYS[key_index]  # Retrieve the corresponding weak key

        encrypted_data = await file.read()
        cipher = AES.new(selected_key, AES.MODE_CBC, IV)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        decrypted_filename = filename.replace(f".enc_{key_index}", ".dec")

        return StreamingResponse(
            io.BytesIO(decrypted_data),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={decrypted_filename}"}
        )

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
