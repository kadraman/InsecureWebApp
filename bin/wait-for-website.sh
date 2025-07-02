#!/bin/bash
until curl --head --silent --fail https://insecurewebapp.azurewebsites.net/products 1> /dev/null 2>&1; do
    sleep 1
done