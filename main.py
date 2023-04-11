from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import rarfile
import aiofiles
from pathlib import Path

app = FastAPI()


def extract_rar_file(rar_file: object, output_path: str):
    try:
        with rarfile.RarFile(rar_file) as rf:
            rf.extractall(output_path)
        return True
    except Exception as e:
        print(e)
        return False


@app.post("/api/extract")
async def extract_rar(file: UploadFile = File(...)):
    async with aiofiles.open(file.filename, "wb") as f:
        content = await file.read()
        await f.write(content)

        path = Path(file.filename)

        if path.suffix == ".rar":
            if extract_rar_file(file.filename, "temp"):

                extracted_files = []

                for file in Path("temp").iterdir():
                    extracted_files.append({"name": file.name, "link": f"/files/{file.name}"})

                return {"success": True, "message": "Done extracting rar file", "files": extracted_files}
            else:
                return {"message": "Error extracting rar file"}


@app.get("/files/{file_name}")
async def get_file(file_name: str):
    return FileResponse(f"temp/{file_name}")
