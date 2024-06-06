Fortify Local Scan
==================

```
sourceanalyzer -b fortifydemoapp -clean
sourceanalyzer -b fortifydemoapp .\gradlew clean build
sourceanalyzer -b fortifydemoapp -scan --scan-policy devops
```

or

```
.\fortify-sast.ps1
```


Fortify ScanCentral SAST Scan
==============================

```
scancentral package -o package.zip
scancentral ...
```

or

```
.\fortify-scancentral-sast-ps1
```

Fortify Command Line (fcli)
===========================

FoD:

```
fcli fod session login
env | grep FCLI (Unix)
dir env: (PowerShell)
scancentral package
fcli fod sast-scan start --release "APP:RELEASE" -f fortifypackage.zip --store curScan
fcli fod sast-scan wait-for ::curScan::
```

ScanCentral SAST:

```
fcli sc-sast session login
env | grep FCLI (Unix)
dir env: (PowerShell)
scancentral package
fcli sc-sast scan start -p fortifypackage.zip --sensor-version 23.3 --store curScan
fcli sc-sast scan wait-for ::curScan::
```
