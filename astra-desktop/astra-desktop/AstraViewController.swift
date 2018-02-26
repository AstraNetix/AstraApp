//
//  AstraViewController.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/16/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Cocoa

import Cocoa

class AstraViewController: NSViewController, PubNubPersistDelegate {
    @IBOutlet var textLabel: NSTextField!
    
    var user: User?
    weak var client: PubNubClient?
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}

extension AstraViewController {
    // MARK: Storyboard instantiation
    static func freshController() -> AstraViewController {
        let storyboard = NSStoryboard(name: NSStoryboard.Name(rawValue: "Main"), bundle: nil)
        let identifier = NSStoryboard.SceneIdentifier(rawValue: "AstraViewController")
        guard let viewcontroller = storyboard.instantiateController(withIdentifier: identifier) as? AstraViewController else {
            fatalError("Why cant I find AstraViewController? - Check Main.storyboard")
        }
        return viewcontroller
    }
}

extension AstraViewController {
    func publishSuccess() {
        /* Do nothing */
    }
    
    func publishError() {
        
    }
    
    func unexpectedDisconnect() {
        
    }
    
    func accessDenied() {
        
    }
    
    func heartbeatFailure() {
        
    }
    
    func quitClient() {
        client?.publish(message: [
            "status" : "update",
            "function" : "inactive"
        ])
    }
    
}

