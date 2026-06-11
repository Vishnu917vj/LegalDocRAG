from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()