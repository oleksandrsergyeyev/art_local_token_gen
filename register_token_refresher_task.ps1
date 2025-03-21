# PowerShell Script to Register Artifactory Token Refresher in Task Scheduler (Run even if user is not logged in)

$taskName = "ArtifactoryTokenRefresher"

# Get full path to the batch file
$scriptPath = "$PSScriptRoot\token_refresher_runner.bat"

# Define the task action
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""

# Trigger the task to run at system startup
$trigger = New-ScheduledTaskTrigger -AtStartup

# Use the current user with highest privileges
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Register the task — will prompt for user credentials
Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "Refreshes Artifactory token at system startup" `
    -Force

Write-Host "✅ Task '$taskName' has been registered successfully to run at system startup (even if user is not logged in)."
