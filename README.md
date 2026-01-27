# 🔐 Password Strength Checker

A professional-grade password security analyzer with real-time entropy calculation, breach detection, and advanced recommendations. Built with Python, Tkinter, and security best practices.

**Status**: ✅ Production Ready | **Version**: 1.0.0 | **License**: MIT

## 🎯 Features

### Core Analysis
- Real-time strength scoring (0-5 scale)
- Entropy calculation in bits
- Crack time estimates (online & offline)
- Pattern detection via zxcvbn
- Common password database (14K+)
- Breach checking (Have I Been Pwned API)
- Bcrypt hash generation

### User Interface
- Professional dark/light mode
- Real-time analysis feedback
- Color-coded strength indicators
- Emoji-based badges
- Non-resizable optimized window

### Advanced Features
- Password generator (12+ characters)
- History tracking (masked storage)
- Batch CSV processing
- PDF report export
- Offline support

## 🚀 Quick Start

### Clone & Install
```bash
# Clone repository
git clone https://github.com/yourusername/password-strength-checker.git
cd password-strength-checker

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
python gui_app.py
```

### CLI Usage
```bash
python cli_app.py "YourPasswordHere"
```

## 📋 Requirements

- Python 3.10+
- Windows/macOS/Linux
- Internet optional (for breach checking)

**Dependencies**: See `requirements.txt`

## 🔒 Security

- ✓ Local analysis (no uploads)
- ✓ K-anonymity for breach detection
- ✓ Masked password history
- ✓ Bcrypt hashing with salt
- ✓ Never stores raw passwords

## 📁 Project Structure

```
├── gui_app.py              # Main GUI application
├── password_core.py        # Core analysis engine
├── cli_app.py              # CLI interface
├── test_core.py            # Unit tests
├── common_passwords.txt    # 14K+ passwords
├── requirements.txt        # Dependencies
├── README.md               # This file
├── QUICKSTART.md           # Getting started
├── DEPLOYMENT.md           # Deployment guide
└── LICENSE                 # MIT License
```

## 🧪 Testing

```bash
# Run tests
python -m pytest test_core.py -v
```

## 🔨 Building EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "common_passwords.txt:." gui_app.py
```

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Docs map

## 🐛 Issues & Features

Found a bug? Have a feature request? Open an issue or submit a pull request!

## 🚀 Roadmap

- Code signing
- .MSI installer
- Auto-updates
- Cross-platform (macOS/Linux)
- Web version

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## ⚠️ Disclaimer

For educational purposes. Always use:
- Unique passwords per service
- Two-factor authentication
- Password managers for storage
- Updated software

---

**Version**: 1.0.0 | **Last Updated**: January 27, 2026 | 🔐 **Stay secure!**
