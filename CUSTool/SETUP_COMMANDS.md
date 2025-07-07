# CLI User Simulator (CUS) - Complete Setup and Run Commands

## PowerShell Commands (Run in PowerShell as Administrator if needed)

### 1. Navigate to Project Directory
```powershell
cd "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"
```

### 2. Create Necessary Directories
```powershell
if (!(Test-Path "Logs")) { New-Item -ItemType Directory -Path "Logs" }
if (!(Test-Path "Logs\CUSErrors")) { New-Item -ItemType Directory -Path "Logs\CUSErrors" }
if (!(Test-Path "Logs\CUSEvents")) { New-Item -ItemType Directory -Path "Logs\CUSEvents" }
if (!(Test-Path "NewErrors")) { New-Item -ItemType Directory -Path "NewErrors" }
if (!(Test-Path "NewEvents")) { New-Item -ItemType Directory -Path "NewEvents" }
```

### 3. Install Required Python Packages
```powershell
& "C:\Program Files\Python313\python.exe" -m pip install --upgrade pip
& "C:\Program Files\Python313\python.exe" -m pip install -r requirements.txt
```

### 4. Create Sample Simulation Dictionary (if not exists)
```powershell
if (!(Test-Path "simulation_dictionary.txt")) {
    @'
{
  "Please enter your choice": "1\n",
  "Continue? (y/n)": "y\n",
  "Enter password": "password123\n"
}
'@ | Out-File -FilePath "simulation_dictionary.txt" -Encoding UTF8
}
```

### 5. Create Sample Output Log File
```powershell
if (!(Test-Path "Logs\output.log")) {
    "Sample log content" | Out-File -FilePath "Logs\output.log" -Encoding UTF8
}
```

### 6. Run Unit Tests
```powershell
& "C:\Program Files\Python313\python.exe" -m pytest test_CUS.py -v | Out-File -FilePath "Logs\test_results.log" -Encoding UTF8
```

### 7. Check Test Results
```powershell
Get-Content "Logs\test_results.log"
```

### 8. Check for Syntax Errors
```powershell
& "C:\Program Files\Python313\python.exe" -m py_compile CUS.py
```

### 9. Run CUS.py
```powershell
& "C:\Program Files\Python313\python.exe" CUS.py
```

## Alternative: Run the Complete Setup Script
```powershell
.\setup_and_run_complete.bat
```

## Manual Installation Commands (if pip fails)
```powershell
& "C:\Program Files\Python313\python.exe" -m pip install pynput==1.7.6
& "C:\Program Files\Python313\python.exe" -m pip install watchdog==3.0.0
& "C:\Program Files\Python313\python.exe" -m pip install pytest==7.0.0
& "C:\Program Files\Python313\python.exe" -m pip install mock==4.0.3
```

## Troubleshooting Commands
```powershell
# Check Python version
& "C:\Program Files\Python313\python.exe" --version

# Check installed packages
& "C:\Program Files\Python313\python.exe" -m pip list

# Check if modules can be imported
& "C:\Program Files\Python313\python.exe" -c "import pynput; import watchdog; import pytest; print('All modules imported successfully')"
```

## File Structure Verification
```powershell
Get-ChildItem -Recurse | Format-Table Name, Mode, Length, LastWriteTime
```
