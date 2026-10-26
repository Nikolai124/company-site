import html
import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

log = logging.getLogger(__name__)


def notify_new_lead(lead) -> None:
    """Шлёт заявку в Telegram. Если что-то сломалось, заявка всё равно уже сохранена в базе."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return

    text = (
        "🧽 <b>Новая заявка с сайта</b>\n\n"
        f"<b>Имя:</b> {html.escape(lead.name)}\n"
        f"<b>Телефон:</b> {html.escape(lead.phone)}\n"
        f"<b>Услуга:</b> {html.escape(str(lead.service or '—'))}\n"
        f"<b>Комментарий:</b> {html.escape(lead.comment or '—')}"
    )
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode(
        {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    ).encode()
    try:
        with urllib.request.urlopen(url, data=payload, timeout=5) as response:
            json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        # Печатаем только тип ошибки: в тексте может оказаться URL с токеном
        log.warning("Не удалось отправить заявку в Telegram: %s", type(error).__name__)
