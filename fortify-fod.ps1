#
# Example script to perform Fortify on Demand Static Code Analysis
#

# Parameters
param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('classic','security','devops')]
    [string]$ScanPolicy = "classic",
    [Parameter(Mandatory=$false)]
    [switch]$SkipPDF,
    [Parameter(Mandatory=$false)]
    [switch]$SkipSSC
)

# Import local environment specific settings
$EnvSettings = $(ConvertFrom-StringData -StringData (Get-Content ".\.env" | Where-Object {-not ($_.StartsWith('#'))} | Out-String))
$AppName = $EnvSettings['APP_NAME']
$AppVersion = $EnvSettings['APP_RELEASE_NAME']
$FoDApiUri = $EnvSettings['FOD_API_URI']
$FoDClientId = $EnvSettings['FOD_CLIENT_ID']
$FoDClientSecret = $EnvSettings['FOD_CLIENT_SECRET']

if ([string]::IsNullOrEmpty($AppName)) { throw "Application Name has not been set" }
if ([string]::IsNullOrEmpty($AppVersion)) { throw "Application Version has not been set" }
if ([string]::IsNullOrEmpty($FoDApiUri)) { throw "FoD API URI has not been set" }
if ([string]::IsNullOrEmpty($FoDClientId)) { throw "FoD Client Id has not been set" }
if ([string]::IsNullOrEmpty($FoDClientSecret)) { throw "FoD Client Secret has not been set" }

# Run the translation and scan

& scancentral package
& fcli fod session login --url $FoDApiUri --client-id $FoDClientId--client-secret $FoDClientSecret --session fcli-local
& fcli fod sast-scan start --release "$($AppName):$($AppVersion)" -f fortifypackage.zip --store curScan --session fcli-local
& fcli fod sast-scan wait-for ::curScan:: --session fcli-local
& fcli fod session logout --session fcli-local

Write-Host Done.
