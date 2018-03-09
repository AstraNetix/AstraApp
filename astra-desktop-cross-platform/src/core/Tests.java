package core;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;


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

    static void testBoinc() {
        Thread boinc = new Thread(() -> {
            BashClient.bashPersist("./boinc -insecure");
        });
        boinc.start();
        BoincCommands.runBenchmarks();
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

    public static void main(String... args) {
        testParseCreateAccount();
    }
}
