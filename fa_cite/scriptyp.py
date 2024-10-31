from main import app  # Импортируйте приложение из вашего основного файла FastAPI
import json

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f)
