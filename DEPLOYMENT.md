# Deployment & Distribution Guide

## Quick Start (For Users)

### Windows Users
1. Download `PasswordStrengthChecker.exe` from `/dist` folder
2. Double-click to run (no installation needed)
3. First run may take a few seconds as it initializes

### For IT/Admin Distribution
```powershell
# Copy EXE to network share
Copy-Item -Path "dist\PasswordStrengthChecker.exe" -Destination "\\network\shared\apps\"

# Create shortcut on user desktops
$SourceFileLocation = "\\network\shared\apps\PasswordStrengthChecker.exe"
$ShortcutLocation = "$env:USERPROFILE\Desktop\Password Checker.lnk"
$WshShell = New-Object -ComObject WshShell
$Shortcut = $WshShell.CreateShortcut($ShortcutLocation)
$Shortcut.TargetPath = $SourceFileLocation
$Shortcut.Save()
```

## Antivirus Considerations

The PyInstaller-generated EXE may trigger false positives in some antivirus software because:
- It unpacks runtime files to temp directory
- Uses uncommon entry points
- Includes bundled Python runtime

### If Flagged:
1. **Most common**: False positive - whitelist in your antivirus
2. **Mitigation**: 
   - Sign EXE with code signing certificate (Windows Authenticode)
   - Submit to antivirus vendors for analysis
   - Use reputable distribution platform

### Signature Information
- **Publisher**: Your organization
- **Timestamp**: Included in build
- **Trusted Root**: Windows Authenticode

## File Manifest

```
dist/
├── PasswordStrengthChecker.exe (45 MB)
└── [Runtime files auto-extracted to %TEMP% on first run]

build/
├── PasswordStrengthChecker/
│   ├── _internal/          (Dependencies, DLLs, libraries)
│   ├── base_library.zip    (Python standard library)
│   ├── PYZ-00.pyz         (Bundled Python packages)
│   └── PKG-00.pkg         (Application package)
```

## System Requirements

**Minimum:**
- Windows 7 SP1 or later
- 100 MB free disk space
- Internet connection (optional, for breach checking)

**Recommended:**
- Windows 10/11
- 200 MB free disk space
- 1GB RAM
- Broadband internet

## Installation Methods

### Method 1: Direct EXE (Current)
- **Pros**: Simplest, no installation
- **Cons**: Large file size (45 MB)
- **Use case**: Individual users, portable installs

### Method 2: Create Windows Installer (.MSI) - Future

```batch
# Install WiX Toolset
# Create installer from EXE
# Automatically creates uninstaller
# Single-click installation for end users
```

### Method 3: Package in Portable ZIP

```powershell
# Create portable package
New-Item -ItemType Directory -Path "dist\PasswordChecker-Portable"
Copy-Item "dist\PasswordStrengthChecker.exe" -Destination "dist\PasswordChecker-Portable\"
Copy-Item "README.md" -Destination "dist\PasswordChecker-Portable\"
Copy-Item "LICENSE" -Destination "dist\PasswordChecker-Portable\"

# Zip it
Compress-Archive -Path "dist\PasswordChecker-Portable\" -DestinationPath "dist\PasswordChecker-v1.0.0.zip"
```

## Troubleshooting Deployment

### EXE won't start
- [ ] Check Windows version (requires Windows 7+)
- [ ] Verify file integrity (check file size: ~45 MB)
- [ ] Disable antivirus temporarily
- [ ] Run from Command Prompt: `PasswordStrengthChecker.exe` (see error output)

### Missing common_passwords.txt
- Verify file included in PyInstaller `--add-data` flag
- Check build output: "common_passwords.txt" in datas
- Rebuild with correct data path

### Breach check not working
- Verify internet connectivity
- Check firewall rules for HTTPS outbound (port 443)
- API endpoint: `api.pwnedpasswords.com`

### Application crashes
- Check Windows Event Viewer for error details
- Verify Python version compatibility (3.10+)
- Clear `%TEMP%\_MEI*` folders and retry

## Performance Optimization

### Reduce EXE Size (Advanced)

```bash
# Use --onedir instead of --onefile (faster launch)
pyinstaller --onedir --windowed --add-data "common_passwords.txt:." gui_app.py

# Use UPX to compress (optional)
pyinstaller --upx-dir=/path/to/upx --onefile gui_app.py
```

### Startup Performance

Current: ~2-3 seconds
- First run initializes Tcl/Tk
- Subsequent runs use cached modules

To improve:
1. Use `--onedir` mode (faster unpacking)
2. Lazy-load pandas/reportlab (only when needed)
3. Pre-cache common passwords on startup

## Distribution Checklist

- [ ] EXE tested on fresh Windows install
- [ ] README included in distribution
- [ ] LICENSE file included
- [ ] Version number documented
- [ ] Common passwords file included (14K+ list)
- [ ] Antivirus scanning completed
- [ ] File integrity verified (MD5/SHA256)
- [ ] User documentation provided
- [ ] Support contact information available

## Update Strategy

### For Version Updates

```powershell
# Build new version
pyinstaller --name "PasswordStrengthChecker-v1.1.0" gui_app.py

# Users simply download and replace EXE
# No configuration migration needed (JSON history preserved)
```

### Auto-Update Feature (Planned)

```python
# Check for new version on startup
import requests
response = requests.get("https://api.github.com/repos/user/password-checker/releases/latest")
latest_version = response.json()['tag_name']
if latest_version > CURRENT_VERSION:
    # Notify user of update available
```

## Security Practices

### Before Distribution

1. **Code Review**: Scan for security issues
   ```bash
   pip install bandit
   bandit -r . -ll
   ```

2. **Dependency Check**: Verify no known vulnerabilities
   ```bash
   pip install safety
   safety check
   ```

3. **Static Analysis**: Check Python code quality
   ```bash
   pip install pylint
   pylint gui_app.py password_core.py
   ```

### Code Signing (Professional Distribution)

```powershell
# Sign the EXE with Authenticode certificate
Set-AuthenticodeSignature -FilePath "dist\PasswordStrengthChecker.exe" -Certificate (Get-Item cert:\CurrentUser\My\{Thumbprint})
```

## Compliance

- **GDPR**: App stores only hashed passwords and user consent logged
- **HIPAA**: Suitable for healthcare use (local analysis only)
- **PCI-DSS**: Can be used for password validation workflows
- **SOC 2**: No data collection or transmission

## Support Information

Include in distributed package:

```
Support Contact: [your-email@example.com]
Documentation: README.md
Known Issues: [list any known issues]
Version: 1.0.0
Last Updated: 2026-01-27
```

---

**Next Steps**: 
1. Code signing for enterprise distribution
2. Create .MSI installer for automated deployment
3. GitHub release with automatic updates
4. Docker image for cloud deployment
