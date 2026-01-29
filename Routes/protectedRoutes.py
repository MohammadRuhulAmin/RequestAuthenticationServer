from fastapi import Depends
from Settings.variableSettings import oauth2_scheme
from Authentication.Auth import KeycloakAuth

class ProtectedResources:
    def __init__(self, kauth: KeycloakAuth):
        self.kauth = kauth

    def protectedResource(self, token: str = Depends(oauth2_scheme)):
        decodeToken = self.kauth.decodeJwt(token)
        username = decodeToken.get("preferred_username", "unknown")
        roles = decodeToken.get("realm_access", {}).get("roles", [])
        return {
            "message": "Successfully Authenticated!",
            "user": username,
            "roles": roles
        }
