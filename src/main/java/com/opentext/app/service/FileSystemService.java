/*
        FortifyDemoApp - an insecure web application.

        Copyright (C) Copyright 2024 OpenText Corp.

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

package com.microfocus.app.service;

import com.fasterxml.jackson.core.JsonEncoding;
import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonGenerator;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;

@Service
public class FileSystemService {

    public static final String USER_INFO_FILE = "user_info.json";
    public static final String NEWSLETTER_USER_FILE = "newsletter_registration.json";
    public static final String DEFAULT_ROLE = "guest";
    private static final Logger log = LogManager.getLogger(FileSystemService.class);

    public FileSystemService() {
    }

    public void writeUser(Integer id, String user, String email) throws IOException {
        JsonFactory jsonFactory = new JsonFactory();

        File dataFile = new File(getFilePath(USER_INFO_FILE));
        if (dataFile.createNewFile()) {
            if (log.isDebugEnabled()) {
                log.debug("Created new file: {}", dataFile.toString());
            }
        }

        JsonGenerator jGenerator = jsonFactory.createGenerator(dataFile, JsonEncoding.UTF8);

        jGenerator.writeStartObject();

        jGenerator.writeFieldName("id");
        jGenerator.writeRawValue("\"" + id.toString() + "\"");

        jGenerator.writeFieldName("name");
        jGenerator.writeRawValue("\"" + user + "\"");

        jGenerator.writeFieldName("email");
        jGenerator.writeRawValue("\"" + email + "\"");

        jGenerator.writeFieldName("role");
        jGenerator.writeRawValue("\"default\"");

        jGenerator.writeEndObject();

        jGenerator.close();
    }

    private String getFilePath(String relativePath) {
        return System.getProperty("user.home") + File.separatorChar + relativePath;
    }
}
