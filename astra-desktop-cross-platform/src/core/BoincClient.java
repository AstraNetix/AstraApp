package core;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * A client for doing BOINC operations.
 * Created by Soham Kale on 2/20/18
 *
 */
public class BoincClient {

    BoincClient(User... user) {
        if (user.length > 0)_user = user[0];
    }

    void setUser(User user) { _user = user; }

    /* ************************************* DISC ************************************* */

    Map<String, Map<String, String>> getTotalDiskUsage() {
        String[] diskUsage = BoincCommands.getDiskUsage();
        Map<String, Map<String, String>> data = new HashMap<String, Map<String, String>>() {{
            put("total", new HashMap<String, String>() {{
                put("value", getDataKnown(diskUsage[1], Line.TOTAL));
            }});
            put("free", new HashMap<String, String>() {{
                put("value", getDataKnown(diskUsage[2], Line.FREE));
            }});
        }};
        int projNum = 0;
        for (int i = 0; i < diskUsage.length; i++) {
            if (diskUsage[i].matches(Line.NUMBER._header)) {
                data.put(Integer.toString(projNum), (getDiskUsage(diskUsage, i + 1)));
                i += 3;
            }
        }
        return data;
    }

    Map<String, String> getDiskUsage(String projectURL) {
        String[] diskUsage = BoincCommands.getDiskUsage();
        for (int i = 0; i < diskUsage.length; i++) {
            if (diskUsage[i].matches(Line.NUMBER._header) &&
                    getDataKnown(diskUsage[i + 1], Line.URL).equals(projectURL)) {
                return getDiskUsage(diskUsage, i + 1);
            }
        }
        return new HashMap<String, String>() {{
            put("error", "No such project");
        }};
    }

    private Map<String, String> getDiskUsage(String[] diskUsage, int i) {
        return new HashMap<String, String>() {{
            put("url", getDataKnown(diskUsage[i], Line.URL));
            put("disk-usage", getDataKnown(diskUsage[i + 1], Line.DISK_USAGE));
        }};
    }

    /* *********************************** PROJECTS *********************************** */

    /** Returns all relevant project info and status from its URL.
     *
     * @param projectURL The URL of the project
     * @return Map of info type (String) to info data (String)
     */
    Map<String, String> getProjectInfo(String projectURL, String[] projectStatus) {
        // String[] projectStatus = BoincCommands.getProjectStatus();  // TODO: Uncomment this
        Pattern header = Pattern.compile(Line.NUMBER._header);
        for (int i = 1; i < projectStatus.length; i++) {
            if (header.matcher(projectStatus[i]).find()) {
                if (getDataKnown(projectStatus[i+2], Line.URL).equals(projectURL))
                    return getProjectInfo(i, projectStatus);
                i += 23;
            }
        }
        return new HashMap<String, String>() {{
            put("error", "No such project");
        }};
    }

    List<String[]> getProjectsAndURLs(String[] projectStatus) {
        // String[] projectStatus = BoincCommands.getProjectStatus(); // TODO: Uncomment this
        Pattern header = Pattern.compile(Line.NUMBER._header);
        List<String[]> projects = new ArrayList<>();
        for (int i = 1; i < projectStatus.length; i++) {
            if (header.matcher(projectStatus[i]).find()) {
                projects.add(new String[] {
                        getDataKnown(projectStatus[i+1], Line.NAME),
                        getDataKnown(projectStatus[i+2], Line.URL)
                });
                i += 23;
            }
        }
        return projects;
    }

    List<String[]> getProjectsURLCredits(String[] projectStatus) {
        // String[] projectStatus = BoincCommands.getProjectStatus();
        Pattern header = Pattern.compile(Line.NUMBER._header);
        List<String[]> projects = new ArrayList<>();
        for (int i = 1; i < projectStatus.length; i++) {
            if (header.matcher(projectStatus[i]).find()) {
                projects.add(new String[] {
                        getDataKnown(projectStatus[i+1], Line.NAME),
                        getDataKnown(projectStatus[i+2], Line.URL),
                        getDataKnown(projectStatus[i+6], Line.USER_TOTAL_CREDIT)
                });
                i += 23;
            }
        }
        return projects;
    }


    /** Starts a project by inputting user information and a randomized password
     *
     * @param projectURL URL for the project to start
     */
    Map<String, String> startProject(String projectURL) {
        String accountKey = _user.getAccountKey(projectURL);
        if (_user.getPassword(projectURL) == null) {
            String password = UUID.randomUUID().toString();
            _user.addPassword(projectURL, password);
            String[] output = BoincCommands.createUser(projectURL, _user._email, password, _user.name());

            if ((accountKey = parseCreateAccount(output)) != null) {
                _user.addAccountKey(projectURL, accountKey);
            } else {
                return new HashMap<String, String>() {{
                    put("failure", String.format("Unable to start project at %s", projectURL));
                }};
            }
        }
        BoincCommands.attachProject(projectURL, accountKey);
        return new HashMap<String, String>() {{
            put("success", String.format("Project at %s successfully started", projectURL));
        }};
    }

    String parseCreateAccount(String[] input) { // TODO make private later
        Pattern status = Pattern.compile(Line.STATUS._data);
        Matcher matcher = status.matcher(input[0]);
        if (!matcher.find() ||
                !input[0].substring(matcher.start(), matcher.end()).equals("Success"))
            return null;
        Pattern accountKey = Pattern.compile(Line.ACCOUNT_KEY._data);
        for (String line : input) {
            matcher = accountKey.matcher(line);
            if (matcher.find()) {
                return line.substring(matcher.start(), matcher.end());
            }
        }
        return null;
    }

    private Map<String, String> getProjectInfo(int ind, String[] projectStatus) {
        Map<String, String> projectData = new HashMap<>();
        int[] indices = new int[] {1, 2, 3, 6, 7, 16, 18, 19, 22};
        Line[] values = Line.values();
        for (int i = 0; i < indices.length - 2; i++) {
            projectData.put(values[i + 2].toString().toLowerCase(),
                    getDataKnown(projectStatus[ind + indices[i]], values[i + 2]));
        }
        return projectData;
    }


    /* *********************************** UTILITIES *********************************** */

    private String getDataUnknown(String input) {
        for (Line dataType: Line.values()) {
            Pattern header = Pattern.compile(dataType._header);
            if ((header.matcher(dataType._header)).find()) {
                Pattern data = Pattern.compile(dataType._data);
                Matcher matcher = data.matcher(input);
                if (matcher.find()) { return input.substring(matcher.start(), matcher.end()); }
            }
        }
        return null;
    }

    private String getDataKnown(String input, Line line) {
        Pattern pattern = Pattern.compile(line._data);
        Matcher matcher = pattern.matcher(input);
        return matcher.find() ? input.substring(matcher.start(), matcher.end()) : "";
    }


    /* ********************************** DECLARATIONS ********************************** */

    private enum Line {
        HEADER("========\\s\\S+\\s========", "[a-zA-Z0-9]+"),
        NUMBER("\\)\\s-----------", "\\d+"),
        NAME("name:\\s", "(?<=name:\\s).+"),
        URL("master\\sURL:\\s", "(?<=master\\sURL:\\s).+"),
        USER_NAME("user_name:\\s", "(?<=user_name:\\s).+"),
        USER_TOTAL_CREDIT("user_total_credit:\\s", "\\d\\.\\d{6}"),
        USER_AVG_CREDIT("user_expavg_credit:\\s", "\\d\\.\\d{6}"),
        ENDED("ended:\\s", "(yes|no)"),
        NO_MORE_WORK("don't request more work:\\s", "(yes|no)"),
        DISK_USAGE("disk\\susage:\\s", "(\\d\\.\\d{6}|\\d*\\.\\d{2}MB)"),
        PROJECT_FILES_DOWNLOADED("project\\sfiles\\sdownloaded:\\s", "\\d\\.\\d{6}"),

        TOTAL("total:\\s", "\\d+\\.\\d+"),
        FREE("free:\\s", "\\d+\\.\\d+"),

        STATUS("status\\s", "(Success|Failure)"),
        ACCOUNT_KEY("account key:\\s", "(?<=account key:\\s).+");


        Line(String header, String data) {
            _header = header;
            _data = data;
        }

        private String _header;
        private String _data;
    }

    private User _user;
}
