
import os
import sys

sys.path.append(os.path.abspath("/Users/ramazanimashovgmail.com/Developer/practice/microservice/first_poroject"))

import grpc
from . import user_pb2
from . import user_pb2_grpc


channel = grpc.insecure_channel('0.0.0.0:50051')
stub = user_pb2_grpc.UserServiceStub(channel)


def get_user(user_id: int):
    try:
        response = stub.GetUser(user_pb2.UserRequest(user_id=user_id))
        return response
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")
        return None


def verify_token(token: str):
    try:
        response = stub.CheckVerifyToken(user_pb2.TokenRequest(token=token))
        if response.is_valid:
            return response
        else:
            return None
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")
        return None





