import requests
import base64
import json
from typing import Dict, Any, List
from fastapi import HTTPException
from jose import JWTError, jwt, jwk

class KeycloakAuth:
    def __init__(self, keycloakUrl: str, realmName: str, allowedOriginUrl):
        self.keycloakUrl = keycloakUrl
        self.realmName = realmName
        self.allowedOriginUrl = allowedOriginUrl

    def generateJwksUrl(self) -> str:
        return f"{self.keycloakUrl}/realms/{self.realmName}/protocol/openid-connect/certs"

    def getKeycloakPublicKey(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(self.generateJwksUrl())
            response.raise_for_status()
            jwks = response.json()
            if "keys" not in jwks:raise HTTPException(500, "Invalid JWKS response from Keycloak")
            return jwks["keys"]
        except Exception as e:
            raise HTTPException(500, f"Error fetching JWKS: {e}")


    # Base64URL decode helper
    def _b64url_decode(self, data: str) -> str:
        padding = '=' * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding).decode()

    def tokenParser(self, token: str) -> Dict[str, Any]:
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")

            return {
                "header": {
                    "base64": header_b64,
                    "json": json.loads(self._b64url_decode(header_b64))
                },
                "payload": {
                    "base64": payload_b64,
                    "json": json.loads(self._b64url_decode(payload_b64))
                },
                "signature": {
                    "base64": signature_b64
                }
            }
        except Exception as e:
            raise HTTPException(400, f"Invalid JWT format: {e}")
    def checkAllowedOrigins(self,allowedOriginsList: list)-> bool:
        try:
            for allowedOrigin in allowedOriginsList:
                if allowedOrigin == self.allowedOriginUrl:
                    return True 
            return False
        except Exception as E:
            print(str(E))
    def decodeJwt(self, token: str) -> Dict[str, Any]:
        try:
            tokenDetails = self.tokenParser(token)
            print(json.dumps(tokenDetails, indent=2))
            keys = self.getKeycloakPublicKey()
            headers = jwt.get_unverified_header(token)
            kid = headers.get("kid")
            if not kid: raise HTTPException(401, "Missing kid in token header")
            key_data = next((k for k in keys if k["kid"] == kid), None)
            if not key_data:raise HTTPException(401, "Public key not found")
            print("allowed-origins: ", tokenDetails.get("payload").get("json").get("allowed-origins"))
            allowedOriginList = tokenDetails.get("payload").get("json").get("allowed-origins")
            if self.checkAllowedOrigins(allowedOriginList) == False:raise HTTPException(401, "Allowed Origin Missmached")

            public_key = jwk.construct(key_data).public_key()
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience="account",   # better: your client_id
                issuer=f"{self.keycloakUrl}/realms/{self.realmName}"
            )

            return payload

        except JWTError:
            raise HTTPException(401, "Invalid or expired token")
