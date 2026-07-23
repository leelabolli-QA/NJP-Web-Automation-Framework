import os, yaml
from dotenv import load_dotenv
load_dotenv()
ENV=os.getenv("ENV","qa")
with open("config/config.yaml") as f:
    config=yaml.safe_load(f)
env=config[ENV]
BASE_URL=os.getenv("BASE_URL",env["base_url"])
TIMEOUT=env["timeout"]
HEADLESS=os.getenv("HEADLESS","false").lower()=="true"
PHONE_NUMBER=os.getenv("PHONE_NUMBER")
OTP=os.getenv("OTP")
