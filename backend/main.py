
import io
import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from diffusers import StableDiffusionXLInstantIDPipeline, T2IAdapter
from diffusers.utils import load_image
import torch
from PIL import Image

# --- 초기 설정 ---
app = FastAPI()

# 생성된 이미지를 저장하고 접근할 디렉토리 생성
output_dir = "generated_images"
os.makedirs(output_dir, exist_ok=True)
app.mount(f"/{output_dir}", StaticFiles(directory=output_dir), name="generated_images")

# --- 모델 로딩 ---
# CUDA 사용 가능 여부 확인
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# InstantID 파이프라인 로드
# 참고: 최초 실행 시 모델 다운로드로 인해 시간이 오래 걸릴 수 있습니다.
try:
    adapter = T2IAdapter.from_pretrained(
        "InstantX/sdxl-adapter-t2i-style-cartoon", 
        torch_dtype=torch.float16
    ).to(device)
    
    pipe = StableDiffusionXLInstantIDPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        t2i_adapter=adapter,
        torch_dtype=torch.float16,
    ).to(device)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    pipe = None

# --- API 엔드포인트 ---
@app.post("/generate-cartoon/")
async def generate_cartoon(file: UploadFile = File(...)):
    if not pipe:
        return JSONResponse(status_code=500, content={"message": "Model is not available."})

    try:
        # 업로드된 이미지 처리
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # InstantID는 특정 크기의 얼굴 이미지를 요구할 수 있습니다.
        # 여기서는 간단히 리사이즈합니다.
        face_image = input_image.resize((224, 224))

        # 동화풍 생성을 위한 프롬프트
        prompt = "a cartoon-style drawing, anime, disney, pixar, chibi"
        
        # 이미지 생성 (4장)
        images = pipe(
            prompt=prompt,
            image=face_image,
            num_images_per_prompt=4,
            num_inference_steps=30,
            guidance_scale=7.5,
        ).images

        # 생성된 이미지 저장 및 URL 생성
        image_urls = []
        for i, img in enumerate(images):
            filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath)
            # http://localhost:8000/generated_images/filename.jpg 형식의 URL
            image_urls.append(f"/{output_dir}/{filename}")

        return JSONResponse(content={"image_urls": image_urls})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})

# 서버 루트 경로
@app.get("/")
def read_root():
    return {"message": "FastAPI server for Cartoon Generation is running."}
