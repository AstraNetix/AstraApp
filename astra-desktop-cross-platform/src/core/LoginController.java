package core;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;
import javafx.scene.text.Text;
import javafx.scene.Cursor;

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
    @FXML ImageView logoImage;
    @FXML TextField email;
    @FXML private TextField password;
    @FXML private Button loginButton;
    @FXML private Button forgotPasswordButton;
    @FXML private Text errorLabel;

    private LoginManager _manager;

    void initManager(final LoginManager loginManager) {
        _manager = loginManager;

        Utils.setupButton(loginButton, event -> _manager.login(email.getText(), password.getText()), _manager);
        Utils.setupButton(forgotPasswordButton, event -> {
            try {
                Desktop.getDesktop().browse(new URI("")); // TODO: Put forgot password link here
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        }, _manager);
    }

    void setErrorLabel(String error) {
        errorLabel.setText(error);
    }

    String getErrorLabel() { return errorLabel.getText(); }

    void disableButtons() {
        loginButton.setDisable(true);
        forgotPasswordButton.setDisable(true);
    }

    void enableButtons() {
        loginButton.setDisable(false);
        forgotPasswordButton.setDisable(false);
    }
}
