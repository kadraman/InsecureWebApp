#
# Example script to perform Fortify Static Code Analysis
#

# Parameters
param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('classic','security','devops')]
    [string]$ScanPolicy = "classic",
    [Parameter(Mandatory=$false)]
    [switch]$SkipPDF
)

# Import local environment specific settings
$EnvSettings = $(ConvertFrom-StringData -StringData (Get-Content ".\.env" | Where-Object {-not ($_.StartsWith('#'))} | Out-String))
$AppName = $EnvSettings['APP_NAME']
$AppVersion = $EnvSettings['APP_VER_NAME']

$JVMArgs = ""
#$JVMArgs = "-Xss256M"
$ScanSwitches = ""
#$ScanSwitches = "-Dcom.fortify.sca.rules.enable_wi_correlation=true -Dcom.fortify.sca.Phase0HigherOrder.Languages=javascript,typescript -Dcom.fortify.sca.EnableDOMModeling=true -Dcom.fortify.sca.follow.imports=true -Dcom.fortify.sca.exclude.unimported.node.modules=true"

# Test we have Fortify installed successfully
if ([string]::IsNullOrEmpty($AppName)) { throw "Application Name has not been set" }
if ([string]::IsNullOrEmpty($AppVersion)) { throw "Application Version Name has not been set" }

# Run the translation and scan

# Compile the application if not already built
$DependenciesFile = Join-Path -Path (Get-Location) -ChildPath "build\classpath.txt"
if (-not (Test-Path -PathType Leaf -Path $DependenciesFile)) {
    Write-Host Cleaning up workspace...
    & sourceanalyzer '-Dcom.fortify.sca.ProjectRoot=.fortify' -b "$AppName" -clean
    Write-Host Building application...
    & .\gradlew clean build writeClasspath -x test
}
$ClassPath = Get-Content -Path $DependenciesFile

Write-Host Running translation...
& sourceanalyzer '-Dcom.fortify.sca.ProjectRoot=.fortify' $JVMArgs $ScanSwitches -b "$AppName" `
    -jdk 11 -java-build-dir "build" -cp $ClassPath -debug -verbose `
    -exclude ".\src\main\resources\static\js\lib" -exclude ".\src\main\resources\static\css\lib" `
    -exclude ".\node_modules" -exclude "src/main/resources/schema.sql" -exclude "src/main/resources/data.sql" `
    "src" "Dockerfile*" "*.bicep"

Write-Host Running scan...
& sourceanalyzer '-Dcom.fortify.sca.ProjectRoot=.fortify' $JVMArgs $ScanSwitches -b "$AppName" `
    -cp $ClassPath  -java-build-dir "build" -debug -verbose `
    -scan-policy $ScanPolicy `
    -build-project "$AppName" -build-version "$AppVersion" -build-label "SNAPSHOT" `
    -scan 
#    -f "$($AppName).fpr"


Write-Host Done.
