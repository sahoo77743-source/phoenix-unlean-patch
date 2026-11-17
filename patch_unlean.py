#!/usr/bin/env python3
"""Remove the 1/3 impulse entry. Keep the 45-minute slow-lane block."""
import os
import shutil
import py_compile

TARGET = "main.py"
BACKUP = "main.py.bak_unlean"

OLD = """        ok_idx, why_idx = index_entry_allowed(idx_now, side)
        if not ok_idx:
            direction = str((idx_now or {}).get("direction") or "NEUTRAL").upper()
            agree = int((idx_now or {}).get("agree") or 0)
            lean_ok = agree == 1 and (
                (side == "BUY" and direction == "BULL")
                or (side == "SELL" and direction == "BEAR")
            )
            if not lean_ok:
                logger.info(f"🚫 IMPULSE index {symbol} | {why_idx}")
                return
            logger.info(f"⚡ IMPULSE lean {symbol} | {direction} {agree}/3 {side}")
"""

NEW = """        ok_idx, why_idx = index_entry_allowed(idx_now, side)
        if not ok_idx:
            logger.info(f"🚫 IMPULSE index {symbol} | {why_idx}")
            return
"""


def main():
    if not os.path.exists(TARGET):
        print(f"STOPPED missing {TARGET}")
        return
    shutil.copy2(TARGET, BACKUP)
    text = open(TARGET, encoding="utf-8").read()
    if text.count(OLD) != 1:
        shutil.copy2(BACKUP, TARGET)
        print(f"STOPPED lean block count={text.count(OLD)}")
        print(f"restored from {BACKUP} — bot file was not changed")
        return
    if "def slow_lane_blocked" not in text:
        shutil.copy2(BACKUP, TARGET)
        print("STOPPED the 45m block is missing — bot file was not changed")
        return
    text = text.replace(OLD, NEW, 1)
    if "IMPULSE lean" in text or "def slow_lane_blocked" not in text:
        shutil.copy2(BACKUP, TARGET)
        print("STOPPED result check failed")
        print(f"restored from {BACKUP} — bot file was not changed")
        return
    open(TARGET, "w", encoding="utf-8").write(text)
    try:
        py_compile.compile(TARGET, doraise=True)
    except Exception as e:
        shutil.copy2(BACKUP, TARGET)
        print(f"STOPPED compile: {e}")
        print(f"restored from {BACKUP} — bot file was not changed")
        return
    print("DONE pieces=1")
    print(f"backup={BACKUP}")


if __name__ == "__main__":
    main()
