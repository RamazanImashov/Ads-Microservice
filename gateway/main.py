# gateway/main.py
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import graphene
import requests
from decouple import config

class Query(graphene.ObjectType):
    products = graphene.List(graphene.String)
    cart = graphene.Field(graphene.String, user_id=graphene.Int())

    def django_users(self, info):
        response = requests.get(f"http://{config("DRF_URL")}:8080/products")
        return response.json()

    def fastapi_ads(self, info, user_id):
        response = requests.get(f"http://{config("FA_URL")}:8001/cart/?user_id={user_id}")
        return response.json()

app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))
