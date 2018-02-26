package core;

import java.io.File;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Stores basic User information and handles its storage.
 * Created by Soham Kale on 2/20/18
 *
 */
public class User implements Serializable {

    User(String firstName, String lastName, String email) {
        _firstName = firstName;
        _lastName = lastName;
        _email = email;
        /** Get authenticator by BOINC command when initializing*/
        /** Get device name somehow */
        _deviceName = "test_device";
        _deviceID = User.hash(_deviceName, email);
        _passwords = new HashMap<>();
    }

    private static String hash(User user) {
        return User.hash(user._deviceName, user._email);
    }
    
    String getPassword(String url) {
        return _passwords.get(url);
    }

    void addPassword(String url, String password) {
        _passwords.put(url, password);
    }

    String name() {
        return _firstName + " " + _lastName;
    }

    private static String hash(String deviceName, String email) {
        return Utils.sha1(
                deviceName,
                /** Find out how to get company and model name */
                email);
    }

    void save() {
        Utils.writeObject(new File("./user_data.txt"), this);
    }

    static User load() {
        return Utils.readObject(new File("./user_data.txt"), User.class);
    }


    String _firstName, _lastName, _email, _deviceName, _company, _model, _deviceID;
    private String _authenticator;
    private Map<String, String> _passwords; /** [project url] -> [password] */
}
