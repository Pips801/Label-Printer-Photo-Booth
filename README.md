# Photo Booth + QZ Tray (Multi-Platform Setup)

This guide sets up the app on Windows, macOS, and Linux without changing any code.

## Requirements

- QZ Tray installed
- Printer driver installed
- Python 3.11+
- A browser (Chrome/Edge recommended)

## One-Time QZ Certificate Setup (All OS)

QZ Tray requires a trusted certificate and a private key.

1) Open QZ Tray
2) Advanced -> Site Manager
3) Click + to create a new site
4) Accept prompts to generate demo keys

QZ Tray will create two files:
- digital-certificate.txt
- private-key.pem

Keep note of the folder where these files are saved.

## Project Setup (All OS)

1) Create a virtual environment

Windows:
  python -m venv .venv
  .venv\Scripts\activate

macOS/Linux:
  python3 -m venv .venv
  source .venv/bin/activate

2) Install dependencies

  pip install -r requirements.txt

3) Set environment variables to point at the QZ files

Windows (PowerShell):
  setx QZ_CERT_PATH "C:\path\to\digital-certificate.txt"
  setx QZ_KEY_PATH "C:\path\to\private-key.pem"

macOS/Linux (bash/zsh):
  export QZ_CERT_PATH="/path/to/digital-certificate.txt"
  export QZ_KEY_PATH="/path/to/private-key.pem"

Note: On Windows, close and reopen the terminal after setx.

## Run the App

Windows:
  python app.py

macOS/Linux:
  python3 app.py

Then open:
  http://127.0.0.1:8000

## Kiosk Mode (Optional)

Windows (Chrome):
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk http://127.0.0.1:8000 --incognito --start-fullscreen

macOS (Chrome):
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk http://127.0.0.1:8000 --incognito

Linux (Chrome):
  google-chrome --kiosk http://127.0.0.1:8000 --incognito

## Troubleshooting

- If QZ Tray shows "Untrusted website" or "Invalid signature":
  - Confirm the QZ demo certs were generated via Site Manager on that machine.
  - Verify QZ_CERT_PATH and QZ_KEY_PATH point to those exact files.
  - Restart QZ Tray and the app.

- If no printers appear:
  - Verify QZ Tray is running.
  - Check browser console for QZ errors.

## Notes

- QZ Tray 2.1+ expects SHA512 signatures (handled by the app).
- The demo certs only work on the machine where they were created.
