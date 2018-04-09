import logging
import pubnub

from django.contrib.auth import get_user_model
from api.exceptions.user_exceptions import AuthenticationError
from api.exceptions.device_exceptions import DeviceClientError

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

User = get_user_model()

class PubNubClient(SubscribeCallback):

    NUM_CORES = 2

    ##############################################################################################
    # PubNubSetup
    
    def __init__(self, delegate):
        self.delegate = delegate

        pubnub.set_stream_logger('pubnub', logging.DEBUG)

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = "sub-c-d5c0f6b8-f436-11e7-b8a6-46d99af2bb8c"
        pnconfig.publish_key = "pub-c-79775796-e891-4ba0-8e96-af4a5dd71beb"
        pnconfig.ssl = False

        self.pubnub = PubNub(pnconfig)

        self.pubnub.subscribe().channels("create").execute()
        (self.pubnub.subscribe().channels(i).execute() 
            for i in range(NUM_CORES))

        self.pubnub.add_listener(self)

        self.async_changed = False

    def quit_client(self):
        self.pubnub.remove_listener(self)

    @staticmethod
    def get_sub_channel(device_id):
        return device_id[0]


    ##############################################################################################
    # Publish

    def publish(self, message, device_id=None, login=False):
        try:
            return self.pubnub.publish().channel(
                    self.get_pub_channel(device_id, login, message)
                ).message(message).sync()
        except PubNubException as pne:
            pass 
            # TODO: Handle PubNub exception pne
 
    @staticmethod
    def get_pub_channel(device_id, login, message):
        return device_id if not login else message["email"]


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
        message = message.message
        if message["status"] == "login":
            self.login(message)
        elif message["status"] == "create":
            self.create_device(message)
        elif message["status"] == "update":
            pass
            # Run update chain
        elif message["status"] == "success":
            self.success_chain(message)
        elif message["status"] == "failure":
            pass
            # Run failure chain

    def login(self, message):
        try:
            user = User.authenticate(email=message['email'], password=message['password'])
            if 'id' in message: # To account for first-time login
                instance = self.delegate.objects.get(uid=message['id'])
                instance.active = True
            self.publish(message={
                "function": "login-success",
                "email": message['email'],
                "first-name": user.first_name,
                "last-name": user.last_name,
            }, login=True)
        except AuthenticationError as ae:
            self.publish(message={
                "function": "invalid-credentials",
                "error": str(ae),
                "email": message['email'],
            }, login=True)

    def create_device(self, message):
        self.delegate.create({
                'name': message['name'], 
                'company': message['company'], 
                'model': message['model'],
                'email': message['email'],
            })

    def update_chain(self, message):
        pass

    def success_chain(self, message):
        instance = self.delegate.objects.get(uid=message["id"])
        if message["function"] == "start-project":
            instance.start_project_async(message["url"])
        elif message["function"] == "quit-project":
            instance.quit_project_async(message["url"])

    def check_for_response(self):
        return self.pubnub.time()



