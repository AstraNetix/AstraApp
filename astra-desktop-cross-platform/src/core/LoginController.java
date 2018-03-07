package core;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.text.Text;

import java.awt.*;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Manages elements of the login screen.
 * Created by Soham Kale on 2/20/18
 *
 */
public class LoginController {
    @FXML TextField email;
    @FXML private TextField password;
    @FXML private Button loginButton;
    @FXML private Button forgotPasswordButton;
    @FXML private Text errorLabel;

    private LoginManager _manager;

    void initManager(final LoginManager loginManager) {
        _manager = loginManager;

        loginButton.setOnAction(event -> _manager.login(email.getText(), password.getText()));
        forgotPasswordButton.setOnAction(event -> {
            try {
                Desktop.getDesktop().browse(new URI("")); // TODO: Put forgot password link here
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        });
    }

    void setErrorLabel(String error) {
        errorLabel.setText(error);
    }

    void disableButtons() {
        loginButton.setDisable(true);
        forgotPasswordButton.setDisable(true);
    }

    void enableButtons() {
        loginButton.setDisable(false);
        forgotPasswordButton.setDisable(false);
    }
}
