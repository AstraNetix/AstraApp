//
//  LoginViewController.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/11/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Cocoa

class LoginViewController: NSViewController, PubNubLoginDelegate {
    
    var launchedBefore: Bool?
    var user: User?
    
    weak var client: PubNubClient?
    
    @IBOutlet weak var email: NSTextField!
    @IBOutlet weak var password: NSSecureTextField!
    @IBOutlet weak var loginLoading: NSProgressIndicator!
    @IBOutlet weak var errorLabel: NSTextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.launchedBefore = UserDefaults.standard(forKey: "launchedBefore")
        user = self.launchedBefore! ? User.loadUser() : nil
        
        self.client = PubNubClient(user: user, delegate: self)
        self.errorLabel.stringValue = ""
    }
    
    func loginSuccess(firstName: String, lastName: String) {
        self.loginLoading.stopAnimation(self)
        self.errorLabel.stringValue = ""
        
        if self.launchedBefore == nil {
            self.user = User(firstName: firstName, lastName: lastName, email: self.email.stringValue)
            UserDefaults.standard.set(true, forKey: "launchedBefore")
            self.client?.publish(message: [
                "status" : "create",
                "user-email" : user?.email ?? "None",
                "name" : user?.deviceName ?? "None",
                "company" : "Apple",
                "model" : "" // TODO: Find out how to get device model
            ])
            // TODO: Do something with this user to perpetuate it
        }
        
        AstraViewController.freshController()
        dismissViewController(self)
    }
    
    func invalidCredentials() {
        self.loginLoading.stopAnimation(self)
        self.errorLabel.stringValue = "Incorrect email or password"
    }
    
    @IBAction func loginPressed(_ sender: Any) {
        self.errorLabel.stringValue = ""
        loginLoading.startAnimation(self)

        self.client?.publish(message: [
            "status": "login",
            "id": user!.deviceID,
            "email": self.email.stringValue,
            "password": self.password.stringValue,
        ])
        // To get messages of successful login or not from API
        self.client?.loginSubscribe(email: self.email.stringValue)
    }
    
    func publishError() {
        loginLoading.stopAnimation(self)
        self.errorLabel.stringValue = "There was a problem connecting to our servers. Please try again"
    }
    
    func accessDenied() {
        self.errorLabel.stringValue = "There was a problem connecting to our servers. We are trying to connect..."
    }
    
    func unexpectedDisconnect() {
        self.errorLabel.stringValue = "There was a problem connecting to our servers. We are trying to connect..."
    }
    
    func publishSuccess() { /* Do nothing */ }
    
    func heartbeatFailure() {
        /** I dont fuckkng nkw what this is */
    }
}
