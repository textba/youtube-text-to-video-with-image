import os
import requests


def upload_video_to_tiktok(file_path: str, title: str, description: str = ""):
    """
    TikTok Content Posting API scaffold.
    Requires a valid user access token with video publish permissions.

    Env required:
      TIKTOK_ACCESS_TOKEN
      TIKTOK_API_BASE (optional, default https://open.tiktokapis.com)

    Note: Depending on your app setup, TikTok may require chunked upload flow.
    This helper uses a simple direct-upload flow and returns status details.
    """
    access_token = os.environ.get("TIKTOK_ACCESS_TOKEN", "")
    api_base = os.environ.get("TIKTOK_API_BASE", "https://open.tiktokapis.com")

    if not access_token:
        return {"ok": False, "status": "missing token", "url": None}

    # 1) Initialize upload session
    init_url = f"{api_base}/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    init_payload = {
        "post_info": {
            "title": title[:150],
            "description": description[:2200],
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": os.path.getsize(file_path),
            "chunk_size": os.path.getsize(file_path),
            "total_chunk_count": 1,
        },
    }

    try:
        init_resp = requests.post(init_url, json=init_payload, headers=headers, timeout=60)
        init_data = init_resp.json() if init_resp.content else {}
        if init_resp.status_code >= 300:
            return {"ok": False, "status": f"init failed: {init_resp.status_code}", "detail": init_data, "url": None}

        upload_url = (((init_data or {}).get("data") or {}).get("upload_url"))
        publish_id = (((init_data or {}).get("data") or {}).get("publish_id"))
        if not upload_url:
            return {"ok": False, "status": "missing upload_url", "detail": init_data, "url": None}

        # 2) Upload bytes
        with open(file_path, "rb") as f:
            upload_resp = requests.put(upload_url, data=f, timeout=300)
        if upload_resp.status_code >= 300:
            return {"ok": False, "status": f"upload failed: {upload_resp.status_code}", "url": None}

        # 3) Return publish id for manual verification/polling
        return {
            "ok": True,
            "status": "uploaded",
            "publishId": publish_id,
            "url": None,
        }

    except Exception as e:
        return {"ok": False, "status": f"error: {e}", "url": None}
