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


@register(_name="menu")
class MenuFactory(factories.CKANFactory):
    class Meta:
        model = blocksmith_model.MenuModel
        action = "blocksmith_create_menu"

    name = factory.LazyFunction(lambda: fake.unique.slug())


@register(_name="menu_item")
class MenuItemFactory(factories.CKANFactory):
    class Meta:
        model = blocksmith_model.MenuItemModel
        action = "blocksmith_create_menu_item"

    title = factory.LazyFunction(lambda: fake.sentence())
    url = factory.LazyFunction(lambda: fake.url())
    order = 0
    parent_id = None
    classes = "some-class some-other-class"
    menu_id = factory.LazyFunction(lambda: MenuFactory()["id"])
