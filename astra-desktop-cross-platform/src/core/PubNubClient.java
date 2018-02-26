package core;

import com.google.gson.JsonObject;
import com.pubnub.api.PNConfiguration;
import com.pubnub.api.PubNub;
import com.pubnub.api.callbacks.PNCallback;
import com.pubnub.api.callbacks.SubscribeCallback;
import com.pubnub.api.models.consumer.PNPublishResult;
import com.pubnub.api.models.consumer.PNStatus;
import com.pubnub.api.models.consumer.pubsub.PNMessageResult;
import com.pubnub.api.models.consumer.pubsub.PNPresenceEventResult;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import static java.util.Collections.singletonList;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * A client for interfacing with PubNub operations and checking status, presence.
 * Created by Soham Kale on 2/20/18
 *
 */
public class PubNubClient extends SubscribeCallback {

    PubNubClient(PubNubDelegate delegate, User... user) {
        _delegate = delegate;

        PNConfiguration pnConfiguration = new PNConfiguration();
        pnConfiguration.setSubscribeKey("sub-c-d5c0f6b8-f436-11e7-b8a6-46d99af2bb8c");
        pnConfiguration.setPublishKey("pub-c-79775796-e891-4ba0-8e96-af4a5dd71beb");

        _pubNub = new PubNub(pnConfiguration);
        _pubNub.addListener(this);

        _boincClient = new BoincClient(user);
    }

    void setUser(User user) {
        _user = user;
        _boincClient.setUser(user);
        _pubNub.subscribe().channels(new ArrayList<>(singletonList(_user._deviceID))).execute();
    }

    void publish(Map data) {
        _pubNub.publish().message(data).channel(getPublishChannel()).async(new PNCallback<PNPublishResult>() {
            @Override
            public void onResponse(PNPublishResult result, PNStatus status) {
                if(status.isError() && _delegate != null) {
                    _delegate.publishError(status.getStatusCode());
                    System.out.println(status);
                } else if (_delegate != null) {
                    _delegate.publishSuccess();
                }
            }
        });
    }

    public void status(PubNub pubnub, PNStatus status) {
        if (status.getOperation() == null)
            /** After a reconnection see status.getCategory() */

        switch (status.getOperation()) {
            case PNSubscribeOperation:
            case PNUnsubscribeOperation:
                switch (status.getCategory()) {
                    case PNUnexpectedDisconnectCategory:
                        if (_delegate != null) _delegate.unexpectedDisconnect();
                    case PNAccessDeniedCategory:
                        if (_delegate != null) _delegate.accessDenied();
                }
            case PNHeartbeatOperation:
                if (status.isError())
                    if (_delegate != null) _delegate.heartbeatFailure();
            default: {
                // Encountered unknown status type
            }
        }
    }

    public void presence(PubNub pubnub, PNPresenceEventResult presence) {

    }

    public void message(PubNub pubnub, PNMessageResult result) {
        JsonObject message;
        if (result.getMessage().isJsonObject()) {
            message = result.getMessage().getAsJsonObject();
        } else { return; }

        switch (message.get("function").getAsString()) {
            case "login-success":
                _pubNub.unsubscribe().channels(new ArrayList<>(singletonList(_user._email))).execute();
                if (_delegate instanceof PubNubLoginDelegate)
                    ((PubNubLoginDelegate) _delegate).loginSuccess(
                            message.get("first-name").getAsString(),
                            message.get("last-name").getAsString()
                    );
            case "invalid-credentials":
                _pubNub.unsubscribe().channels(new ArrayList<>(singletonList(_user._email))).execute();
                if (_delegate instanceof PubNubLoginDelegate)
                    ((PubNubLoginDelegate) _delegate).invalidCredentials(message.get("error").getAsString());

            case "start-project":
                _boincClient.startProject(message.get("url").getAsString());
            case "quit-project":
                BoincCommands.noMoreWorkProject(message.get("url").getAsString());
            case "resume-project":
                BoincCommands.resetProject(message.get("url").getAsString());
            case "suspend-project":
                BoincCommands.suspendProject(message.get("url").getAsString());
            case "no-more-work":
                BoincCommands.noMoreWorkProject(message.get("url").getAsString());

            case "project-status":
                publish(_boincClient.getProjectInfo(message.get("url").getAsString()));

            case "disk-usage":
                publish((_boincClient.getDiskUsage(message.get("url").getAsString())));
            case "total-disk-usage":
                publish((_boincClient.getTotalDiskUsage()));

            case "quit":
                BoincCommands.quit();
            default:
                publish(new HashMap<String, String>() {{
                    put("status", "unknown-command");
                }});
        }
    }

    interface PubNubDelegate {
        void publishSuccess();
        void publishError(int errorCode);
        void unexpectedDisconnect();
        void accessDenied();
        void heartbeatFailure();
    }

    interface PubNubLoginDelegate extends PubNubDelegate {
        void loginSuccess(String firstName, String lastName);
        void invalidCredentials(String error);
    }

    void loginSubscribe(String email) {
        _email = email;
        _pubNub.subscribe().channels(new ArrayList<>(singletonList(email))).execute();
    }

    void loginUnsubscribe() {
        _pubNub.unsubscribe().channels(new ArrayList<>(singletonList(_email))).execute();
    }

    private String getSubscribeChannel() { return String.valueOf(Long.parseLong(_user._deviceID) % _coreNum); }

    private String getPublishChannel() {
        return _user == null ? "create" : String.valueOf(Long.parseLong(_user._deviceID));
    }

    private PubNub _pubNub;
    private User _user;
    private String _email;
    private PubNubDelegate _delegate;
    private BoincClient _boincClient;

    private static int _coreNum = 8;

}
