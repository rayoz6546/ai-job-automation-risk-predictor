# src/clients/aws_client.py

import json
import requests


def call_aws_api(job_title: str, api_base_url: str, api_key: str) -> dict:
    if not api_base_url or not api_key:
        raise ValueError("Missing API_BASE_URL or API_KEY")

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {"jobTitle": job_title}

    response = requests.post(
        api_base_url,
        json=payload,
        headers=headers,
        timeout=30,
    )

    try:
        data = response.json()
    except Exception:
        data = {"raw_response": response.text}

    if response.status_code != 200:
        raise ValueError(f"AWS API error ({response.status_code}): {data}")

    if "body" in data:
        body = data["body"]

        if isinstance(body, str):
            try:
                return json.loads(body)
            except Exception:
                return {"raw_body": body}

        return body

    return data