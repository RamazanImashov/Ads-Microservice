from fastapi import FastAPI, Request
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
import graphene
import httpx
import requests
from decouple import config

DRF_URL = config("DRF_URL")
FA_URL = config("FA_URL")

app = FastAPI()

# REST маршрутизация для перенаправления запросов
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_users(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"http://{DRF_URL}:8003/{path}",
            headers=request.headers.raw,
            content=await request.body()
        )
        return response.json()

@app.api_route("/ads/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_ads(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"http://{FA_URL}:8004/{path}",
            headers=request.headers.raw,
            content=await request.body()
        )
        return response.json()

# GraphQL Schema
class Query(graphene.ObjectType):
    get_django_users = graphene.List(graphene.String)
    get_fastapi_ads = graphene.List(graphene.String)
    get_id_fastapi_ads = graphene.Field(graphene.String, ads_id=graphene.Int())

    def resolve_get_django_users(self, info):
        response = requests.get(f"http://{DRF_URL}:8003/users/api/v1/users/user")
        return response.json()

    def resolve_get_fastapi_ads(self, info):
        response = requests.get(f"http://{FA_URL}:8004/ad/ads/")
        return response.json()

    def resolve_get_id_fastapi_ads(self, info, ads_id):
        response = requests.get(f"http://{FA_URL}:8004/ad/ads/{ads_id}/")
        return response.json()

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query), on_get=make_graphiql_handler()), methods=["GET", "POST"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
