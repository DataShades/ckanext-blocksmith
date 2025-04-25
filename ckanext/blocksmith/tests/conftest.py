import pytest
import factory
from faker import Faker
from pytest_factoryboy import register

from ckan.tests import factories

from ckanext.blocksmith import model as blocksmith_model

fake = Faker()


@register(_name="page")
class PageFactory(factories.CKANFactory):
    class Meta:
        model = blocksmith_model.PageModel
        action = "blocksmith_create_page"

    name = factory.LazyFunction(lambda: fake.unique.slug())
    title = factory.LazyFunction(lambda: fake.sentence())
    html = "<p>Hello, world!</p>"
    data = "{}"
    fullscreen = False
    published = True


@pytest.fixture()
def clean_db(reset_db, migrate_db_for):
    reset_db()

    migrate_db_for("blocksmith")


@register(_name="sysadmin")
class SysadminFactory(factories.Sysadmin):
    pass
