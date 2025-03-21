# PowerShell Script to Register Artifactory Token Refresher in Task Scheduler

$taskName = "ArtifactoryTokenRefresher"

# Get full path to the batch file
$scriptPath = "$PSScriptRoot\token_refresher_runner.bat"

# Create the task action
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""

# Set trigger to run at user logon
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Run with highest privileges
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Description "Refreshes Artifactory token at login" -Force

Write-Host "✅ Task '$taskName' has been registered successfully!"
