from flask import redirect
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from flask_cors import CORS

from routes.accessories import api as accessories_api
from routes.users import api as users_api
from routes.wells import api as wells_api

info = Info(title="Cementing Accessories API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")


@app.get("/", tags=[home_tag])
def home():
    """Redireciona à documentação da API."""
    return redirect("/openapi/swagger")


app.register_api(accessories_api)
app.register_api(wells_api)
app.register_api(users_api)
