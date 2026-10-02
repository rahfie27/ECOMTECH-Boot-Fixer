<img src="https://www.upload.ee/image/19807858/2026-10-02_075416.png" border="0" alt="2026-10-02_075416.png" />

# ECOMTECH BOOT Fixer

A Windows boot repair and system recovery utility built with Python and PyQt.
ECOMTECH BOOT Fixer provides a simple graphical interface to help diagnose and repair common Windows boot-related issues.

## 🚀 Features

* 🖥️ User-friendly graphical interface
* 🔧 Windows boot repair tools
* ⚙️ System recovery assistance
* 📋 Easy access to repair commands
* 🛠️ Built with Python and PyQt
* 📦 Ready for packaging with PyInstaller

## 📂 Project Structure

```
ECOMTECH_BOOT_Fixer/
│
├── ECOMTECH_boot_fixer.py      # Main application
├── requirements.txt            # Runtime dependencies
├── requirements-build.txt      # Build dependencies
├── icons/                      # Application icons
├── .gitignore                  # Git ignored files
└── README.md                   # Project documentation
```

## 🖥️ Requirements

* Windows 10 / Windows 11
* Python 3.10 or newer
* Administrator privileges (required for system repair operations)

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ECOMTECH_BOOT_Fixer.git
cd ECOMTECH_BOOT_Fixer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run Application

Start the application:

```bash
python ECOMTECH_boot_fixer.py
```

Run as Administrator for full repair functionality.

## 📦 Build Executable

Install build requirements:

```bash
pip install -r requirements-build.txt
```

Build using PyInstaller:

```bash
pyinstaller --onefile --windowed ECOMTECH_boot_fixer.py
```

The executable will be created inside:

```
dist/
```

## 🔐 Permissions

Some features require administrator access because Windows boot repair operations modify system configuration.

## ⚠️ Disclaimer

This tool performs system repair operations. Always create a backup or restore point before making major system changes.

Use at your own risk.

## 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork this repository
2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push your branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

## 📄 License

Add your preferred license before publishing.

Example:

MIT License

## 👨‍💻 Author

ECOMTECH

---

⭐ If this project helps you, consider giving it a star on GitHub.
