# youtube-text-to-video-with-image

Minimal working version of the current YouTube text-to-video app.

## Included files only
- `index.html`
- `api/app.py`
- `api/youtube_uploader.py`
- `api/youtube_auth.py`
- `api/drive_uploader.py`
- `api/tiktok_uploader.py`
- `requirements.txt`

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in project root if needed for optional integrations.

Run:
```bash
cd api
python app.py
```

Server runs on `http://127.0.0.1:5000`.
