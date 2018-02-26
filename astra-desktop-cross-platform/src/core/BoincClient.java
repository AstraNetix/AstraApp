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
                    getDataKnown(diskUsage[i + 1], Line.MASTER_URL).equals(projectURL)) {
                return getDiskUsage(diskUsage, i + 1);
            }
        }
        return new HashMap<String, String>() {{
            put("error", "No such project");
        }};
    }

    private Map<String, String> getDiskUsage(String[] diskUsage, int i) {
        return new HashMap<String, String>() {{
            put("url", getDataKnown(diskUsage[i], Line.MASTER_URL));
            put("disk-usage", getDataKnown(diskUsage[i + 1], Line.DISK_USAGE));
        }};
    }

    /* *********************************** PROJECTS *********************************** */

    /** Returns all relevant project info and status.
     *
     * @param projectURL The URL of the project
     * @return Map of info type (String) to info data (String)
     */
    Map<String, String> getProjectInfo(String projectURL) {
        String[] projectStatus = BoincCommands.getProjectStatus();
        for (int i = 1; i < projectStatus.length; i++) {
            if (projectStatus[i].matches(Line.NUMBER._header)) {
                if (getDataKnown(projectStatus[i+2], Line.MASTER_URL).equals(projectURL))
                    return getProjectInfo(i, projectStatus);
                i += 23;
            }
        }
        return new HashMap<String, String>() {{
            put("error", "No such project");
        }};
    }


    /** Starts a project by inputting user information and a randomized password
     *
     * @param projectURL URL for the project to start
     */
    void startProject(String projectURL) {
        if (_user.getPassword(projectURL) == null) {
            String password = UUID.randomUUID().toString();
            _user.addPassword(projectURL, password);
            // TODO: Parse return for this and set up authenticator key.
            BoincCommands.createUser(projectURL, _user._email, UUID.randomUUID().toString(), _user.name());
        }
        BoincCommands.attachProject(projectURL, "" /** Use authenticator key here */);

    }

    private Map<String, String> getProjectInfo(int ind, String[] projectStatus) {
        Map<String, String> projectData = new HashMap<>();
        int[] indices = new int[] {1, 2, 3, 6, 7, 16, 18, 19, 21};
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
            if (input.matches(dataType._header)) {
                Pattern pattern = Pattern.compile(dataType._data);
                Matcher matcher = pattern.matcher(input);
                if (matcher.matches()) return matcher.group(1);
            }
        }
        return null;
    }

    private String getDataKnown(String input, Line line) {
        Pattern pattern = Pattern.compile(line._data);
        Matcher matcher = pattern.matcher(input);
        if (matcher.matches())
            return matcher.group(1);
        return "";
    }


    /* ********************************** DECLARATIONS ********************************** */

    private enum Line {
        HEADER("========\\s\\S+\\s========", "[a-zA-Z0-9]+"),
        NUMBER("\\)\\s-----------", "\\d)"),
        NAME("name:\\s", "\\S+"),
        MASTER_URL("master\\sURL:\\s", "\\S+"),
        USER_NAME("user_name:\\s", "\\S+"),
        USER_TOTAL_CREDIT("user_total_credit:\\s", "\\d\\.\\d{6}"),
        USER_AVG_CREDIT("user_expavg_credit:\\s", "\\d\\.\\d{6}"),
        ENDED("ended:\\s", "[yes|no]"),
        NO_MORE_WORK("don't request more work:\\s", "[yes|no]"),
        DISK_USAGE("disk usage:\\s", "[\\d\\.\\d{6}|\\d*\\.\\d{2}MB]"),
        PROJECT_FILES_DOWNLOADED("project\\sfiles\\sdownloaded:\\s", "\\d\\.\\d{6}"),

        TOTAL("total:\\s", "\\d+\\.\\d+"),
        FREE("free:\\s", "\\d+\\.\\d+");


        Line(String header, String data) {
            _header = header;
            _data = data;
        }

        private String _header;
        private String _data;
    }

    private User _user;
}
