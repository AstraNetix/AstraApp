package core;

import javafx.animation.Animation;
import javafx.animation.KeyFrame;
import javafx.animation.KeyValue;
import javafx.animation.Timeline;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.util.Duration;

import javax.jws.soap.SOAPBinding;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Timer;
import java.util.TimerTask;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Handles control flow for the login screen.
 * Created by Soham Kale on 2/20/18
 *
 */
public class LoginManager extends Manager implements PubNubClient.PubNubLoginDelegate {
    private PubNubClient _pubnub;
    private LoginController _controller;
    private Timeline _logoTimeline;

    LoginManager(Scene scene) {
        _scene = scene;
        _pubnub = new PubNubClient(this);
    }

    void showScreen() {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("login.fxml"));
            _scene.setRoot(loader.load());
            _controller = loader.getController();
            _controller.initManager(this);

            _logoTimeline = new Timeline(
                    new KeyFrame(Duration.seconds(1),
                            new KeyValue(_controller.logoImage.rotateProperty(), 110)),
                    new KeyFrame(Duration.seconds(0.5),
                            new KeyValue(_controller.logoImage.rotateProperty(), 0))
            );
            _logoTimeline.setCycleCount(Animation.INDEFINITE);
        } catch (IOException ex) {
            Logger.getLogger(LoginManager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    void login(String email, String password) {
        if (email.isEmpty()|| password.isEmpty()) {
            _controller.setErrorLabel("Please fill in the required fields");
            return;
        }

        _controller.disableButtons();
        _logoTimeline.play();

        _pubnub.loginSubscribe(email);
        _pubnub.publish(new HashMap<String, String>() {{
            put("status", "login");
            put("email", email);
            put("password", password);
        }});

        TimerTask quit = new TimerTask() {
            public void run() {
                _logoTimeline.pause();
                _controller.enableButtons();
                if (_controller.getErrorLabel().isEmpty()) {
                    _controller.setErrorLabel("There was a problem connecting to " +
                            "our servers. Please try again.");
                }
            }
        };

        Timer timer = new Timer();
        timer.schedule(quit, 4000L);
    }

    public synchronized void loginSuccess(String firstName, String lastName) {
        System.out.println("Login success!");
        if (!User.exists()) {
            _user = new User(firstName, lastName, _controller.email.getText());
            _pubnub.setUser(_user);
            _pubnub.publish(new HashMap<String, String>() {{
                put("status", "create");
                put("email", _user._email);
                put("name", _user._deviceName);
                put("company", _user._company);
                put("model", _user._model);
            }});
            _user.save();
        } else {
            _user = User.load();
        }
        _pubnub.loginUnsubscribe();

        MainManager mainManager = new MainManager(_scene, _user);
        mainManager.showScreen();
    }

    public void invalidCredentials(String error) {
        _controller.enableButtons();
        _logoTimeline.pause();
        _controller.setErrorLabel(error);
    }

    public void publishSuccess() {
        System.out.println("Publish Success!");
    }

    public void publishError(int errorCode) {
        _controller.enableButtons();
        _logoTimeline.pause();
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. Please try again.");
        System.out.println(errorCode);
    }

    public void unexpectedDisconnect() {
        _controller.enableButtons();
        _logoTimeline.pause();
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. We are trying to connect...");
        System.out.println("Unexpected Disconnect");
    }

    public void accessDenied() {
        _controller.enableButtons();
        _logoTimeline.stop();
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. We are trying to connect...");
        System.out.println("Access denied");
    }

    public void heartbeatFailure() {
        _controller.enableButtons();
        _logoTimeline.pause();
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. We are trying to connect...");
        System.out.println("Heartbeat Failure");
    }
}
