import os


class Config:

    # Get environment from environment variable, default to 'dev'
    ENV = os.getenv("ENV", "dev").strip().lower()

    if ENV == "prod":
        BASE_URL = "https://wadhwanientrepreneur.ai/en/login"
    else:
        BASE_URL = "https://dev.wadhwanientrepreneur.ai/en/login"

    # Authentication
    PHONE_NUMBER = os.getenv("PHONE_NUMBER", "4800048000")
    OTP = os.getenv("OTP", "2806")