from urllib.parse import urlparse

from thespian.actors import ActorTypeDispatcher
from splinter import Browser

from actors.messages import ScreenShotRequestMsg


class ScreenShotActor(ActorTypeDispatcher):
    """
    Actor for taking screenshots
    """

    def receiveMsg_ScreenShotRequestMsg(self, message: ScreenShotRequestMsg, sender: ActorTypeDispatcher) -> None:
        """
        Receive a request for screens hot
        """
        print('ScreenShotActor[ScreenShotRequestMsg]', message)
        image_name = ('/screen' + str(urlparse(message.url).path).replace('/', '_')).rstrip('_') + '.png'
        result_path = message.save_dir + image_name
        with Browser('phantomjs') as browser:
            browser.visit(message.url)
            browser.driver.save_screenshot(result_path)
