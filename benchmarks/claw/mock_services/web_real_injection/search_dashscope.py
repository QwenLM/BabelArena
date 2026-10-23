"""
Search via DashScope web-search API (google-serper-inner)

POST https://dashscope.aliyuncs.com/api/v1/services/search/web-search/text-search
Headers:
    Authorization: <DASHSCOPE_SEARCH_KEY>
    Content-Type:  application/json
Body:
    model:      "google-serper-inner"
    input.query: <query>
    input.page:  <int, 1-based>
    input.rows:  <int, 1-10>
    parameters.timeout: <int, milliseconds>

Env vars:
    DASHSCOPE_SEARCH_KEY  — DashScope API key (required)
    DASHSCOPE_SEARCH_URL  — API endpoint (default: official URL)
    DASHSCOPE_SEARCH_MODEL — model name (default: google-serper-inner)

Input:  query (str), timeout (int), num (int), start (int)
Output: {"status": <int>, "output": <list[dict]>}
        Same shape as search_serp for drop-in compatibility.
"""

import os
import sys
import requests

DASHSCOPE_SEARCH_URL = os.getenv(
    "DASHSCOPE_SEARCH_URL",
    "https://dashscope.aliyuncs.com/api/v1/services/search/web-search/text-search",
)
DASHSCOPE_SEARCH_KEY = os.getenv("DASHSCOPE_SEARCH_KEY", "")
DASHSCOPE_SEARCH_MODEL = os.getenv("DASHSCOPE_SEARCH_MODEL", "google-serper-inner")


def search_dashscope(
    query: str,
    timeout: int = 20,
    num: int = 10,
    start: int = 1,
    raw_save_path: str | None = None,
) -> dict:
    """Search via DashScope web-search API and return extracted results.

    Args:
        query: Search query string.
        timeout: Request timeout in seconds.
        num: Number of results (1-10).
        start: 1-based page offset (mapped to input.page).

    Returns:
        dict with keys:
            status (int): HTTP status code, or -1 on error.
            output (list[dict]): List of result dicts with keys:
                title, link, snippet, date, query.
    """
    if not DASHSCOPE_SEARCH_KEY:
        print(f"[search_dashscope] DASHSCOPE_SEARCH_KEY is empty, returning -1", file=sys.stderr)
        return {"status": -1, "output": []}

    headers = {
        "Authorization": f"Bearer {DASHSCOPE_SEARCH_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": DASHSCOPE_SEARCH_MODEL,
        "input": {
            "query": query,
            "page": max(start, 1),
            "rows": min(max(num, 1), 10),
        },
        "parameters": {
            "timeout": timeout * 1000,
        },
    }

    try:
        print(f"[search_dashscope] POST {DASHSCOPE_SEARCH_URL} query={query!r} rows={body['input']['rows']}",
              file=sys.stderr)
        resp = requests.post(
            DASHSCOPE_SEARCH_URL,
            headers=headers,
            json=body,
            timeout=timeout,
        )
        print(f"[search_dashscope] response status={resp.status_code} len={len(resp.text)}",
              file=sys.stderr)
        if raw_save_path and resp.status_code == 200:
            os.makedirs(os.path.dirname(raw_save_path) or ".", exist_ok=True)
            with open(raw_save_path, "w", encoding="utf-8") as f:
                f.write(resp.text)
        if resp.status_code != 200:
            print(f"[search_dashscope] non-200 body: {resp.text[:500]}", file=sys.stderr)
            return {"status": resp.status_code, "output": []}

        data = resp.json().get("output", {}).get("data", {})
        docs = data.get("docs", [])
        print(f"[search_dashscope] parsed docs_count={len(docs)}", file=sys.stderr)
        results = [
            {
                "title": item.get("title", ""),
                "link": item.get("url", ""),
                "snippet": item.get("snippet", ""),
                "date": "",
                "query": query,
            }
            for item in docs
        ]
        return {"status": resp.status_code, "output": results}
    except Exception as exc:
        print(f"[search_dashscope] exception: {type(exc).__name__}: {exc}", file=sys.stderr)
        return {"status": -1, "output": []}


if __name__ == "__main__":
    import json

    result = search_dashscope("Python web scraping", num=3)
    print(f"status={result['status']}  count={len(result['output'])}")
    print(json.dumps(result["output"], indent=2, ensure_ascii=False)[:1000])
