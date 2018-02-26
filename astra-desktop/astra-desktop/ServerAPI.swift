//
//  ServerAPI.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/6/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Foundation

class ServerAPI {
    var urlHandle = "" /* Add URL handle for Astra API */
    
    func makeRequest(urlEndpoint: String, requestData: [String: String]? = nil, requestType: String) throws -> [String: String] {
        let endpoint: String = "https://" + urlHandle + urlEndpoint
        guard let url = URL(string: endpoint) else {
            throw ServerAPIError.urlCreation
        }
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = requestType
        let session = URLSession.shared
        
        if true {
            let newData: [String: Any] = requestData!
            let jsonData: Data  
            do {
                jsonData = try JSONSerialization.data(withJSONObject: newData, options: [])
                urlRequest.httpBody = jsonData
            } catch {
                throw ServerAPIError.jsonCreation
            }
        }
        
        let task = session.dataTask(with: urlRequest) {
            (data, response, error) -> Void in
            guard error == nil else { throw ServerAPIError.serverError(error: error) }
            guard let responseData = data else { throw ServerAPIError.dataNotFound }
            
            do {
                guard let validatedData = try JSONSerialization.jsonObject(with: responseData, options: []) as? [String: Any] else {
                    throw ServerAPIError.jsonConversion
                }
                return validatedData
            } catch {
                throw ServerAPIError.jsonConversion
            }
        }
        task.resume()
    }
}


extension ServerAPI {
    /* Add methods for making HTTP calls to API */
 
    func testHTTP() throws -> [String: String] {
        return try makeRequest(urlEndpoint: "/test/", requestType: "GET")
    }
}


enum ServerAPIError: Error {
    case urlCreation
    case serverError(error: String)
    case dataNotFound
    case jsonTranslation
    case jsonCreation
}
