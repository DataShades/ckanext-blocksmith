import factory
import pytest
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

    url = factory.LazyFunction(lambda: fake.unique.slug())
    title = factory.LazyFunction(lambda: fake.sentence())
    html = "<p>Hello, world!</p>"
    data = '{"assets":[],"styles":[{"selectors":["#i5m5"],"style":{"padding":"10px"}}],"pages":[{"frames":[{"component":{"type":"wrapper","stylable":["background","background-color","background-image","background-repeat","background-attachment","background-position","background-size"],"attributes":{"id":"i41k"},"components":[{"type":"text","attributes":{"id":"i5m5"},"components":[{"type":"textnode","content":"Hello world"}]}],"head":{"type":"head"},"docEl":{"tagName":"html"}},"id":"iCHoiKaDRa2yMcto"}],"id":"WfDsiGNwJKoQUCMN"}],"symbols":[],"dataSources":[]}'
    fullscreen = False
    published = True


@pytest.fixture()
def clean_db(reset_db, migrate_db_for):
    reset_db()

    migrate_db_for("blocksmith")


@register(_name="sysadmin")
class SysadminFactory(factories.Sysadmin):
    pass
