from push_api_clientpy.securityidentitybuilder import GroupSecurityIdentityBuilder, UserSecurityIdentityBuilder, VirtualGroupSecurityIdentityBuilder


class TestSecurityIdentityBuilder:
    def testUserSecurityIdentityBuilderProviderByDefault(self):
        identity = UserSecurityIdentityBuilder("the_identity")
        assert identity.build().identity == "the_identity"
        assert identity.build().identityType == "USER"
        assert identity.build().securityProvider == "Email Security Provider"

    def testUserSecurityIdentityBuilderProviderDefined(self):
        identity = UserSecurityIdentityBuilder("the_identity", "my provider")
        assert identity.build().securityProvider == "my provider"

    def testUserSecurityIdentityBuilderMultipleIdentities(self):
        identities = UserSecurityIdentityBuilder(["first", "second"])
        assert identities.build()[0].identity == "first"
        assert identities.build()[1].identity == "second"

    def testGroupSecurityIdentityBuilder(self):
        group = GroupSecurityIdentityBuilder("the_group", "my provider")
        assert group.build().identity == "the_group"
        assert group.build().identityType == "GROUP"
        assert group.build().securityProvider == "my provider"

    def testGroupSecurityIdentityBuilderMultipleIdentities(self):
        group = GroupSecurityIdentityBuilder(["first", "second"], "my provider")
        assert group.build()[0].identity == "first"
        assert group.build()[1].identity == "second"

    def testVirtualGroupSecurityIdentityBuilder(self):
        group = VirtualGroupSecurityIdentityBuilder("the_group", "my provider")
        assert group.build().identity == "the_group"
        assert group.build().identityType == "VIRTUAL_GROUP"
        assert group.build().securityProvider == "my provider"

    def testVirtualGroupSecurityIdentityBuilderMultipleIdentities(self):
        group = VirtualGroupSecurityIdentityBuilder(["first", "second"], "my provider")
        assert group.build()[0].identity == "first"
        assert group.build()[1].identity == "second"
