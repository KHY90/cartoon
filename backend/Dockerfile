# CUDA 지원 PyTorch 최신 안정화 이미지를 기반으로 합니다.
FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

# 작업 디렉토리 설정
WORKDIR /app

# C++ 컴파일러(g++)를 포함한 빌드 도구와 시스템 라이브러리를 설치하고, 캐시를 정리합니다.
RUN apt-get update && apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# pip 업그레이드 및 모든 파이썬 라이브러리를 명시적 버전으로 한 번에 설치합니다.
# requirements.txt를 사용하지 않고 Dockerfile에서 모든 의존성을 관리하여 빌드의 일관성을 보장합니다.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        fastapi==0.111.0 \
        uvicorn==0.29.0 \
        python-multipart==0.0.9 \
        opencv-python-headless==4.9.0.80 \
        insightface==0.7.3 \
        diffusers==0.28.2 \
        transformers==4.41.2 \
        accelerate==0.30.1

# 백엔드 소스 코드 복사
COPY . .

# 8000 포트 노출
EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]