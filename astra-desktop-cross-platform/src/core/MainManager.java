package core;

import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Handles control flow for main application screen.
 * Created by Soham Kale on 2/20/18
 *
 */
public class MainManager implements PubNubClient.PubNubDelegate {
    private Scene _scene;
    private PubNubClient _pubnub;
    private MainController _controller;

    MainManager(Scene scene, User user) {
        _scene = scene;

        _pubnub = new PubNubClient(this);
        _pubnub.setUser(user);
    }

    void showMainScreen() {
        try {
            FXMLLoader loader = new FXMLLoader(
                    getClass().getResource("main.fxml")
            );
            _scene.setRoot(loader.load());

            Thread boinc = new Thread(() -> {
                BashClient.bashPersist("./boinc -insecure");
            });
            boinc.start();
        } catch (IOException ex) {
            Logger.getLogger(LoginManager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    void logout() {
        LoginManager loginManager = new LoginManager(_scene);
        loginManager.showLoginScreen();
    }


    public void publishSuccess() {
        _controller.setErrorMessages("Published Successfully!");
    }

    public void publishError(int errorCode) {
        _controller.setErrorMessages("Error: " + Integer.toString(errorCode) + ".");
    }

    public void unexpectedDisconnect() {
        _controller.setErrorMessages("Error: Unexpected Disconnect.");
    }

    public void accessDenied() {
        _controller.setErrorMessages("Error: Access Denied.");
    }

    public void heartbeatFailure() {
        _controller.setErrorMessages("Error: Heartbeat Failure.");
    }

}
