
import os
from app import application

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4433))
    application.run('127.0.0.1', port=port)