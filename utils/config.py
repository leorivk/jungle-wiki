import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # 개발 환경에서는 False, 실제 배포 시에는 True로 설정
    JWT_COOKIE_CSRF_PROTECT = True  # CSRF 보호 활성화
