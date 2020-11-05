import uvicorn
from fastapi import FastAPI, Query, Body
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
from PIL import Image

app = FastAPI(title='Testserver FS', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class B64Image(BaseModel):
    img: str = Query(..., description='The image as a base64 string')


@app.get('/test')
async def test():
    return 'Das hat schon mal funktioniert'

@app.post('/image')
async def embed(data: B64Image):

    if not isinstance(data.img, str):
        return 'Das Bild ist kein String'

    if not data.img.startswith('data:image/'):
        return 'Das Bild ist kein valider B64 string. Es müsste mit data:image/ beginnen, aber geginnt mit ' + data.img[:11]
    
    try:
        b64_body = data.img.split(',')[1]
        decoded = base64.b64decode(b64_body)
        raw = io.BytesIO(decoded)
    except:
        return 'Beim dekodieren des B64 Strings ist etwas schief gelaufen'

    try: 
        img = Image.open(raw).convert('RGB')
    except:
        return 'Der B64 String konnte nicht in ein Bild umkonvertiert werden'

    return 'Ein Bild mit der Breite ' + str(img.size[0]) + ' konnte erfolgreich eingelesen werden'

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, log_level="info")