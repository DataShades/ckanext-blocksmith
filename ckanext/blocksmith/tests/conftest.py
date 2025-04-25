import pytest
from faker import Faker
from pytest_factoryboy import register

from ckan.tests import factories

from ckanext.blocksmith import model as blocksmith_model

fake = Faker()


@register(_name="blocksmith_page")
class PageFactory(factories.CKANFactory):
    class Meta:
        model = blocksmith_model.PageModel
        action = "blocksmith_page_save"

    name = fake.slug()
    title = fake.sentence()
    html = fake.sentence()
    css = fake.sentence()
    editor_data = {"fake": "data"}
    published = True
    order_index = 1


@pytest.fixture()
def clean_db(reset_db, migrate_db_for):
    reset_db()

    migrate_db_for("blocksmith")


@register(_name="sysadmin")
class SysadminFactory(factories.Sysadmin):
    pass
