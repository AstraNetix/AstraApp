package core;

import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;

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
public class LoginManager implements PubNubClient.PubNubLoginDelegate {
    private Scene _scene;
    private PubNubClient _pubnub;
    private User _user;
    private LoginController _controller;

    LoginManager(Scene scene) {
        _scene = scene;
        _pubnub = new PubNubClient(this);
    }

    void showLoginScreen() {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("login.fxml"));
            _scene.setRoot(loader.load());
            _controller = loader.getController();
            _controller.initManager(this);
        } catch (IOException ex) {
            Logger.getLogger(LoginManager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    void login(String email, String password) {
        if (email.isEmpty()|| email.isEmpty()) {
            _controller.setErrorLabel("Please fill in the required fields");
            return;
        }
        _controller.disableButtons();

        _pubnub.loginSubscribe(email);
        _pubnub.publish(new HashMap<String, String>() {{
            put("status", "login");
            put("email", email);
            put("password", password);
        }});

        TimerTask quit = new TimerTask() {
            public void run() {
                _controller.setErrorLabel("There was a problem connecting to " +
                        "our servers. Please try again.");
                _controller.enableButtons();

                //TODO: only for debugging!
                loginSuccess("Soham", "Kale");
            }
        };

        Timer timer = new Timer();
        timer.schedule(quit, 5000L);
    }

    public void loginSuccess(String firstName, String lastName) {
        File userData = new File("./user_data.txt");
        if (!userData.exists()) {
            _user = new User(firstName, lastName, _controller.email.getText());
            _pubnub.publish(new HashMap<String, String>() {{
                put("status", "create");
                put("user-email", _user._email);
                put("name", _user._deviceName);
                put("company", _user._company);
                put("model", _user._model);
            }});
            _user.save();
        } else {
            _user = User.load();
        }

        MainManager mainManager = new MainManager(_scene, _user);
        mainManager.showMainScreen();
    }

    public void invalidCredentials(String error) {
        _controller.enableButtons();
        _controller.setErrorLabel(error);
    }

    public void publishSuccess() {

    }

    public void publishError(int errorCode) {
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. Please try again.");
        System.out.println(errorCode);
    }

    public void unexpectedDisconnect() {
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. We are trying to connect...");
        System.out.println("Unexpected Disconnect");
    }

    public void accessDenied() {
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. We are trying to connect...");
        System.out.println("Access denied");
    }

    public void heartbeatFailure() {
        _controller.setErrorLabel("There was a problem connecting to " +
                "our servers. We are trying to connect...");
        System.out.println("Heartbeat Failure");
    }
}
