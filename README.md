# TalkyBoi

Audio dictation app with multi-provider transcription support: Gemini, OpenAI Whisper, or local Whisper.

## Installation

```bash
git clone https://github.com/nbhansen/TalkyBoi.git
cd TalkyBoi
pip install .
```

This installs `talkyboi` and `talkyboi-quick` commands with Gemini as the default provider.

### Optional providers

```bash
pip install .[openai]     # Add OpenAI Whisper API support
pip install .[whisper]    # Add local Whisper support (no API needed)
pip install .[all]        # Install all providers
```

### Development setup

```bash
git clone https://github.com/nbhansen/TalkyBoi.git
cd TalkyBoi
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create `.env` in the project directory:

### Gemini (default)

```
TRANSCRIPTION_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash  # optional
```

Gemini cleans up filler words (um, uh, like) automatically.

### OpenAI Whisper API

```
TRANSCRIPTION_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

### Local Whisper

```
TRANSCRIPTION_PROVIDER=whisper
WHISPER_MODEL=base  # optional: tiny, base, small, medium, large-v2, large-v3
```

No API key required. First run downloads the model (~150MB for base).

## Usage

### Normal Mode

```bash
talkyboi              # if installed via pip
python main.py        # if running from source
```

- Hold **Right Ctrl** or click the button to record
- Release to transcribe
- Text accumulates in the window
- **Ctrl+L** to clear, **Ctrl+Shift+C** to copy all

### Quick Record Mode (Voice to Clipboard)

```bash
talkyboi-quick        # if installed via pip
python main.py --quick  # if running from source
```

A minimal floating window appears:
1. Recording starts immediately
2. Speak your text
3. Press **Escape** or click **Stop**
4. Text is transcribed and copied to clipboard
5. Window closes automatically

## Global Shortcut Setup (GNOME/Wayland)

Set up a keyboard shortcut to launch quick record from anywhere:

1. Open **Settings > Keyboard > Keyboard Shortcuts**
2. Scroll to **Custom Shortcuts**
3. Click **+** to add:
   - **Name:** TalkyBoi Quick Record
   - **Command:** `talkyboi-quick` (or full path to `talkyboi.sh --quick`)
   - **Shortcut:** Your choice (e.g., `Super+T` or `Ctrl+Alt+R`)

Now press your shortcut from anywhere to start recording!

## Desktop Entry

To add to your application menu:
```bash
cp talkyboi.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

Right-click the app icon for a "Quick Record" action.
