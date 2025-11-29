# TalkyBoi

Audio dictation app that transcribes speech using Gemini API and cleans up filler words.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` with your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```

Optionally specify a different Gemini model:
```
GEMINI_MODEL=gemini-2.5-flash
```

## Usage

### Normal Mode

```bash
python main.py
```

- Hold **F5** or click the button to record
- Release to transcribe
- Text accumulates in the window
- **Ctrl+L** to clear, **Ctrl+Shift+C** to copy all

### Quick Record Mode (Voice to Clipboard)

```bash
python main.py --quick
```

A minimal floating window appears:
1. Recording starts immediately
2. Speak your text
3. Press **Escape** or click **Stop**
4. Text is transcribed and copied to clipboard
5. Window closes automatically

Perfect for quickly capturing voice notes!

## Global Shortcut Setup (GNOME/Wayland)

Set up a keyboard shortcut to launch quick record from anywhere:

1. Open **Settings > Keyboard > Keyboard Shortcuts**
2. Scroll to **Custom Shortcuts**
3. Click **+** to add:
   - **Name:** TalkyBoi Quick Record
   - **Command:** `/home/nbhansen/dev/TalkyBoi/talkyboi.sh --quick`
   - **Shortcut:** Your choice (e.g., `Super+T` or `Ctrl+Alt+R`)

Now press your shortcut from anywhere to start recording!

## Desktop Entry

To add to your application menu:
```bash
cp talkyboi.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

Right-click the app icon for a "Quick Record" action.
