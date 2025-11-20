# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Certifique-se de que você está executando este arquivo
    app.run(debug=True)