"""Simple i18n helper for English/Italian translations.

Provides language detection by message prefix (e.g., `it:` or `/it `)
and a small translations table used by the bot and listener.
"""
from typing import Tuple

TRANSLATIONS = {
    'en': {
        'approval_requested': 'Approval requested:',
        'note_execution_disabled': 'Note: execution is disabled by default (ALLOW_COMMAND_EXECUTION=1 to enable).',
        'approve': 'Approve',
        'deny': 'Deny',
        'info': 'Info',
        'proceed_disabled': 'Proceed (disabled)',
        'proceed_disabled_test': '🔴 Proceed (disabled - TEST)',
        'received': 'Received',
        'command_approved': 'Command approved:',
        'to_execute': 'To execute: '
    },
    'it': {
        'approval_requested': 'Approvazione richiesta:',
        'note_execution_disabled': "Nota: l'esecuzione è disabilitata per impostazione predefinita (impostare ALLOW_COMMAND_EXECUTION=1 per abilitare).",
        'approve': 'Approva',
        'deny': 'Nega',
        'info': 'Info',
        'proceed_disabled': 'Procedi (disabilitato)',
        'proceed_disabled_test': '🔴 Procedi (disabilitato - TEST)',
        'received': 'Ricevuto',
        'command_approved': 'Comando approvato:',
        'to_execute': 'Per eseguire: '
    }
}


def detect_and_strip_prefix(text: str, env: dict = None) -> Tuple[str, str]:
    """Detect language prefix in text. Returns (lang, cleaned_text).

    Recognizes prefixes: `it:`, `/it `, `lang:it` at start (case-insensitive).
    Falls back to `TELEGRAM_DEFAULT_LANG` in env or 'en'.
    """
    if not text:
        default = (env or {}).get('TELEGRAM_DEFAULT_LANG') if env else None
        return (default or 'en', text)
    s = text.strip()
    ls = s.lower()
    if ls.startswith('it:'):
        return ('it', s[len('it:'):].lstrip())
    if ls.startswith('/it '):
        return ('it', s[len('/it '):].lstrip())
    if ls.startswith('lang:it'):
        return ('it', s[len('lang:it'):].lstrip())
    # fallback to env default
    default = (env or {}).get('TELEGRAM_DEFAULT_LANG') if env else None
    return (default or 'en', text)


def t(key: str, lang: str = 'en') -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
