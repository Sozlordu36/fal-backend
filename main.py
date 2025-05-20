from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/fal")
async def yorumla(image: UploadFile = File(...)):
    try:
        content = await image.read()
        base64_image = base64.b64encode(content).decode("utf-8")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Sen 40 yıllık tecrübeli bir kahve falı bakan kadınsın. 'Bacım' diye hitap edersin ve aşırı abartı düzeyde uzun uzun açıklarsın yani en az 350 kelime ve normal falcılardan daha da spesifik şaşırtıcı ama iyi yorumlar ve çıkarımlar yapıyorsun. Eğer gönderilen görsellerden her hangi biri kahve fincanı değilse şunu yaz: 'Bacım, bu fincan değil. Sadece kahve falı atılır burada 🙏'"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Fal bakar mısın bacım?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=800
        )

        return {"yorum": response.choices[0].message["content"]}

    except Exception as e:
        return {"yorum": f"Bacım bir hata oluştu: {str(e)}"}

