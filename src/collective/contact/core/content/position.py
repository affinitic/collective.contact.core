from zope.interface import implements
from zope import schema
from z3c.form.interfaces import NO_VALUE

from five import grok

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.core import _
from collective.contact.core.interfaces import IContactContent
from collective.contact.core.browser.contactable import Contactable


class IPosition(model.Schema, IContactContent):
    """ """

    position_type = schema.Choice(
        title=_("Type"),
        vocabulary="PositionTypes",
        )

    def get_organization():
        """Returns organization"""


class PositionContactableAdapter(Contactable):
    grok.context(IPosition)

    @property
    def position(self):
        return self.context

    @property
    def organizations(self):
        organization = self.context.get_organization()
        return organization.get_organizations_chain()


class Position(Container):
    """ """
    implements(IPosition)
    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def get_organization(self):
        return self.getParentNode()

    def get_full_title(self):
        organization = self.get_organization().Title()
        return "%s (%s)" % (self.Title(), organization)


class PositionSchemaPolicy(grok.GlobalUtility,
                           DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_position")

    def bases(self, schemaName, tree):
        return (IPosition,)