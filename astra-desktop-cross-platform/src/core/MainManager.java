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
public class MainManager extends Manager implements PubNubClient.PubNubDelegate {
    private PubNubClient _pubnub;
    private MainController _controller;
    private Thread _boinc;

    MainManager(Scene scene, User user) {
        _scene = scene;
        _user = user;
        _pubnub = new PubNubClient(this);
        _pubnub.setUser(user);
    }

    void showScreen() {
        try {
            FXMLLoader loader = new FXMLLoader(
                    getClass().getResource("main.fxml")
            );
            _scene.setRoot(loader.load());
            _boinc = BoincCommands.startBoinc();

            _controller = loader.getController();
            _controller.initManager(this);
            _controller.deviceName.setText(_user._deviceName);

        } catch (IOException ex) {
            Logger.getLogger(LoginManager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    void logout() {
        BoincCommands.quit();
        LoginManager loginManager = new LoginManager(_scene);
        loginManager.showScreen();
    }

    void quit() { Main.quit(_user); }


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
