class IsForbiddenRequestToken:
    def __init__(self, requiredOrigin,allowedOriginsList,accessRole):
        self.allowedOriginsList = allowedOriginsList
        self.accessRole = accessRole,
        self.requiredOrigin = requiredOrigin
    
    def checkAllowedOrigin(self) -> bool:
        try:
            return any(o.strip() == self.requiredOrigin for o in self.allowedOriginsList)
        except Exception:
            return False
    
