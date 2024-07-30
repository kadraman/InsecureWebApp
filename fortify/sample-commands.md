Fortify Local Scan
==================

```
sourceanalyzer -b fortifydemoapp -clean
sourceanalyzer -b fortifydemoapp -python-path ".venv/Lib/site-packages/" -exclude ".venv" "app"
sourceanalyzer -b fortifydemoapp -scan
```

Fortify ScanCentral SAST Scan
==============================

```
scancentral -url _YOUR_SCANCENTRAL_CTRL_UTL start -upload -uptoken _YOUR_SSC_AUTH_TOKEN_ -bt none --python-virtual-env .venv
    -sp package.zip -application "FortifyDemoApp" -version "main" -email _YOUR_EMAIL_ -block -o -f "FortifyDemoApp.fpr"
```

Fortify Command Line (fcli)
===========================

FoD:

```
env | grep FCLI (Unix)
dir env: (PowerShell)
fcli fod session login
scancentral package -o package.zip -bt none --python-virtual-env .venv
fcli fod sast-scan start --release "FortifyDemoApp:main" -f package.zip --store curScan
fcli fod sast-scan wait-for ::curScan::
```

ScanCentral SAST:

```
env | grep FCLI (Unix)
dir env: (PowerShell)
fcli sc-sast session login
scancentral package -o package.zip -bt none --python-virtual-env .venv
fcli sc-sast scan start -p package.zip --sensor-version 23.3 --store curScan
fcli sc-sast scan wait-for ::curScan::
```
