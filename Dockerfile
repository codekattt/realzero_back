# Python 이미지를 기반으로 한다.
FROM python:3.9-slim

# 작업 디렉토리를 설정한다.
WORKDIR /realzero_back

# requirements.txt 파일을 작업 디렉토리로 복사한다.
COPY requirements.txt .

# 종속성을 설치한다.
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 애플리케이션 파일을 복사한다.
COPY . .

# 환경 변수를 설정한다.
ENV PORT 8080

# 애플리케이션을 실행한다.
# CMD ["python", "zero.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "zero:app"]