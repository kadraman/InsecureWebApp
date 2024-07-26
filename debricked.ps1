#
# Example script to perform Debricked scan
#

# Import local environment specific settings
$EnvSettings = $(ConvertFrom-StringData -StringData (Get-Content ".\.env" | Where-Object {-not ($_.StartsWith('#'))} | Out-String))
$AppName = $EnvSettings['APP_NAME']
$DebrickedToken = $EnvSettings['DEBRICKED_TOKEN']

if ([string]::IsNullOrEmpty($AppName)) { throw "Application Name has not been set" }
if ([string]::IsNullOrEmpty($DebrickedToken)) { throw "Debricked Token has not been set" }

debricked scan -r "$AppName" --access-token="$DebrickedToken" .