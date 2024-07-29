#
# Example script to perform Fortify Static Code Analysis
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
$SSCUrl = $EnvSettings['SSC_URL']
$SSCAuthToken = $EnvSettings['SSC_AUTH_TOKEN'] # AnalysisUploadToken
$JVMArgs = "-Xss256M"
$ScanSwitches = "-Dcom.fortify.sca.ProjectRoot=.fortify"

if ([string]::IsNullOrEmpty($AppName)) { throw "Application Name has not been set" }

# Run the translation and scan

Write-Host Running translation...
& sourceanalyzer $ScanSwitches $JVMArgs -b "$AppName" -python-path ".venv/Lib/site-packages/" -exclude ".venv" "app"

Write-Host Running scan...
& sourceanalyzer $ScanSwitches $JVMArgs -b "$AppName" -debug -verbose `
    -scan-policy $ScanPolicy -build-project "$AppName" -build-version "$AppVersion" -build-label "SNAPSHOT" `
    -scan -f "$($AppName).fpr"

# summarise issue count by analyzer
& fprutility -information -analyzerIssueCounts -project "$($AppName).fpr"

if (-not $SkipPDF) {
    Write-Host Generating PDF report...
    & ReportGenerator $ScanSwitches -user "Demo User" -format pdf -f "$($AppName).pdf" -source "$($AppName).fpr"
}

if (-not $SkipSSC) {
    Write-Host Uploading results to SSC...
    & fortifyclient uploadFPR -file "$($AppName).fpr" -url $SSCUrl -authtoken $SSCAuthToken -application "$AppName" -applicationVersion "$AppVersion"
}

Write-Host Done.
