"""One-shot script to expire old pending commands.

Usage: python scripts/expire_pending.py
"""
import sys
sys.path.insert(0, '.')
from scripts import tg_command_manager as tcm

def main():
    tcm.expire_old()
    print('expire_old run complete')

if __name__ == '__main__':
    main()
