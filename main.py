from Settings.variableSettings import keycloakVariable,oauth2_scheme,FastApiVariable
from Authentication.TokenDecoder import KeycloakAuth
from Routes.protectedRoutes import ProtectedResources
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import JWTError, jwt, jwk
app = FastAPI()

Kauth = KeycloakAuth(
    keycloakUrl=keycloakVariable.keycloakUrl,
    realmName=keycloakVariable.realmName,
    allowedOriginUrl=FastApiVariable.allowedOriginUrl,
    allowedRole = FastApiVariable.allowedRole
)

@app.get("/hello")
async def hello_route():
    return {"message": "Hello World!"}

@app.get("/protected")
def protectedProperties(token:str = Depends(oauth2_scheme)):
    pr = ProtectedResources(Kauth)
    return pr.protectedResource(token)