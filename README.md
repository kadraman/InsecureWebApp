[![CodeQL Advanced](https://github.com/kadraman/InsecureWebApp/actions/workflows/codeql.yml/badge.svg)](https://github.com/kadraman/InsecureWebApp/actions/workflows/codeql.yml) [![Fortify on Demand](https://github.com/fortify-presales/InsecureWebApp/actions/workflows/fod.yml/badge.svg)](https://github.com/kadraman/InsecureWebApp/actions/workflows/fod.yml) [![Build and Deploy to Azure](https://github.com/kadraman/InsecureWebApp/actions/workflows/azure_webapp.yml/badge.svg)](https://github.com/kadraman/InsecureWebApp/actions/workflows/azure_webapp.yml)

# InsecureWebApp

This is a simple Python Flask web application that can be used for the demonstration of Application
Security testing tools (include SAST, DAST and SCA). The application has a few basic features to demonstrate some common vulnerabilities such as:

    - SQL Injection
    - Cross Site Scripting (XSS)
    - Insecure Deserialization
    - Security Misconfiguration
    - Sensitive Data Exposure
    - Broken Authentication (with 2FA)
    - Using Components with Known Vulnerabilities

The application is not intended to be used in production and is provided for educational purposes only.

Pre-requisites
---------------

 - [Python 3.12 or later](https://www.python.org/downloads/)
 - [Pip package manager](https://pypi.org/project/pip/)
 - [CygWin](https://www.cygwin.com/) - if running on Windows
 - [Rust Compiler](https://www.rust-lang.org/tools/install) - if running on Windows as some Pip packages require it
 - Docker installation (optional)

Run Application (locally)
-------------------------

You can the run the application locally using the following:

Windows:

```
make build
make run
```

The application should then be available at the URL `http://localhost:5000`. If it fails to start,
make sure you have no other applications running on port 5000. 

Run Application (as Docker container)
-------------------------------------

You also can build a Docker image for the application using the following:

```
docker build -t demoapp:latest .
```

Then run the container using a command similar to the following:

```
docker run -dp 8080:8000 demoapp:latest
```

The application will then be available at the URL `http://localhost:8080`. If it fails to start,
make sure you have no other applications running on port 8080.

Using the Application
---------------------

Most of the application functionality is available as a guest user, however some features require
you to login. The application has a basic 2FA implementation using the `pyotp` package.

You can login using the following credentials:
- user1@localhost.com/password
- admin@localhost.com/password

For the OTP code, the secret is hard coded to `base32secret3232`.
You can use an app or online tool such as <a href="https://totp.danhersam.com/">TOTP Token Generator</a> to generate the code.

Scan Application (with bandit)
------------------------------

To carry out a basic security scan with bandit, run the following:

```
make bandit-scan
firefox bandit-report.html
```

Scan Application (with OpenText Application Security)
-----------------------------------------------------

To carry out an OpenText Static Code Analyzer local scan, run the following:

```
make sast-scan
```

To carry out a OpenText ScanCentral SAST scan, run the following:

```
fcli ssc session login
scancentral package -o package.zip -bt none --python-virtual-env .venv -oss
fcli sast-scan start --release "_YOURAPP_:_YOURREL_" -f package.zip --store curScan
fcli sast-scan wait-for ::curScan::
fcli ssc action run appversion-summary --av "_YOURAPP_:_YOURREL_" -fs "Security Auditor View" -f summary.md
```

To carry out an OpenText Application Security Core scan, run the following:

```
fcli fod session login
scancentral package -o package.zip -bt none --python-virtual-env .venv -oss
fcli fod sast-scan start --release "_YOURAPP_:_YOURREL_" -f package.zip --store curScan
fcli fod sast-scan wait-for ::curScan::
fcli fod action run release-summary --rel "_YOURAPP_:_YOURREL_" -f summary.md
```

---

Kevin A. Lee (kadraman) - klee2@opentext.com