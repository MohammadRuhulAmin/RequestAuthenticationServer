import logging
logging.basicConfig(level=logging.INFO)
class KeycloakConfigClass:
    def __init__(self, keycloakUrl,realmName,clientId):
        self.keycloakUrl = keycloakUrl
        self.realmName = realmName
        self.clientId = clientId
    
    def configproperties(self):
        try:
            logging.info("Keycloak URL: %s", self.keycloakUrl)
            logging.info("Keycloak realm name: %s",self.realmName)
            logging.info("Keycloak client: %s", self.clientId)
        except Exception as E:
            logging.error(str(E))

