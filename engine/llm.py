import re
from typing import List, Tuple

from requests import HTTPError

from .common import clean_strings, env, get_json, log, parse_json, post_json, require_env
from .constants import (
    GEMINI_MODEL,
    GEMINI_URL,
    LLM_TIMEOUT,
    METADATA_PROMPT,
    SCRIPT_PROMPT,
    TERMS_PROMPT,
    VERTEX_KEY_PREFIX,
    VERTEX_URL,
)


def default_model() -> str:
    return env("GEMINI_MODEL", GEMINI_MODEL)


def _key() -> str:
    require_env("GEMINI_API_KEY")
    return env("GEMINI_API_KEY")


def _is_vertex(key: str) -> bool:
    return key.startswith(VERTEX_KEY_PREFIX)


def _error(err: HTTPError) -> RuntimeError:
    status = err.response.status_code if err.response is not None else "?"
    try:
        message = err.response.json()["error"]["message"]
    except Exception:
        message = "request failed"
    hint = ""
    if status == 404:
        hint = " Check GEMINI_MODEL, or use an AI Studio key (starts with AIza) from https://aistudio.google.com/apikey."
    return RuntimeError(f"Gemini {status}: {message}{hint}")


def list_models() -> List[str]:
    key = _key()
    if _is_vertex(key):
        return [default_model()]
    try:
        data = get_json(GEMINI_URL, headers={"x-goog-api-key": key}, params={"pageSize": 100})
    except HTTPError as err:
        raise _error(err) from None
    return [
        model["name"].removeprefix("models/")
        for model in data.get("models", [])
        if "generateContent" in model.get("supportedGenerationMethods", [])
    ]


def complete(prompt: str, model: str = "", json_mode: bool = False) -> str:
    key = _key()
    base = VERTEX_URL if _is_vertex(key) else GEMINI_URL
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if json_mode:
        payload["generationConfig"] = {"responseMimeType": "application/json"}
    try:
        data = post_json(
            f"{base}/{model or default_model()}:generateContent",
            payload,
            headers={"x-goog-api-key": key},
            timeout=LLM_TIMEOUT,
        )
    except HTTPError as err:
        raise _error(err) from None
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as err:
        reason = data.get("promptFeedback", {}).get("blockReason") or data.get("candidates", [{}])[0].get("finishReason")
        raise RuntimeError(f"Gemini returned no content ({reason or 'unknown reason'}).") from err
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def complete_json(prompt: str, model: str = "") -> dict:
    return parse_json(complete(prompt, model, json_mode=True))


def generate_script(subject: str, paragraphs: int, voice: str, custom_prompt: str = "", model: str = "") -> str:
    prompt = custom_prompt or SCRIPT_PROMPT.format(subject=subject, paragraphs=paragraphs, language=voice[:2])
    if custom_prompt:
        prompt += f"\n\nSubject: {subject}\nParagraphs: {paragraphs}\nLanguage code: {voice[:2]}"
    text = complete(prompt, model).replace("*", "").replace("#", "")
    text = re.sub(r"\[.*?\]|\(.*?\)", "", text)
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    script = "\n\n".join(chunks[:paragraphs])
    if not script:
        raise RuntimeError("Could not generate a script.")
    log(f"[+] Script generated ({len(chunks[:paragraphs])} paragraph(s))", "success")
    return script


def search_terms(subject: str, script: str, amount: int, model: str = "") -> List[str]:
    data = complete_json(TERMS_PROMPT.format(subject=subject, script=script, amount=amount), model)
    terms = clean_strings(data.get("terms", []))[:amount] or [subject]
    log(f"[+] Search terms: {', '.join(terms)}", "info")
    return terms


def metadata(subject: str, script: str, model: str = "") -> Tuple[str, str, List[str]]:
    data = complete_json(METADATA_PROMPT.format(subject=subject, script=script), model)
    title = str(data.get("title") or subject).strip()
    description = str(data.get("description") or script[:200]).strip()
    keywords = clean_strings(data.get("keywords", []))[:10]
    return title, description, keywords
