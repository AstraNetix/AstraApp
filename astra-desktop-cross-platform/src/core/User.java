package core;

import java.io.File;
import java.io.Serializable;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
        _accountKeys = new HashMap<>();
        _passwords = new HashMap<>();
        _deviceName = getComputerName();
        _deviceID = User.hash(_deviceName, email);
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

    String getAccountKey(String url) {
        return _accountKeys.get(url);
    }

    void addAccountKey(String url, String accountKey) { _accountKeys.put(url, accountKey); }


    String name() {
        return _firstName + " " + _lastName;
    }


    private static String hash(String deviceName, String email) {
        return Utils.sha1(
                deviceName,
                // TODO: Find out how to get company and model name */
                email);
    }

    private String getComputerName() {
        Map<String, String> env = System.getenv();
        if (env.containsKey("COMPUTERNAME"))
            return env.get("COMPUTERNAME");
        else if (env.containsKey("HOSTNAME"))
            return env.get("HOSTNAME");
        else if (env.containsKey("SESSION_MANAGER")) {
            // TODO: test this on Ubuntu somehow
            String input = env.get("SESSION_MANAGER");
            Pattern pattern = Pattern.compile("(?<=local/).*(?=:@)");
            Matcher matcher = pattern.matcher(input);
            return matcher.find() ? input.substring(matcher.start(), matcher.end()) : "";
        } else {
            return "Unknown Computer";
        }
    }

    void save() {
        Utils.writeObject(new File("./user_data.txt"), this);
    }

    static User load() {
        return Utils.readObject(new File("./user_data.txt"), User.class);
    }


    String _firstName, _lastName, _email, _deviceName, _company, _model, _deviceID;
    private Map<String, String> _passwords, _accountKeys; /* [project url] -> [password | account key] */
}
