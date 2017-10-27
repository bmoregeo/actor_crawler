import logging
from urllib.parse import urlparse

from thespian.actors import ActorTypeDispatcher, ActorExitRequest
from thespian.troupe import troupe
from splinter import Browser

from actors.messages import ScreenShotRequestMsg


log = logging.getLogger('thespian.log')

@troupe(25)
class ScreenShotActor(ActorTypeDispatcher):
    """
    Actor for taking screenshots
    """

    def __init__(self):
        super().__init__()
        self.browser = Browser('phantomjs')


    def receiveMsg_ScreenShotRequestMsg(self, message: ScreenShotRequestMsg, sender: ActorTypeDispatcher) -> None:
        """
        Receive a request for screens hot
        """
        log.debug('ScreenShotActor[ScreenShotRequestMsg] : ' + str(message))
        image_name = ('/screen' + str(urlparse(message.url).path).replace('/', '_')).rstrip('_') + '.png'
        result_path = message.save_dir + image_name
        self.browser.visit(message.url)
        self.browser.driver.save_screenshot(result_path)

    def receiveMsg_ActorExitRequest(self, message: ActorExitRequest, sender: ActorTypeDispatcher):
        """
        Close Browser upon exit
        """
        log.debug('ScreenShotActor[ActorExitRequest]')
        self.browser.close()