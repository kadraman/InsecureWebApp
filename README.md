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
.venv\Scripts\Activate.ps1      [Windows]
.venv/Scripts/activate          [Linux/UNIX]
pip install -r app\requirements.txt
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

---

Kevin A. Lee (kadraman) - klee2@opentext.com
