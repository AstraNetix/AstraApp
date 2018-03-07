package core;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.text.Text;



/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Basic object container for main screen.
 * Created by Soham Kale on 2/20/18
 *
 */
public class MainController {
    @FXML private Text errorMessages;
    @FXML private Button quitButton;
    @FXML private Button logoutButton;

    private MainManager _manager;

    public void initialize() {}

    public void initManager(final MainManager manager) {
        _manager = manager;
        errorMessages.setText("Everything is ok!");
        quitButton.setOnAction(event -> Platform.exit());
        logoutButton.setOnAction(event -> manager.logout());
    }

    void setErrorMessages(String error) {
        errorMessages.setText(error);
    }
}
