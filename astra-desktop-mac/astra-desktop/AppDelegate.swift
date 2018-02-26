//
//  AppDelegate.swift
//  astra-desktop
//
//  Created by Soham Kale on 1/4/18.
//  Copyright © 2018 Soham Kale. All rights reserved.
//

import Cocoa
import PubNub

@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {
    var window: Window?
    let user: User? = nil
    
    var eventMonitor: EventMonitor?
    let statusItem = NSStatusBar.system.statusItem(withLength:NSStatusItem.squareLength)
    let popover = NSPopover()
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
            
        if let button = statusItem.button {
            button.image = NSImage(named:NSImage.Name("StatusBarButtonImage"))
            button.action = #selector(togglePopover(_:))
        }
        popover.contentViewController = AstraViewController.freshController()
        
        eventMonitor = EventMonitor(mask: [.leftMouseDown, .rightMouseDown]) {[weak self] event in
            if let strongSelf = self, strongSelf.popover.isShown {
                strongSelf.closePopover(sender: event)
            }
        }
    }
    
    func applicationWillTerminate(_ aNotification: Notification) {
        
        let data = NSKeyedArchiver.archivedData(withRootObject: user)
        UserDefaults.standard.set(data, forKey: "user")
    }
    
    func constructMenu() {
        let menu = NSMenu()
        
        menu.addItem(NSMenuItem(title: "Open Astra Webapp", action: #selector(self.openWebApp(_:)),
                                keyEquivalent: "O"))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "Quit Astra Client", action: #selector(NSApplication.terminate(_:)),
                                keyEquivalent: "Q"))
        
        statusItem.menu = menu
    }
    
    @objc func openWebApp(_ sender: Any) {
        NSWorkspace.shared.open(NSURL(string: "")! as URL) // Replace with astra web app url
    }
    
    @objc func togglePopover(_ sender: Any) {
        if popover.isShown {
            closePopover(sender: sender)
        } else {
            showPopover(sender: sender)
        }
    }
    
    func showPopover(sender: Any?) {
        if let button = statusItem.button {
            popover.show(relativeTo: button.bounds, of: button, preferredEdge: NSRectEdge.minY)
        }
        eventMonitor?.start()
    }
    
    func closePopover(sender: Any?) {
        popover.performClose(sender)
        eventMonitor?.stop()
    }
}

