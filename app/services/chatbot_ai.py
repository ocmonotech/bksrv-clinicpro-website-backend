import os
from typing import Any

import requests


CLINICPRO_SYSTEM_PROMPT = """
You are ClinicPro's website assistant for clinics and healthcare practices in India.

ClinicPro is clinic management software by ocmono. Help visitors with product questions only.

Product facts you can use:
- Plans: Starter ₹599/month (₹5,990/year), Professional ₹1,299/month (₹12,990/year), Enterprise ₹2,299/month (₹22,990/year). GST may apply.
- Features: patient management, EMR/clinical notes, appointments, billing & invoices, telehealth, inventory/pharmacy, reminders, multi-location, role-based access.
- Security: encrypted records, role-based access, HIPAA-ready infrastructure.
- Visitors can book a demo, view pricing, explore specialties, contact support, or open WhatsApp.

Rules:
- Be concise, friendly, and practical (2–5 short sentences unless asked for detail).
- Do not invent features, prices, or guarantees.
- If unsure, suggest booking a demo or contacting support.
- Never ask for patient medical details or PHI.
- Do not mention that you are an AI model unless asked.
- Prefer Indian clinic context when relevant.
""".strip()


def openai_enabled() -> bool:
    return bool((os.getenv("OPENAI_API_KEY") or "").strip())


def _openai_model() -> str:
    return (os.getenv("OPENAI_MODEL") or "gpt-4o-mini").strip()


def _default_options() -> list[dict[str, Any]]:
    return [
        {"id": "demo", "label": "Book a demo", "action": "demo"},
        {"id": "pricing", "label": "Pricing & plans", "action": "pricing"},
        {"id": "contact", "label": "Contact support", "action": "contact"},
        {"id": "back-main", "label": "Main menu", "action": "main"},
    ]


def _infer_options(reply: str) -> list[dict[str, Any]]:
    lower = (reply or "").lower()
    options: list[dict[str, Any]] = []

    if any(word in lower for word in ("demo", "walkthrough", "onboarding")):
        options.append({"id": "demo", "label": "Book a demo", "action": "demo"})
    if any(word in lower for word in ("price", "pricing", "plan", "₹", "rs")):
        options.append({"id": "pricing", "label": "View pricing", "action": "pricing"})
    if any(word in lower for word in ("security", "hipaa", "encrypt")):
        options.append(
            {"id": "nav-security", "label": "Open Security", "action": "navigate", "href": "/security"}
        )
    if any(word in lower for word in ("feature", "emr", "appointment", "billing")):
        options.append(
            {"id": "nav-features", "label": "Browse features", "action": "navigate", "href": "/features"}
        )
    if any(word in lower for word in ("contact", "support", "whatsapp", "call")):
        options.append({"id": "contact", "label": "Contact support", "action": "contact"})

    if not options:
        return _default_options()

    options.append({"id": "back-main", "label": "Main menu", "action": "main"})
    # de-dupe by id
    seen = set()
    unique = []
    for item in options:
        key = item.get("id")
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique[:5]


def ask_openai(*, message: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Call OpenAI Chat Completions. Returns {reply, options, source}."""
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    messages: list[dict[str, str]] = [{"role": "system", "content": CLINICPRO_SYSTEM_PROMPT}]

    for item in (history or [])[-8:]:
        role = item.get("role")
        text = (item.get("text") or "").strip()
        if not text:
            continue
        if role == "user":
            messages.append({"role": "user", "content": text[:2000]})
        elif role in {"bot", "assistant"}:
            messages.append({"role": "assistant", "content": text[:2000]})

    messages.append({"role": "user", "content": message.strip()[:2000]})

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": _openai_model(),
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 450,
        },
        timeout=45,
    )

    if response.status_code >= 400:
        try:
            payload = response.json()
            api_message = ((payload.get("error") or {}).get("message") or response.text)[:400]
            api_type = (payload.get("error") or {}).get("type") or ""
        except Exception:
            api_message = response.text[:400]
            api_type = ""

        if response.status_code == 429 or "insufficient_quota" in api_type or "quota" in api_message.lower():
            raise RuntimeError(
                "OpenAI quota exceeded (429). Add billing/credits at https://platform.openai.com/account/billing"
            )
        if response.status_code == 401:
            raise RuntimeError("OpenAI API key is invalid (401). Check OPENAI_API_KEY.")
        raise RuntimeError(f"OpenAI error ({response.status_code}): {api_message}")

    data = response.json()
    reply = (
        ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    ).strip()

    if not reply:
        raise RuntimeError("OpenAI returned an empty reply")

    return {
        "reply": reply,
        "options": _infer_options(reply),
        "source": "openai",
        "model": _openai_model(),
    }
