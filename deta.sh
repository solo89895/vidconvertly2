name: vidconvertly-backend
runtime: python3.8
entrypoint: backend/main.py
build:
  - pip install -r backend/requirements.txt 