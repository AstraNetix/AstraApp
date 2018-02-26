//
//  PubNubClient.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/10/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Foundation
import PubNub

protocol PubNubDelegate: class {
    func publishSuccess()
    func publishError()
    func unexpectedDisconnect()
    func accessDenied()
    func heartbeatFailure()
}

protocol PubNubLoginDelegate: PubNubDelegate {
    func loginSuccess(firstName: String, lastName: String)
    func invalidCredentials()
}

protocol PubNubPersistDelegate: PubNubDelegate {
    func quitClient()
}

class PubNubClient: NSObject, PNObjectEventListener {
    var client: PubNub!
    var user: User?
    var email: String?
    weak var delegate: PubNubDelegate?
    
    let numServerCores = 8
    
    init(user: User?, delegate: PubNubDelegate?) {
        super.init()
        self.user = user!
        self.delegate = delegate
        
        let configuration = PNConfiguration(
            publishKey: "pub-c-79775796-e891-4ba0-8e96-af4a5dd71beb",
            subscribeKey: "sub-c-d5c0f6b8-f436-11e7-b8a6-46d99af2bb8c"
        )
        self.client = PubNub.clientWithConfiguration(configuration)
        self.client.addListener(self)
        
        self.client.subscribeToChannels([String(describing: user?.deviceID)], withPresence: true)
    }
    
    func publish(message: [String: Any]) {
        self.client.publish(message, toChannel: self.getPubChannel(), compressed: false, withCompletion: { (status) in
            if status.isError && self.delegate != nil {
                self.delegate?.publishError()
            } else if self.delegate != nil {
                self.delegate?.publishSuccess()
            }
        })
    }
    
    func client(_ client: PubNub, didReceiveMessage message: PNMessageResult) {
        let message = message.data.message as! [String: String]
        switch message["function"] {
        case "login-success"?:
            self.client.unsubscribeFromChannels([self.email!], withPresence: false)
            delegate?.loginSuccess(firstName: message["first-name"]!, lastName: message["last-name"]!)
        case "invalid-credentials"?:
            self.client.unsubscribeFromChannels([self.email!], withPresence: false)
            delegate?.invalidCredentials()
        case "start-project"?:
            BoincCommands.createUser(url: message["url"]!, email: (self.email!), password: (user?.getPassword(url: message["url"]!))!, name: (user?.name())!)
            BoincCommands.attachProject(url: (message["url"])! , accountKey: (user?.authenticator)!)
            BoincCommands.lookupAccount(url: message["url"]!, email: (self.email!), password: (user?.passwords[message["url"]!])!) /* Get authentication id from here and attach to user */
        case "quit-project"?:
            BoincCommands.noMoreWorkProject(url: message["url"]!)
        case "project-status"?:
            publish(message: [BoincCommands.getProjectStatus(): "test"]) /* Find out how to convert from status to a dictionary */
        case "quit"?:
            BoincCommands.quit()
        default:
            publish(message: ["status": "unknown command"])
        }
    }
    
    func client(_ client: PubNub, didReceive status: PNStatus) {
        if status.operation == .subscribeOperation {
            if status.category == .PNUnexpectedDisconnectCategory {
                self.delegate?.unexpectedDisconnect()
            } else {
                let errorStatus: PNErrorStatus = status as! PNErrorStatus
                if errorStatus.category == .PNAccessDeniedCategory {
                    self.delegate?.accessDenied()
                }
            }
        } else if status.operation == .unsubscribeOperation {
            if status.category == .PNDisconnectedCategory {
                // Handle unsubscribing with no errors
            }
        } else if status.operation == .heartbeatOperation {
            if status.isError {
                self.delegate?.heartbeatFailure()
            }
        }
    }
    
    func loginSubscribe(email: String) {
        self.email = email
        self.client.subscribeToChannels([email], withPresence: false)
    }
    
    func getPubChannel() -> String {
        return (user != nil) ? String(self.user!.deviceID.truncatingRemainder(dividingBy: Double(self.numServerCores))) : "create"
    }
}

