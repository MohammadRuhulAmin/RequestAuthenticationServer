
from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.KeycloakConfig import KeycloakConfigClass



keycloakVariable = KeycloakConfigClass(
    keycloakUrl=os.getenv("KEYCLOAK_URL"),
    realmName=os.getenv("REALM_NAME"),
    clientId=os.getenv("KEYCLOAK_CLIENT_ID")
)

