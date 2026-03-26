import os

from dotenv import load_dotenv

load_dotenv() # loads the environmental variable  from .env file 


def main():
    print(f"{os.getenv('OPENAI_API_KEY')}")
    print("Hello from 1stapp!")


if __name__ == "__main__":
    main()
