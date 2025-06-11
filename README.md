[![Fortify on Demand](https://github.com/kadraman/InsecureWebApp/actions/workflows/fod.yml/badge.svg)](https://github.com/kadraman/InsecureWebApp/actions/workflows/fod.yml) [![Debricked](https://github.com/kadraman/InsecureWebApp/actions/workflows/debricked.yml/badge.svg)](https://github.com/kadraman/InsecureWebApp/actions/workflows/debricked.yml)

# InsecureWebApp

This is a simple Python Flask web application that can be used for the demonstration of Application
Security testing tools - such as [OpenText Application Security](https://www.opentext.com/products/application-security). 

Pre-requisities
---------------

 - Windows or Linux machine with Python 3.12 or later
 - [Pip package manager](https://pypi.org/project/pip/)
 - [GNU Make}(https://www.gnu.org/software/make/)
 - Local Docker installation (optional)

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

There are only a few features that are functional in this version of the app:

- you can navigate to the "Shop"
- you can type in some keywords in the Shop search box, e.g. "alphadex" to filter results
- you can click on any search result to navigate to a details page
- you can download a datasheet PDF from a details page
- you can subscribe to the newsletter by entering an email address in the input field of the footer

You can login/logout (user credentials are: user1@localhost.com/password or admin@localhost.com/password)
for the OTP code, the secret is hard coded to "base32secret3232" so you can use an app or online tool
such as <a href="https://totp.danhersam.com/">TOTP Token Generator</a> to generate the code.


Scan Application (with OpenText Application Security)
-----------------------------------------------------

To carry out a Fortify Static Code Analyzer local scan, run the following:

```
make sast-scan
```

To carry out a Fortify ScanCentral SAST scan, run the following:

```
fcli ssc session login
scancentral package -o package.zip -bt none --python-virtual-env .venv -oss
fcli sast-scan start --release "_YOURAPP_:_YOURREL_" -f package.zip --store curScan
fcli sast-scan wait-for ::curScan::
fcli ssc action run appversion-summary --av "_YOURAPP_:_YOURREL_" -fs "Security Auditor View" -f summary.md
```

To carry out a Fortify on Demand scan, run the following:

```
fcli fod session login
scancentral package -o package.zip -bt none --python-virtual-env .venv -oss
fcli fod sast-scan start --release "_YOURAPP_:_YOURREL_" -f package.zip --store curScan
fcli fod sast-scan wait-for ::curScan::
fcli fod action run release-summary --rel "_YOURAPP_:_YOURREL_" -f summary.md
```

---

Kevin A. Lee (kadraman) - klee2@opentext.com
