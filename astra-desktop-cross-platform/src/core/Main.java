package core;

import javafx.application.Application;

import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage stage) throws Exception{
        Scene scene = new Scene(new StackPane());
        LoginManager loginManager = new LoginManager(scene);
        loginManager.showScreen();

        stage.setTitle("Astra Desktop");

        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();

        // TODO if your clearing todos right now, get rid of all .printStackTrace()s
    }

    public static void quit(User user) {
        user.save();
        BoincCommands.quit();
        Platform.exit();
        System.exit(0);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
