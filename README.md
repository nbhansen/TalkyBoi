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

## Usage

```bash
source venv/bin/activate
python main.py
```

- Hold **F5** or click the button to record
- Release to transcribe
- Text accumulates in the window

## Desktop Entry

To add to your application menu:
```bash
cp talkyboi.desktop ~/.local/share/applications/
```
