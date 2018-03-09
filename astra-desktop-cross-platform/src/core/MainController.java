package core;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.text.Text;

import java.awt.*;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;


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
    @FXML Text deviceName;

    @FXML Text projectNameOne;
    @FXML Text projectCreditsOne;
    @FXML private Button seeDetailsOne;

    @FXML Text projectNameTwo;
    @FXML Text projectCreditsTwo;
    @FXML private Button seeDetailsTwo;

    @FXML private Button goToManagerButton;

    private MainManager _manager;

    public void initialize() {}

    public void initManager(final MainManager manager) {
        _manager = manager;
        errorMessages.setText("Everything is ok!");
        quitButton.setOnAction(event -> _manager.quit());
        logoutButton.setOnAction(event -> _manager.logout());

        List<String[]> projectData =  (new BoincClient()).getProjectsURLCredits(
                Tests.getData("/Users/sohamkale/Documents/Astra/astra-desktop-cross-platform/project_status.txt"));

        projectNameOne.setText(projectData.get(0)[0]);
        projectCreditsOne.setText(projectData.get(0)[2] + " credits");
        projectNameTwo.setText(projectData.get(1)[0]);
        projectCreditsTwo.setText(projectData.get(1)[2] + " credits");

        seeDetailsOne.setOnAction(event -> {
            try {
                Desktop.getDesktop().browse(new URI(projectData.get(0)[1]));
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        });

        seeDetailsTwo.setOnAction(event -> {
            try {
                Desktop.getDesktop().browse(new URI(projectData.get(1)[1]));
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        });

        goToManagerButton.setOnAction(event -> {
            try {
                Desktop.getDesktop().browse(new URI("")); // TODO: Set URL of Astra dashboard - no login needed!
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        });
    }

    void setErrorMessages(String error) {
        errorMessages.setText(error);
    }
}
