//
//  User.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/11/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Foundation

class User : NSObject, NSCoding {
    let hashIndex = 9
    
    let firstName: String
    let lastName: String
    let email: String
    var authenticator: String?
    let deviceName: String
    let deviceID: Double
    var passwords: [String: String] // [project url] -> [password]
    
    init(firstName: String, lastName: String, email: String, authenticator: String?, deviceID: Double, deviceName: String, passwords: [String: String]?) {
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.authenticator = authenticator
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.passwords = passwords!
    }
    
    convenience init(firstName: String, lastName: String, email: String) {
        self.init(firstName: firstName,
                  lastName: lastName,
                  email: email,
                  authenticator: "", /* Make sure to get authenticator when initializing somehow */
                  deviceID: User.hashCode(email: email),
                  deviceName: (Host.current().localizedName)!,
                  passwords: [:])
    }
    
    func name() -> String {
        return self.firstName + self.lastName
    }
    
    func getPassword(url: String) -> String? {
        var password : String? = self.passwords[url]
        if password == nil {
            password = String(User.sha256(input: url))
            self.passwords[url] = password
        }
        return password!
    }
    
    static func hashCode(email: String) -> Double {
        return Double(
            User.sha256(input: (Host.current().localizedName)!) +
            User.sha256(input: "Apple") +
            User.sha256(input: "" /* TODO: Find out how to get device model */) +
            User.sha256(input: email)
        ).truncatingRemainder(dividingBy: 1e10)
    }
    
    static func sha256(input: String) -> Int {
        let data = input.data(using: .utf8)
        let transform = SecDigestTransformCreate(kSecDigestSHA2, 256, nil)
        SecTransformSetAttribute(transform, kSecTransformInputAttributeName, data as CFTypeRef, nil)
        return (SecTransformExecute(transform, nil) as! Data).toInt()
    }
    
    required convenience init?(coder decoder: NSCoder) {
        guard let firstName = decoder.decodeObject(forKey: "firstName") as! String?,
            let lastName = decoder.decodeObject(forKey: "lastName") as! String?,
            let email = decoder.decodeObject(forKey: "email") as! String?,
            let authenticator = decoder.decodeObject(forKey: "authenticator") as! String?,
            let passwords = decoder.decodeObject(forKey: "passwords") as! [String: String]?,
            let deviceName = decoder.decodeObject(forKey: "deviceName") as! String?,
            let deviceID = decoder.decodeObject(forKey: "deviceID") as! Double?
            else { return nil /* Handle decoding error */ }
        
        self.init(firstName: firstName, lastName: lastName, email: email, authenticator: authenticator, deviceID: deviceID, deviceName: deviceName, passwords: passwords)
    }
    
    func encode(with coder: NSCoder) {
        coder.encode(self.firstName, forKey: "firstName")
        coder.encode(self.lastName, forKey: "lastName")
        coder.encode(self.email, forKey: "email")
        coder.encode(self.authenticator, forKey: "authenticator")
        coder.encode(self.deviceName, forKey: "deviceName")
        coder.encode(self.deviceID, forKey: "deviceID")
        coder.encode(self.passwords, forKey: "passwords")
    }
    
    func save() {
        let savedData = NSKeyedArchiver.archivedData(withRootObject: self)
        let defaults = UserDefaults.standard
        defaults.set(savedData, forKey: "user")
    }
    
    static func loadUser() -> User {
        let defaults = UserDefaults.standard
        var user: User?
        
        if let savedUser = defaults.object(forKey: "user") as? Data {
            user = NSKeyedUnarchiver.unarchiveObject(with: savedUser) as? User
        }
        return user!
    }
}

extension Data {
    func toInt() -> Int {
        return self.withUnsafeBytes { $0.pointee }
    }
}
