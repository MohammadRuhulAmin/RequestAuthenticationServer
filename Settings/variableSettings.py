
from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.KeycloakConfig import KeycloakConfigClass
from fastapi.security import OAuth2PasswordBearer
from Config.FastApiConfig import FastApiConfig

keycloakVariable = KeycloakConfigClass(
    keycloakUrl=os.getenv("KEYCLOAK_URL"),
    realmName=os.getenv("REALM_NAME"),
    clientId=os.getenv("KEYCLOAK_CLIENT_ID")
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{keycloakVariable.keycloakUrl}/realms/{keycloakVariable.realmName}/protocol/openid-connect/token"
)

FastApiVariable = FastApiConfig(
    allowedOriginUrl=os.getenv("ALLOWED_ORIGIN_URL"),
    allowedRole = os.getenv("ALLOWED_ROLE")
)