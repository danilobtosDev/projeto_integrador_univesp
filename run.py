# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Usar debug=True apenas para desenvolvimento local
    app.run(debug=True)