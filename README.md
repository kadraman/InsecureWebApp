[![Fortify on Demand](https://github.com/fortify-presales/FortifyDemoApp/actions/workflows/fod.yml/badge.svg)](https://github.com/fortify-presales/FortifyDemoApp/actions/workflows/fod.yml) [![Debricked](https://github.com/fortify-presales/FortifyDemoApp/actions/workflows/debricked.yml/badge.svg)](https://github.com/fortify-presales/FortifyDemoApp/actions/workflows/debricked.yml)

# Fortify Demo App

This is a simple Python Flask web application that can be used for the demonstration of application
security testing tools such as those provided by [Fortify by OpenText](https://www.microfocus.com/en-us/cyberres/application-security).
It is a cut down "search" results/details page from a larger sample application [IWA-Java](https://github.com/fortify/IWA-Java) and is kept deliberately small for demos.

Run Application (locally)
-------------------------

You can the run the application locally using the following:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
cd app
pip install -r requirements.txt
flask run
```

The application should then be available at the URL `http://localhost:5000`. If it fails to start,
make sure you have no other applications running on port 5000. There are only a few features that are
functional in this version of the app:

- you can navigate to the "Shop"
- you can type in some keywords in the Shop search box, e.g. "alphadex" to filter results
- you can click on any search result to navigate to a details page
- you can download a datasheet PDF from a details page
- you can subscribe to the newsletter by entering an email address in the input field of the footer
- you can login/logout (user credentials are: user1@localhost.com/password or admin@localhost.com/password)

These have been "enabled" because they all have potential security issues that can be found by Fortify.

Deploy Application (Azure)
--------------------------

If you want to run the application in the cloud you can deploy it to Microsoft Azure along with its required
infrastructure by using the Azure DevOps CLI and the Gradle build script. In order to deploy to Azure you will need
to create a `.env` file in the root directory with contents similar to the following:

```
AZURE_SUBSCRIPTION_ID=17d2722b-256e-47e5-84b8-5b01f509a42c
AZURE_RESOURCE_GROUP=fortifydemorg
AZURE_APP_NAME=fortifydemoapp
AZURE_REGION=eastus
```

Then you can run the following commands:

```
az login [--tenant XXXX]
az group create --name [YOUR_INITIALS]-fortifydemorg --location eastus
TBD
```

Replace `eastus` with your own desired region and make sure in the `.env` file you have
set `AZURE_APP_NAME` to a unique value.

You can navigate to your [Azure portal](https://portal.azure.com/#home) to see the built infrastructure and to
the deployed web application using the URL output shown from the `azureWebAppDeploy task`.

Remove Application and Infrastructure
-------------------------------------

To clean up all the resources you can execute the following (from a Windows command prompt):

```
az group delete --name [YOUR_INITIALS]-fortifydemorg
```

Run a Fortify scan:

First clean up any existing data from a previous build and scan:

```
sourceanalyzer -b fortifydemoapp -clean
```

Next, translate the source files by using the sourceanalyzer command:

```
sourceanalyzer -b fortifydemoapp -python-path ".venv/Lib/site-packages/" app
```

Then, execute the scan on the translated files:

```
sourceanalyzer -b fortifydemoapp -scan -verbose -f fortifydemoapp.fpr
```

Finally, view the results in AuditWorkbench:

```
auditworkbench fortifydemoapp.fpr
```

You can also use ScanCentral by first creating a mobile build solution (mbs) and then uploading it:

```
sourceanalyzer -b fortifydemoapp.fpr -export-build-session fortifydemoapp.mbs -python-path ".venv/Lib/site-packages/" app
scancentral -url _YOUR_SCANCENTRAL_CTRL_URL_ start -upload -uptoken _YOUR_SSC_AUTHTOKEN_ `
    -b fortifydemoapp.fpr -application FortifyDemoApp -version 1.0 -mbs fortifydemoapp.mbs `
    -email _YOUR_EMAIL_ -block -o -f fortifydemoapp.fpr
```

---

Kevin A. Lee (kadraman) - klee2@opentext.com
