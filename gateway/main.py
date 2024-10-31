# gateway/main.py
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp
import graphene
import requests
from decouple import config

DRF_URL=config("DRF_URL")
FA_URL=config("FA_URL")

class Query(graphene.ObjectType):
    products = graphene.List(graphene.String)
    cart = graphene.Field(graphene.String, user_id=graphene.Int())

    def get_django_users(self, info):
        response = requests.get(f"http://{DRF_URL}:8003/users/api/v1/users/user")
        return response.json()

    def get_fastapi_ads(self, info):
        response = requests.get(f"http://{FA_URL}:8004/ad/ads/")
        return response.json()
    
    def get_id_fastapi_ads(self, info, ads_id):
        response = requests.get(f"http://{FA_URL}:8004/ad/ads/{ads_id}/")
        return response.json()

app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))
