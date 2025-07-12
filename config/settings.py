from dotenv import load_dotenv
import os

load_dotenv()
AWS_REGION_NAME =os.getenv("AWS_REGION_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]