FROM python:3.12-slim-bookworm

# 작업 환경 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul

# 런타임에 필요한 시스템 패키지 (tzdata, libpq5 등)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt 복사 및 의존성 설치 (시스템 Python에 직접)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스(app/)와 공용 모듈(shared/ - 필요시) 복사
COPY app/ ./app/
# 만약 admin 서비스도 shared/ 디렉토리를 사용하고, app/ 과 같은 레벨에 있다면:
# COPY shared/ ./shared/ # /app/shared/ 에 복사됨
# ENV PYTHONPATH="/app:${PYTHONPATH}" # shared 사용 시 필요할 수 있음

# Non-root user 설정
RUN useradd --system --create-home appuser && \
    chown -R appuser:appuser /app # /app 디렉토리만 권한 부여 (site-packages는 root 소유 유지해도 무방)
USER appuser

EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]