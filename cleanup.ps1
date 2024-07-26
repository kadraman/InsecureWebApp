
# Import local environment specific settings
$EnvSettings = $(ConvertFrom-StringData -StringData (Get-Content ".\.env" | Where-Object {-not ($_.StartsWith('#'))} | Out-String))
$AppName = $EnvSettings['APP_NAME']
$ScanSwitches = "'-Dcom.fortify.sca.ProjectRoot=.fortify'"

Write-Host "Removing files..."
& sourceanalyzer $ScanSwitches -b "$AppName" -clean
Remove-Item -Force -Recurse ".fortify" -ErrorAction SilentlyContinue
Remove-Item "$($AppName)*.fpr" -ErrorAction SilentlyContinue
Remove-Item "$($AppName)*.pdf" -ErrorAction SilentlyContinue
Remove-Item "fod.zip" -ErrorAction SilentlyContinue
Remove-Item "*Package.zip" -ErrorAction SilentlyContinue
Remove-Item "*.debricked*" -ErrorAction SilentlyContinue
Remove-Item -Force -Recurse "instance"

Write-Host "Done."
