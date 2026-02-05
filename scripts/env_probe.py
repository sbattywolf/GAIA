#!/usr/bin/env python3
import os

def main():
    tok = bool(os.getenv('TELEGRAM_BOT_TOKEN'))
    chat = os.getenv('TELEGRAM_CHAT_ID')
    print('TOK_PRESENT', tok)
    print('CHAT', chat)

if __name__ == '__main__':
    main()
