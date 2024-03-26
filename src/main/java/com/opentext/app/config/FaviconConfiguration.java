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

package com.opentext.app.config;

import com.opentext.app.FortifyDemoApp;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.web.servlet.handler.SimpleUrlHandlerMapping;
import org.springframework.web.servlet.resource.ResourceHttpRequestHandler;

import java.util.Arrays;
import java.util.Collections;

@Configuration
public class FaviconConfiguration {

    private static final Logger log = LogManager.getLogger(FaviconConfiguration.class);

    @Value("${server.servlet.context-path}")
    private String contextPath;

    @Bean("CustomFaviconHandlerMapping")
    public SimpleUrlHandlerMapping faviconHandlerMapping() {
        SimpleUrlHandlerMapping mapping = new SimpleUrlHandlerMapping();
        mapping.setOrder(Integer.MIN_VALUE);
        mapping.setUrlMap(Collections.singletonMap(contextPath + "/img/favicons/favicon.png",
                faviconRequestHandler()));
        return mapping;
    }

    @Bean("CustomFaviconRequestHandler")
    protected ResourceHttpRequestHandler faviconRequestHandler() {
        ResourceHttpRequestHandler requestHandler = new ResourceHttpRequestHandler();
        requestHandler.setLocations(Arrays
                .<Resource> asList(new ClassPathResource("/")));
        return requestHandler;
    }

}
