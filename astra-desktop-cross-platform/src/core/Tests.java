package core;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;

import static java.util.Collections.singletonList;


/**
 * /**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * A testing module for desktop client and BOINC calls.
 * Created by Soham Kale on 2/20/18
 *
 */
public class Tests {

    static void testCL() {
        Arrays.asList(BashClient.bash("ls")).forEach(System.out::println);
    }

    static void testBoinc() {
        BoincCommands.startBoinc();
        TimerTask task = new TimerTask() {
            @Override
            public void run() {
                System.out.println("Starting data drop...");
                Arrays.asList(BoincCommands.getDiskUsage()).forEach(System.out::println);
            }
        };
        Timer timer = new Timer();
        timer.schedule(task, 4000L);
    }

    static String[] getData(String path) {
        List<String> output = new ArrayList<>();
        try (Stream<String> stream = Files.lines(Paths.get(path))) {
            stream.forEach(output::add);
        } catch (IOException io) {
            io.printStackTrace();
        }
        return output.toArray(new String[output.size()]);
    }

    static void testProjectsAndURLs() {
        BoincClient _client = new BoincClient();
        List<String[]> result = _client.getProjectsAndURLs(
                getData("/Users/sohamkale/Documents/Astra/astra-desktop-cross-platform/project_status.txt"));
        System.out.println(result.get(1)[1]);
    }

    static void testProjectInfo() {
        BoincClient _client = new BoincClient();
        Map<String, String> result = _client.getProjectInfo("http://setiathome.berkeley.edu/",
                getData("/Users/sohamkale/Documents/Astra/astra-desktop-cross-platform/project_status.txt"));
        System.out.println(result);
    }

    static void testParseCreateAccount() {
        BoincClient _client = new BoincClient();
        System.out.println(_client.parseCreateAccount(
                getData("/Users/sohamkale/Documents/Astra/astra-desktop-cross-platform/create_account.txt")));
    }

    static void testSingletonList() {
        User _user = User.load();
        System.out.println(new ArrayList<>(singletonList(_user._email)));
    }

    static void testDeviceCreatePubNub() {
        PubNubClient _pubnub = new PubNubClient(new FakePNDelegate());
        User _user = User.load();
        // _pubnub.setUser(_user);
        _pubnub.publish(new HashMap<String, String>() {{
            put("status", "create");
            put("email", _user._email);
            put("name", _user._deviceName);
            put("company", _user._company);
            put("model", _user._model);
        }});
    }

    private static class FakePNDelegate implements PubNubClient.PubNubDelegate {
        public void publishSuccess() {
            System.out.println("Publish Success");
        }
        public void publishError(int errorCode) {
            System.out.println("Publish Error");
        }
        public void unexpectedDisconnect() {
            System.out.println("Unexpected Disconnect");
        }
        public void accessDenied() {
            System.out.println("Access Denied");
        }
        public void heartbeatFailure() {
            System.out.println("Heartbeat Failure");
        }
    }


    public static void main(String... args) {
        testBoinc();
    }

}
