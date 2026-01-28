# Quick Start Guide - Password Strength Checker

## First Time Setup (< 1 minute)

1. **Download**: Get `PasswordStrengthChecker.exe` from the project folder
2. **Run**: Double-click the EXE file
3. **Allow**: Windows may show security prompt - click "Run anyway"
4. **Wait**: App initializes (first run takes 5-10 seconds)
5. **Start**: Begin analyzing passwords!

## Basic Usage

### Check a Password
```
1. Type password in the input field
2. Press Enter or Tab
3. View results instantly:
   - Score: 0-5 rating
   - Strength badge: Visual indicator
   - Entropy: Bits of mathematical strength
   - Suggestions: How to improve
   - Crack time: How long to break
   - Breach status: Is it in data breaches?
```

### Color Coding
- 🔴 **Red** (Score 0-1): Very Weak - AVOID
- 🟠 **Orange** (Score 2-3): Weak - Add complexity
- 🟢 **Green** (Score 4-5): Strong - Good choice!

### Generate Strong Password
```
Click: "Generate Strong Password"
Result: Random 12-char password automatically analyzed
```

## Features Explained

### Strength Badge
```
❌ Vulnerable (Very Weak)        Score < 1
⚠️ Caution (Weak)                Score 1-2
🔒 Secure (Good)                 Score 2-3
🛡️ Stronghold (Very Strong)      Score 3-4
🏆 Fort Knox (Excellent!)        Score 4-5
```

### Entropy
- Higher = Stronger
- 50+ bits = Strong
- 80+ bits = Very strong
- Measures randomness mathematically

### Crack Time
- **Online throttling**: Attacker limited by login attempts
- **Offline fast**: Attacker with GPU/hardware (worst case)
- Shows realistic timeframes to break password

### Breach Check
- ✓ **No**: Password not found in breaches
- ⚠️ **Yes**: Password found in X breaches - DO NOT USE
- ?: **Check failed**: No internet - use cautiously

## Advanced Features

### Dark Mode
- Click: "🌙 Dark Mode"
- Easier on eyes during night use
- Persists during session

### Show/Hide Password
- Check: "Show Password" to see what you're typing
- Security: Only visible to you

### Batch CSV Check
1. Click: "Batch Check CSV"
2. Select: CSV file with 'password' column
3. View: Score for each password at once

Example CSV format:
```
password,username
MyP@ssw0rd!,john_doe
SecurePass123,jane_smith
WeakPass,bob_johnson
```

### Export Report
1. Click: "Export PDF Report"
2. Choose: Save location
3. Opens: PDF with analysis history
4. **Security**: Only shows masked passwords (first + last char)

### Password History
1. Click: "History"
2. View: Last 10 checked passwords
3. Info shown: Masked preview, length, score, entropy

## What's Happening Behind the Scenes?

### Your Password Safety
- ✓ Never stored in plain text
- ✓ Only hashed passwords saved
- ✓ History shows only masked versions
- ✓ All analysis happens locally (no upload)

### Breach Detection
- Sends only: First 5 characters of password hash
- Receives: List of matching hashes
- Compares: Client-side (your computer)
- Privacy: 100% safe (API can't see your full password)

### Strength Analysis
- Character types: Uppercase, lowercase, numbers, symbols
- Pattern detection: Avoids common patterns
- Entropy: Random strength calculation
- Zxcvbn: Advanced heuristic analysis

## Tips for Strong Passwords

### DO
✓ Use 12+ characters
✓ Mix: UPPERCASE + lowercase + 123 + !@#
✓ Use random words or phrases
✓ Make passwords unique per service
✓ Use a password manager

### DON'T
✗ Use personal info (names, birthdays)
✗ Use dictionary words
✗ Reuse passwords
✗ Write down passwords
✗ Share passwords via email/chat

### Password Formula
```
[Random word] + [Number] + [Symbol] + [Another word]

Examples:
- Giraffe47!Phoenix
- Thunder23@Mountains
- Whisper99#Elephant
```

## Troubleshooting

### App won't start
1. Check Windows version (needs Windows 7+)
2. Disable antivirus temporarily
3. Try: Run as Administrator (right-click → Run as administrator)
4. Restart computer

### Breach check not working
1. Check internet connection
2. Try again (API may be temporarily down)
3. Continue without check (shows warning)
4. Offline mode: Use other features while offline

### Password analysis seems wrong
1. Ensure caps lock is OFF
2. Copy/paste password to verify input
3. Check suggestions for patterns app detected
4. Zxcvbn may find patterns you didn't realize

### Can't find history
1. History file: `password_history.json` in app folder
2. Delete to start fresh: Just delete the file
3. Last 10 entries shown in History window

## Security Best Practices

### Using This App
1. **Private computer**: Use on your personal device
2. **Don't test real passwords**: Generate test ones
3. **Internet optional**: Works offline (except breach check)
4. **Share carefully**: Don't screenshot results showing passwords

### After Using
1. **Clear history**: Delete `password_history.json` if needed
2. **Dark mode**: Use to avoid shoulder surfing
3. **Copy generated**: Password to clipboard with password manager

## For IT Professionals

### Enterprise Deployment
- Single .EXE file - no installation needed
- No registry modifications
- Portable to USB drives
- Works offline (except breach checking)
- Suitable for security training

### Compliance Notes
- GDPR compliant: No user data collection
- HIPAA compatible: For healthcare password policies
- No network calls except breach check (HTTPS to api.pwnedpasswords.com)
- Audit trail: None (fully local processing)

### Recommendation
Use in security awareness training:
1. Show password strength variation
2. Demonstrate breach exposure
3. Teach entropy vs. complexity
4. Compare real vs. weak passwords

## Common Questions

**Q: Is my password being uploaded?**
A: No. Only first 5 chars of hashed version sent to breach API.

**Q: Why is it flagged by antivirus?**
A: PyInstaller bundles Python runtime. It's a false positive.

**Q: Can I use generated passwords?**
A: Yes! Click "Generate Strong Password" then copy to clipboard.

**Q: Where's my password history saved?**
A: Local file: `password_history.json` in app folder.

**Q: What if I lose the EXE?**
A: Just download again - no installation data to lose.

**Q: Can it work offline?**
A: Yes, except breach checking (needs internet).

## Next Steps

1. ✓ Download EXE
2. ✓ Run application
3. ✓ Test with sample password
4. ✓ Try "Generate Strong Password"
5. ✓ Check "History" window
6. ✓ Export a PDF report
7. ✓ Toggle dark mode
8. ✓ Use for real passwords!

## Support

- **Documentation**: See README.md for full manual
- **Deployment**: See DEPLOYMENT.md for IT setup
- **Source Code**: github.com/[your-repo]/password-checker
- **Issues**: Report bugs or suggest features

---

**Remember**: This tool helps you understand password strength. Always:
- Use strong, unique passwords
- Enable 2-factor authentication
- Use a password manager
- Stay safe online!

**Version**: 1.0.0 | **Updated**: January 27, 2026
