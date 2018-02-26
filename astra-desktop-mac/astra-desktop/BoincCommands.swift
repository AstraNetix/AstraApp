//
//  BoincCommands.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/10/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Foundation

enum BoincCommands {
    
    static func lookupAccount(url: String, email: String, password: String) -> String { return self.exec_cmnd(args: ["--lookup_account", url, email, password]) }
    
            
    static func createUser(url: String, email: String, password: String, name: String) -> String { return self.exec_cmnd(args: ["--create_account", url, email, password, name]) }
    
    static func attachProject(url: String, accountKey: String) -> String { return self.exec_cmnd(args: ["--project_attach", url, accountKey]) }
    
    
    static func getCCStatus() -> String { return self.exec_cmnd(args: ["--get_cc_status"]) }
    
    static func getState() -> String { return self.exec_cmnd(args: ["--get_state"]) }
    
    static func getTasks() -> String { return self.exec_cmnd(args: ["--get_tasks"]) }
    
    static func getProjectStatus() -> String { return self.exec_cmnd(args: ["--get_project_status"]) }
    
    static func getDiskUsage() -> String { return self.exec_cmnd(args: ["--get_disk_usage"]) }
    
    
    static func resetProject(url: String) -> String { return self.exec_cmnd(args: ["--project", url, "reset"]) }
    
    static func detachProject(url: String) -> String { return self.exec_cmnd(args: ["--project", url, "detach"]) }
    
    static func suspendProject(url: String) -> String { return self.exec_cmnd(args: ["--project", url, "suspend"]) }
    
    static func resumeProject(url: String) -> String { return self.exec_cmnd(args: ["--project", url, "resume"]) }
    
    static func noMoreWorkProject(url: String) -> String { return self.exec_cmnd(args: ["--project", url, "nomorework"]) }
    
    
    static func alwaysCPU(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_run_mode", "always", (duration == nil) ? "" : String(describing: duration)]) }
    
    static func autoCPU(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_run_mode", "auto", (duration == nil) ? "" : String(describing: duration)]) }
    
    static func neverCPU(duration: Int?) -> String {
        return self.exec_cmnd(args: ["--set_run_mode", "never", (duration == nil) ? "" : String(describing: duration)])
    }
    
    
    static func alwaysGPU(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_gpu_mode", "always", (duration == nil) ? "" : String(describing: duration)]) }
    
    static func autoGPU(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_gpu_mode", "auto", (duration == nil) ? "" : String(describing: duration)]) }
    
    static func neverGPU(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_gpu_mode", "never", (duration == nil) ? "" : String(describing: duration)]) }
    
    
    static func alwaysNetwork(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_gpu_mode", "always", (duration == nil) ? "" : String(describing: duration)]) }
    
    static func autoNetwork(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_gpu_mode", "auto", (duration == nil) ? "" : String(describing: duration)]) }
    
    static func neverNetwork(duration: Int?) -> String { return self.exec_cmnd(args: ["--set_gpu_mode", "never", (duration == nil) ? "" : String(describing: duration)]) }
    
    
    static func quit() -> String { return self.exec_cmnd(args: ["--quit"]) }

}

extension BoincCommands {
    static func exec_cmnd(args: [String]) -> String {
        return BashController.bash(command: "Boinc/boinccmd", arguments: args)
    }
}
