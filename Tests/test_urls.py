import datetime
import os
import pytest
import pytz

from Data.websites import urls
from Modules.Helpers.gmail_service import get_link_from_mail


@pytest.fixture
def clear_screenshots():
    @pytest.fixture(scope="module")
    def driver_ext():
        folder = 'Screenshots/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


class TestAppearance(object):

    @pytest.mark.parametrize("url", [urls])
    def test_appearance(self, clear_screenshots, driver):
        get_link_from_mail("Fortuna Intelligent Prospecting (Dev) password restoration")
        z = 5

