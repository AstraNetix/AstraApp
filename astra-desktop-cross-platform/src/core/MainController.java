package core;

import javafx.animation.RotateTransition;
import javafx.fxml.FXML;
import javafx.scene.Cursor;
import javafx.scene.control.Button;
import javafx.scene.image.ImageView;
import javafx.scene.text.Text;
import javafx.util.Duration;

import javafx.scene.image.Image;
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
    @FXML private Button astraButton;

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

        Image astraLogoImage = new Image(
                "file:../../Astra-Logo@3x.png",
                30,
                0,
                true,
                true);
        ImageView astraLogo = new ImageView(astraLogoImage);
        RotateTransition rotate = new RotateTransition(Duration.seconds(2), astraLogo);
        rotate.setByAngle(360);

        astraButton.setGraphic(astraLogo);
        astraButton.setOnMouseEntered(event -> {
            rotate.play();
            _manager._scene.setCursor(Cursor.HAND);
        });
        astraButton.setOnMouseExited(event -> {
            rotate.pause();
            manager._scene.setCursor(Cursor.DEFAULT);
        });
        astraButton.setOnAction(event -> {
            try {
                Desktop.getDesktop().browse(new URI("")); // TODO: Add Astra homepage
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        });


        errorMessages.setText("Everything is ok!");

        Utils.setupButton(quitButton, event -> _manager.quit(), _manager);
        Utils.setupButton(logoutButton, event -> _manager.logout(), _manager);

        List<String[]> projectData =  (new BoincClient()).getProjectsURLCredits(
                Tests.getData("/Users/sohamkale/Documents/Astra/astra-desktop-cross-platform/project_status.txt"));

        projectNameOne.setText(projectData.get(0)[0]);
        projectCreditsOne.setText(projectData.get(0)[2] + " credits");
        projectNameTwo.setText(projectData.get(1)[0]);
        projectCreditsTwo.setText(projectData.get(1)[2] + " credits");

        Utils.setupButton(seeDetailsOne, event -> {
            try {
                Desktop.getDesktop().browse(new URI(projectData.get(0)[1]));
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        }, _manager);

        Utils.setupButton(seeDetailsTwo, event -> {
            try {
                Desktop.getDesktop().browse(new URI(projectData.get(1)[1]));
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        }, _manager);

        Utils.setupButton(seeDetailsTwo, event -> {
            try {
                Desktop.getDesktop().browse(new URI("")); // TODO: Set URL of Astra dashboard - no login needed!
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }
        }, _manager);

    }

    void setErrorMessages(String error) {
        errorMessages.setText(error);
    }
}
