package core;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Parses a BOINC global_prefs.xml file and either edits or gets tags.
 * Created by Soham Kale on 2/20/18
 *
 */
public class XMLController {

    static boolean editTag(String element, String value) {
        Element elem = getElement(element);
        if (elem != null && element.equals(elem.getNodeName())) {
            elem.setTextContent(value);
            return true;
        } return false;
    }

    static String getTag(String element) {
        Element elem = getElement(element);
        if (elem != null) {
            return elem.getTextContent();
        } return "";
    }

    private static Element getElement(String element) {
        File globalPrefFile = new File("./Boinc/global_prefs_override.xml");
        DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder;
        try {
            dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(globalPrefFile);
            doc.getDocumentElement().normalize();

            NodeList globalPreferences = doc.getFirstChild().getChildNodes();
            Node node;
            Element elem;
            for (int i = 0; i< globalPreferences.getLength(); i++) {
                node = globalPreferences.item(i);
                if (node.getNodeType() == Node.ELEMENT_NODE) {
                    elem = (Element) node;
                    if (element.equals(elem.getNodeName())) {
                        return elem;
                    }
                }
            }
        } catch (SAXException | ParserConfigurationException | IOException e1) {
            e1.printStackTrace();
        }
        return null;
    }
}







