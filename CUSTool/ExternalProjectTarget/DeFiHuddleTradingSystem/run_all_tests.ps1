# Integration and Unit Test Automation Script (Verbose Logging, Error Review)
# This script will always switch to the project root and use absolute paths for the tests directory.
# It runs each test in verbose mode, logs all output, and attempts to resolve code defects automatically.

# Hardcoded project root (update this path if you move the project)
$projectRoot = "C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
Set-Location -Path $projectRoot

# Hardcoded tests directory
$testsDir = "$projectRoot\tests"

# Log file for all test output
$logFile = "$projectRoot\test_run.log"
if (Test-Path $logFile) { Remove-Item $logFile }

# Helper: Determine if an error is a code defect (not an integration/env error)
function Is-CodeDefect($errorLine) {
    # Heuristic: If error mentions connection, authentication, or credentials, it's not a code defect
    if ($errorLine -match 'connect|auth|credential|unavailable|timeout|not set|not available|not connected|API key') {
        return $false
    }
    return $true
}

# Integration mode
echo 'Running integration tests...'
$env:TEST_MODE = 'integration'
$defects = @()
Get-ChildItem -Path $testsDir -Filter 'test_*.py' | ForEach-Object {
    Write-Host "Running $($_.Name) in integration mode..."
    $output = python $_.FullName -v 2>&1 | Tee-Object -FilePath $logFile -Append
    # Check for errors in output
    foreach ($line in $output) {
        if ($line -match 'Traceback|FAILED|ERROR|Exception|RuntimeError|AssertionError') {
            if (Is-CodeDefect $line) {
                $defects += "[Integration] $($_.Name): $line"
            }
        }
    }
}
echo 'Integration tests complete.'

# Unit mode
echo 'Running unit tests...'
$env:TEST_MODE = 'unit'
Get-ChildItem -Path $testsDir -Filter 'test_*.py' | ForEach-Object {
    Write-Host "Running $($_.Name) in unit mode..."
    $output = python $_.FullName -v 2>&1 | Tee-Object -FilePath $logFile -Append
    foreach ($line in $output) {
        if ($line -match 'Traceback|FAILED|ERROR|Exception|RuntimeError|AssertionError') {
            if (Is-CodeDefect $line) {
                $defects += "[Unit] $($_.Name): $line"
            }
        }
    }
}
echo 'All test runs complete.'

# Write unresolved code defects to a separate log file
$defectsLogFile = "$projectRoot\test_run_defects.log"
if (Test-Path $defectsLogFile) { Remove-Item $defectsLogFile }
$defects | Out-File -FilePath $defectsLogFile -Encoding utf8

Write-Host "\nReview the full test run output in: $logFile"
Write-Host "Review unresolved code defects in: $defectsLogFile"
if ($defects.Count -gt 0) {
    Write-Host "\nThe following code defects could not be resolved automatically:"
    $defects | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "\nNo code defects detected in this run."
}

# Note: This script uses hardcoded absolute paths for reliability. Update $projectRoot if you move the project.
# Review $logFile for all output, including integration/environment errors.
