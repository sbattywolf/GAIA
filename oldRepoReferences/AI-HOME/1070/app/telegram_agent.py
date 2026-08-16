import os
from pathlib import Path

from home_intents import parse_home_intent
from home_resolver import (
    resolve_intent_to_plan,
    resolve_intent_to_query,
)

import httpx
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from env_loader import load, require
from home_aggregate import (
    CountResults,
    HomeAggregateService,
    HomeReport,
)
from home_config import load_max_entity_list
from ha_client import (
    EntityQuery,
    HAClient,
    format_entity_results,
)
from ollama_client import decide, parse_home_query
from response_formatter import ResponseFormatter
from storage import backlog, log, now, rid


BASE = Path(__file__).resolve().parent.parent
load(BASE)

TOKEN = require("TELEGRAM_BOT_TOKEN")
CHAT = int(require("TELEGRAM_ALLOWED_CHAT_ID"))
MODE = os.getenv("ZEUS_RUNTIME_MODE", "observe")

MODEL = require("OLLAMA_MODEL")
OLLAMA = require("OLLAMA_API_URL")

HA_AGENT_ID = (
    os.getenv("HOME_ASSISTANT_AGENT_ID", "").strip()
    or None
)

ha = HAClient(
    base_url=require("HOME_ASSISTANT_BASE_URL"),
    token=require("HOME_ASSISTANT_TOKEN"),
    agent_id=HA_AGENT_ID,
)

aggregate_service = HomeAggregateService()
MAX_ENTITY_LIST = load_max_entity_list()

sessions = {}
last_home_queries = {}
ha_conversations = {}


HOME_TERMS = (
    "casa",
    "home assistant",
    "finestra",
    "finestre",
    "porta",
    "porte",
    "luce",
    "luci",
    "sensore",
    "sensori",
    "interruttore",
    "interruttori",
    "temperatura",
    "termostato",
    "climate",
    "presenza",
    "movimento",
    "automazione",
    "automazioni",
)

FOLLOW_UP_TERMS = (
    "e quelle",
    "e quelli",
    "e quella",
    "e quello",
    "quelle aperte",
    "quelle chiuse",
    "quelli aperti",
    "quelli chiusi",
    "tutte",
    "tutti",
    "le altre",
    "gli altri",
)

ACTION_TERMS = (
    "accendi",
    "accendere",
    "spegni",
    "spegnere",
    "apri",
    "aprire",
    "chiudi",
    "chiudere",
    "imposta",
    "attiva",
    "disattiva",
    "adduma",
    "astuta",
)


async def start(update, context):
    if (
        update.effective_chat
        and update.effective_chat.id == CHAT
        and update.message
    ):
        await update.message.reply_text(
            "Zeus online in modalità " + MODE + "."
        )


async def reset_home(update, context):
    if (
        not update.effective_chat
        or update.effective_chat.id != CHAT
        or not update.message
    ):
        return

    ha_conversations.pop(CHAT, None)
    last_home_queries.pop(CHAT, None)

    await update.message.reply_text(
        "Conversazione Home Assistant azzerata."
    )


def merge_with_previous(
    chat_id,
    parsed,
    preserve_scope=False,
):
    previous = last_home_queries.get(chat_id)

    if previous is None:
        return parsed

    if preserve_scope:
        parsed.domain = previous.domain
        parsed.device_classes = list(
            previous.device_classes
        )
        parsed.name_terms = list(
            previous.name_terms
        )
        return parsed

    if not parsed.domain:
        parsed.domain = previous.domain

    if not parsed.device_classes:
        parsed.device_classes = list(
            previous.device_classes
        )

    if not parsed.name_terms:
        parsed.name_terms = list(
            previous.name_terms
        )

    return parsed


async def handle_home_read(chat_id, text):

    #
    # Fast deterministic path
    #
    intent = parse_home_intent(text)

    if intent.confidence >= 0.90:
        plan = resolve_intent_to_plan(intent)

        if plan:
            aggregate_results = (
                await aggregate_service.execute_plan(
                    ha,
                    plan,
                    MAX_ENTITY_LIST,
                )
            )

            if isinstance(
                aggregate_results,
                CountResults,
            ):
                return (
                    ResponseFormatter.format_count_results(
                        aggregate_results,
                    ),
                    True,
                    None,
                )

            if isinstance(
                aggregate_results,
                HomeReport,
            ):
                return (
                    ResponseFormatter.format_home_report(
                        aggregate_results,
                    ),
                    True,
                    None,
                )

        query = resolve_intent_to_query(intent)

        if query:

            results = await ha.query_entities(
                query
            )

            truncated = (
                aggregate_service.truncate_results(
                    results,
                    MAX_ENTITY_LIST,
                )
            )

            return (
                ResponseFormatter.format_truncated_state_results(
                    truncated,
                    intent.device_kind,
                    intent.desired_state,
                ),
                True,
                None,
            )

    #
    # Fallback LLM path
    #
    
    parsed = await parse_home_query(
        text,
        MODEL,
        OLLAMA,
    )

    lowered = text.lower()

    preserve_scope = any(
        term in lowered
        for term in FOLLOW_UP_TERMS
    )

    parsed = merge_with_previous(
        chat_id,
        parsed,
        preserve_scope=preserve_scope,
    )

    if not parsed.domain:
        return (
            "Non riesco a determinare il tipo di entità "
            "da controllare.",
            False,
            "INVALID_HOME_QUERY",
        )

    query = EntityQuery(
        domain=parsed.domain,
        device_classes=parsed.device_classes,
        states=parsed.states,
        name_terms=parsed.name_terms,
    )

    results = await ha.query_entities(query)

    if not results and parsed.name_terms:
        parsed.name_terms = []

        query = EntityQuery(
            domain=parsed.domain,
            device_classes=parsed.device_classes,
            states=parsed.states,
            name_terms=[],
        )

        results = await ha.query_entities(query)
        
    last_home_queries[chat_id] = parsed

    response = format_entity_results(
        results,
        parsed.requested_state_label,
    )

    return response, True, None


async def handle_home_action(chat_id, text):
    response, conversation_id, response_type = (
        await ha.process_conversation(
            text=text,
            conversation_id=ha_conversations.get(
                chat_id
            ),
            language="it",
        )
    )

    if conversation_id:
        ha_conversations[chat_id] = (
            conversation_id
        )

    return response, True, None


async def message(update, context):
    if (
        not update.effective_chat
        or update.effective_chat.id != CHAT
        or not update.message
        or not update.message.text
    ):
        return

    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    lowered = text.lower()

    explicit_home = any(
        term in lowered
        for term in HOME_TERMS
    )

    home_follow_up = (
        chat_id in last_home_queries
        and any(
            term in lowered
            for term in FOLLOW_UP_TERMS
        )
    )

    home_request = (
        explicit_home or home_follow_up
    )

    home_action = (
        home_request
        and any(
            term in lowered
            for term in ACTION_TERMS
        )
    )

    executed = False
    error = None
    tool = "none"

    try:
        if home_request:
            category = "HOME"
            target = "LOCAL"

            if MODE == "observe":
                action = "OBSERVE_HOME_REQUEST"
                response_text = (
                    "Ho riconosciuto una richiesta "
                    "Home Assistant, ma sono ancora "
                    "in modalità osservazione."
                )

            elif home_action:
                action = "HA_ACTION"
                tool = "ha_conversation"

                response_text, executed, error = (
                    await handle_home_action(
                        chat_id,
                        text,
                    )
                )

            else:
                action = "HA_STATE_QUERY"
                tool = "ha_query"

                response_text, executed, error = (
                    await handle_home_read(
                        chat_id,
                        text,
                    )
                )

        else:
            decision = await decide(
                text,
                MODEL,
                OLLAMA,
                sessions.get(chat_id, [])[-8:],
            )

            category = decision.category
            action = decision.action
            target = decision.target
            tool = decision.tool
            response_text = decision.response

            if target in {
                "BACKLOG",
                "RTX_3090",
            }:
                backlog({
                    "request_id": rid(),
                    "timestamp": now(),
                    "message": text,
                    "category": category,
                    "action": action,
                    "target": target,
                    "response": response_text,
                })

    except httpx.TimeoutException:
        error = "TIMEOUT"
        response_text = (
            "La richiesta non ha risposto "
            "entro il timeout."
        )

    except httpx.HTTPStatusError as exc:
        error = (
            "HTTP_"
            + str(exc.response.status_code)
        )
        response_text = (
            "Home Assistant ha rifiutato "
            "la richiesta."
        )

    except Exception as exc:
        error = type(exc).__name__
        response_text = (
            "Si è verificato un errore "
            "durante la richiesta."
        )

    record = {
        "schema_version": 4,
        "request_id": rid(),
        "timestamp": now(),
        "message": text,
        "category": category,
        "action": action,
        "target": target,
        "tool": tool,
        "mode": MODE,
        "executed": executed,
        "response": response_text,
        "error": error,
    }

    log(record)

    sessions.setdefault(chat_id, []).extend([
        {
            "role": "user",
            "content": text,
        },
        {
            "role": "assistant",
            "content": response_text,
        },
    ])

    sessions[chat_id] = (
        sessions[chat_id][-8:]
    )

    await update.message.reply_text(
        response_text
    )


async def error_handler(update, context):
    print(
        "Telegram error: "
        + type(context.error).__name__
        + ": "
        + str(context.error)
    )


def main():
    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CommandHandler(
            "reset_home",
            reset_home,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message,
        )
    )

    application.add_error_handler(
        error_handler
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
