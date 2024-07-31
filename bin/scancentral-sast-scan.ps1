#
# Example script to perform Fortify Static Code Analysis via ScanCentral SAST
#

# Import local environment specific settings
$EnvSettings = $(ConvertFrom-StringData -StringData (Get-Content (Join-Path "." -ChildPath ".env") | Where-Object {-not ($_.StartsWith('#'))} | Out-String))
$AppName = $EnvSettings['SSC_APP_NAME']
$AppVersion = $EnvSettings['SSC_APP_VER_NAME']
$SSCAuthToken = $EnvSettings['SSC_AUTH_TOKEN'] # AnalysisUploadToken
$ScanCentralCtrlUrl = $EnvSettings['SCANCENTRAL_CTRL_URL']
$ScanCentralPoolId = $EnvSettings['SCANCENTRAL_POOL_ID'] # Not yet used
$ScanCentralEmail = $EnvSettings['SCANCENTRAL_EMAIL']

$BuildVersion = $(git log --format="%H" -n 1)
$BuildLabel = "fortifydemoapp-cli"
$ScanArgs = @(
    "-build-project",
    "'$AppName'",
    "-build-version",
    "$BuildVersion",
    "-build-label",
    "$BuildLabel"
)
$PackageName = "package.zip"

# Test we have Fortify installed successfully
if ([string]::IsNullOrEmpty($ScanCentralCtrlUrl)) { throw "ScanCentral Controller URL has not been set" }
if ([string]::IsNullOrEmpty($ScanCentralEmail)) { throw "ScanCentral Email has not been set" }
if ([string]::IsNullOrEmpty($SSCAuthToken)) { throw "SSC Authentication token has not been set" }
if ([string]::IsNullOrEmpty($AppName)) { throw "Application Name has not been set" }
if ([string]::IsNullOrEmpty($AppVersion)) { throw "Application Version has not been set" }

# Delete Package if it already exists
if (Test-Path $PackageName) {
   Remove-Item $PackageName -Verbose
}

# Package, upload and run the scan and import results into SSC
Write-Host Invoking ScanCentral SAST ...
& scancentral -url $ScanCentralCtrlUrl start -upload -uptoken $SSCAuthToken -bt none --python-virtual-env .venv -oss -sp $PackageName `
    -application "$AppName" -version $AppVersion -email $ScanCentralEmail -block -o -f "$($AppName).fpr"  `
    -sargs "$($ScanArgs)"

# Uncomment if not using "-block" in scancentral command above
#Write-Host
#Write-Host You can check ongoing status with:
#Write-Host " scancentral -url $ScanCentralCtrlUrl status -token [received-token]"

Write-Host Done.
