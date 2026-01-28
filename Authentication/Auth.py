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

    def decodeJwt(self, token: str):
        try:
            keys = self.getKeycloakPublicKey()
            headers = jwt.get_unverified_header(token)
            if not headers or "kid" not in headers:
                raise HTTPException(status_code=401, detail="Invalid token header")
            kid = headers["kid"]
            key_data = next((key for key in keys if key["kid"] == kid), None)
            if not key_data:
                raise HTTPException(status_code=401, detail="Public key not found")
            public_key = jwk.construct(key_data).public_key()
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience="account",   # or your client_id
                issuer=f"{self.keycloakUrl}/realms/{self.realmName}"
            )
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        except HTTPException:
            raise
        except Exception as e:
            # unknown error → internal server error
            raise HTTPException(
                status_code=500,
                detail=f"Authentication service error: {str(e)}"
            )
        # Traceback 