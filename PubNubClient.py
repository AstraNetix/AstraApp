import time
import hashlib

import logging
import pubnub

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

User = get_user_model()

class PubNubClient(SubscribeCallback):

    NUM_CORES = 8

    device_id = 5

    ##############################################################################################
    # PubNubSetup

    def __init__(self):
        pubnub.set_stream_logger('pubnub', logging.DEBUG)

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = "sub-c-d5c0f6b8-f436-11e7-b8a6-46d99af2bb8c"
        pnconfig.publish_key = "pub-c-79775796-e891-4ba0-8e96-af4a5dd71beb"
        pnconfig.ssl = False

        self.pubnub = PubNub(pnconfig)

        self.pubnub.subscribe().channels("create").execute()
        self.pubnub.subscribe().channels(self.get_sub_channel()).execute() 

        self.pubnub.add_listener(self)

        self.async_changed = False


    @staticmethod
    def get_sub_channel():
        return str(device_id)


    ##############################################################################################
    # Publish

    def publish(self, message):
        try:
            return self.pubnub.publish().channel(self.get_pub_channel()).message(message).sync()
        except PubNubException as e:
            pass
            # handle exception 

    @staticmethod
    def get_pub_channels():
        return str(device_id % NUM_CORES) 


    ##############################################################################################
    # Responses

    def status(self, pubnub, status):
        if (status.operation == PNOperationType.PNSubscribeOperation
            or status.operation == PNOperationType.PNUnsubscribeOperation):
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # Handle successful subscribing
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # Handle temporary device connection issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # Handle successful unsubscribing
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                raise DeviceClientError.unexpected_disconnect()
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # Handle channel denial
        elif status.operation == PNOperationType.PNSubscribeOperation:
            if status.is_error():
                pass
                # Handle heartbeat operation error

    def message(self, pubnub, message):
        message = message.data.message
        if message["status"] == "start":
            pass # Run yo miner ho
        elif message["status"] == "stop":
            pass # Stop your miner ho 

    def check_for_response(self):
        time.sleep(5)
        if not self.async_changed:
            return False
        cls.async_changed = False

