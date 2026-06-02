# 🚀 Installation

You can install ShieldEye on any Debian-based distribution (Ubuntu, Kali, Mint, etc.), Windows 10, 11 by following these steps:

## Method 1: Using Terminal

- Run the following in your terminal:

### Linux OS

[**Using apt**]

```bash
sudo apt update
wget "https://github.com/holoolagoke/shield-eye-desktop/releases/download/v1.1.0/shieldeye_1.1.0_amd64.deb"
sudo apt install ./shieldeye_1.1.0_amd64.deb
```

[**Using dpkg**]

If you prefer the standard Debian package tool:

```bash
wget "https://github.com/holoolagoke/shield-eye-desktop/releases/download/v1.1.0/shieldeye_1.1.0_amd64.deb"
sudo dpkg -i shieldeye_1.1.0_amd64.deb
sudo apt-get install -f
```

### Windows OS

Download the installer using your browser or PowerShell:

```powershell
curl -L -o shieldeye_1.1.0_setup.exe "https://github.com/holoolagoke/shield-eye-desktop/releases/download/v1.1.0/shieldeye_1.1.0_setup.exe"
```

Then double-click `shieldeye_1.1.0_setup.exe` to run the installer.

## Method 2: Using GUI

- Download the [latest version](https://github.com/holoolagoke/shield-eye-desktop/releases/latest) for your OS
- Execute the setup file

## 🛠 Usage

Once installed, you can launch the app from your application menu or via the terminal:

```bash
shieldeye
```

## How to uninstall

### Linux

[**Delete App Only, Keep Data**]

```bash
sudo apt remove shieldeye
```

[**Delete Both App and Data**]

```bash
sudo apt purge shieldeye
```

### Windows

```bash
winget uninstall shieldeye
```

[**Delete Both App and Data**]

Uninstall the app first, then manually delete the data folder:

1. Run: `winget uninstall shieldeye`
2. Delete the data folder at: `C:\Users\<YourName>\AppData\Roaming\ShieldEye`
