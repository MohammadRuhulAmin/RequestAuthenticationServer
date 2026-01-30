class IsForbiddenRequestToken:
    def __init__(self, requiredOrigin, requiredRole ,allowedOriginsList,accessRoleList):
        self.allowedOriginsList = allowedOriginsList
        self.accessRoleList = accessRoleList,
        self.requiredOrigin = requiredOrigin
        self.requiredRole = requiredRole
    
    def checkAllowedOrigin(self) -> bool:
        try:
            return any(alwdUrl.strip() == self.requiredOrigin for alwdUrl in self.allowedOriginsList)
        except Exception:
            return False
    def checkAllowedRole(self)-> bool:
        try:
            return any(alwdRole.strip() == self.requiredRole for alwdRole  in self.accessRoleList[0])
        except Exception:
            return False
    
