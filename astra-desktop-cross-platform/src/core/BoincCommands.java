package core;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * A command interface for the boincmmd tool with basic utilities to be exposed to user.
 * Created by Soham Kale on 2/20/18
 *
 */
public class BoincCommands {

    static Thread startBoinc() {
        Thread boinc = new Thread(() -> {
            BashClient.bashPersist("./boinc -insecure");
        });
        boinc.start();
        return boinc;
    }


    /* ****************************** GLOBAL PREFERENCES ****************************** */

    static void setRunOnBatteries(boolean opt) {
        XMLController.editTag("run_on_batteries", opt ? "1" : "0");
        globalPrefsOverride();
    }

    static void setRunIfActive(boolean opt) {
        XMLController.editTag("run_if_user_active", opt ? "1" : "0");
        globalPrefsOverride();
    }

    static void setConfigHours(int startHour, int endHour) {
        XMLController.editTag("start_hour", Integer.toString(startHour));
        XMLController.editTag("end_hour", Integer.toString(endHour));
        globalPrefsOverride();
    }

    static void setMaxCPUs(int max) {
        XMLController.editTag("max_cpus", Integer.toString(max));
        globalPrefsOverride();
    }

    static void setDiskMaxPercent(int percent) {
        XMLController.editTag("disk_max_used_pct", Integer.toString(percent));
        globalPrefsOverride();
    }

    static void setRAMMaxUse(int percent) {
        boolean dummyVar = XMLController.getTag("run_if_user_active").equals("1") ?
                XMLController.editTag("ram_max_used_busy_pct", Integer.toString(percent)) :
                XMLController.editTag("ram_max_used_idle_pct", Integer.toString(percent));
        globalPrefsOverride();
    }

    static void setCPUUsage(int percent) {
        XMLController.editTag("cpu_usage_limit", Integer.toString(percent));
        globalPrefsOverride();
    }



    static String getRunIfActive(boolean opt) {
        return XMLController.getTag("run_if_user_active");
    }

    static String[] getConfigHours(int startHour, int endHour) {
        return new String[] {XMLController.getTag("start_hour"), XMLController.getTag("end_hour")};
    }

    static String getMaxCPUs(int max) {
        return XMLController.getTag("max_cpus");
    }

    static String getDiskMaxPercent(int percent) {
        return XMLController.getTag("disk_max_used_pct");
    }

    static String getRAMMaxUse(int percent) {
        return XMLController.getTag("run_if_user_active").equals("1") ?
                XMLController.getTag("ram_max_used_busy_pct") :
                XMLController.getTag("ram_max_used_idle_pct");
    }

    static String getCPUUsage(int percent) {
        return XMLController.getTag("cpu_usage_limit");
    }


    /* *********************************** BOINCCMD *********************************** */

    static String[] lookupAccount(String url, String email, String password) {
        return execCmnd("--lookup_account", url, email, password);
    }

    static String[] createUser(String url, String email, String password, String name)  {
        return execCmnd("--create_account", url, email, password, name);
    }

    static String[] attachProject(String url, String accountKey)  {
        return execCmnd("--project_attach", url, accountKey);
    }


    static String[] getCCStatus()  { return execCmnd("--get_cc_status"); }

    static String[] getState()  { return execCmnd("--get_state"); }

    static String[] getTasks()  { return execCmnd("--get_tasks"); }

    static String[] getProjectStatus()  {
        return execCmnd("--get_project_status");
    }

    static String[] getDiskUsage()  { return execCmnd("--get_disk_usage"); }


    static String[] resetProject(String url)  { return execCmnd("--project", url, "reset"); }

    static String[] detachProject(String url)  { return execCmnd("--project", url, "detach"); }

    static String[] suspendProject(String url)  { return execCmnd("--project", url, "suspend"); }

    static String[] resumeProject(String url)  { return execCmnd("--project", url, "resume"); }

    static String[] noMoreWorkProject(String url)  { return execCmnd("--project", url, "nomorework"); }


    static String[] runBenchmarks()  { return execCmnd("--run_benchmarks"); }


    static String[] setCPU(String setting, int... duration)  {
        return execCmnd("--set_run_mode", setting, (duration == null) ? "" : String.valueOf(duration[0]));
    }

    static String[] setGPU(String setting, int... duration)  {
        return execCmnd("--set_gpu_mode", setting, (duration == null) ? "" : String.valueOf(duration[0]));
    }

    static String[] setNetwork(String setting, int... duration)  {
        return execCmnd("--set_gpu_mode", setting, (duration == null) ? "" : String.valueOf(duration[0]));
    }


    static String[] quit()  { return execCmnd("--quit"); }

    private static String[] globalPrefsOverride()  { return execCmnd("--read_global_prefs_override"); }


    private static String[] execCmnd(String... args) {
        String[] boincArgs = new String[args.length + 1];
        System.arraycopy(args, 0, boincArgs, 1, args.length);
        boincArgs[0] = "./boinccmd";
        return BashClient.bash(boincArgs);
    }

}
