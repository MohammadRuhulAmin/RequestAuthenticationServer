import requests
from fastapi import FastAPI, Depends, HTTPException
from jose import JWTError, jwt, jwk
class KeycloakAuth:
    def __init__(self, keycloakUrl, realmName):
        self.keycloakUrl = keycloakUrl
        self.realmName = realmName
    
    def generateJwksUrl(self):
        postfixUrl = "/protocol/openid-connect/certs"
        jwks_url = f"{self.keycloakUrl}/realms/{self.realmName}" + postfixUrl
        return jwks_url
    
    def getKeycloakPublicKey(self):
        jwks_url = self.generateJwksUrl()
        try:
            response = requests.get(jwks_url)
            response.raise_for_status()
            jwks = response.json()
            if "keys" not in jwks:
                raise HTTPException(status_code=500, detail="Invalid JWKS response from Keycloak")
            return jwks["keys"]
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching JWKS: {e}")

    def decodeJwt(self, token):
        try:
            keys = self.getKeycloakPublicKey()
            headers = jwt.get_unverified_header(token)
            if not headers or "kid" not in headers:
                raise HTTPException(status_code=403, detail="Invalid token header")

            kid = headers["kid"]

            key_data = next((key for key in keys if key["kid"] == kid), None)
            if not key_data:
                raise HTTPException(status_code=403, detail="Public key for token not found")
            try:
                public_key = jwk.construct(key_data).public_key()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error constructing public key: {e}")

            try:
                payload = jwt.decode(
                    token,
                    public_key,
                    algorithms=["RS256"],
                    audience="account",  # change if your client ID is different
                    issuer=f"{self.keycloakUrl}/realms/{self.realmName}"
                )
                return payload
            except JWTError as e:
                raise HTTPException(status_code=403, detail=f"Invalid token: {e}")
        except Exception as E:
            raise 