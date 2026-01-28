from Settings.keycloakSettings import keycloakVariable
from Authentication.Auth import KeycloakAuth

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import JWTError, jwt, jwk
app = FastAPI()
Kauth = KeycloakAuth(
    keycloakUrl=keycloakVariable.keycloakUrl,
    realmName=keycloakVariable.realmName
)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{keycloakVariable.keycloakUrl}/realms/{keycloakVariable.realmName}/protocol/openid-connect/token"
)

@app.get("/hello")
async def hello_route():
    return {"message": "Hello World!"}

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    decoded_token = Kauth.decodeJwt(token)
    username = decoded_token.get("preferred_username", "unknown")
    roles = decoded_token.get("realm_access", {}).get("roles", [])
    return {
        "message": "Successfully authenticated!",
        "user": username,
        "roles": roles
    }