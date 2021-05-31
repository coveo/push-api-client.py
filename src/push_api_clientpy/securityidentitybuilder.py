from typing import Union

from .document import SecurityIdentity
from .platformclient import SecurityIdentityType


class SecurityIdentityBuilder:
    def build(self) -> Union[SecurityIdentity, list[SecurityIdentity]]:
        raise NotImplementedError


class AnySecurityIdentityBuilder(SecurityIdentityBuilder):
    def __init__(self, identity: str, identityType: SecurityIdentityType, securityProvider: str) -> None:
        self.identity = identity
        self.identityType = identityType
        self.securityProvider = securityProvider

    def build(self):
        return SecurityIdentity(identity=self.identity, identityType=self.identityType, securityProvider=self.securityProvider)


class UserSecurityIdentityBuilder(SecurityIdentityBuilder):
    def __init__(self, identity: Union[str, list[str]], securityProvider: str = "Email Security Provider") -> None:
        self.identity = identity
        self.securityProvider = securityProvider

    def build(self):
        if type(self.identity) is list:
            return list(map(lambda identity: AnySecurityIdentityBuilder(identity, "USER", self.securityProvider).build(), self.identity))

        return AnySecurityIdentityBuilder(self.identity, "USER", self.securityProvider).build()


class GroupSecurityIdentityBuilder(SecurityIdentityBuilder):
    def __init__(self, group: Union[str, list[str]], securityProvider: str) -> None:
        self.group = group
        self.securityProvider = securityProvider

    def build(self):
        if type(self.group) is list:
            return list(map(lambda group: AnySecurityIdentityBuilder(group, "GROUP", self.securityProvider).build(), self.group))

        return AnySecurityIdentityBuilder(self.group, "GROUP", self.securityProvider).build()


class VirtualGroupSecurityIdentityBuilder(SecurityIdentityBuilder):
    def __init__(self, virtualGroup: Union[str, list[str]], securityProvider: str) -> None:
        self.virtualGroup = virtualGroup
        self.securityProvider = securityProvider

    def build(self):
        if type(self.virtualGroup) is list:
            return list(map(lambda virtualGroup: AnySecurityIdentityBuilder(virtualGroup, "VIRTUAL_GROUP", self.securityProvider).build(), self.virtualGroup))

        return AnySecurityIdentityBuilder(self.virtualGroup, "VIRTUAL_GROUP", self.securityProvider).build()
