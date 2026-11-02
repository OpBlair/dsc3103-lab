import json
import time

BROKER = "data/stream/events.jsonl"
LATE_LOG = "data/stream/late_events.jsonl"
DUP_LOG = "data/stream/duplicate_events.jsonl"

WINDOW = 10        # tumbling window length, seconds
WATERMARK = 20     # how long we wait for late events, seconds (5, 20, 40)
IDLE_STOP = 45     # stop when no new events arrive for this long


def window_start(event_time):
    return int(event_time // WINDOW) * WINDOW

def append(path, record):
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")

def consume():
    for p in (LATE_LOG, DUP_LOG):
        open(p, "w").close()

    offset = 0               # how many lines we have already read
    windows = {}             # window start -> {"n": count, "total": sum of prices}
    finalised = set()        # windows we have already reported
    seen_ids = set()         # event ids we have already counted
    last_new = time.time()

    while time.time() - last_new < IDLE_STOP:
        # 1. read any new lines from the log
        with open(BROKER) as f:
            lines = f.readlines()
        new_lines = lines[offset:]
        offset = len(lines)
        if new_lines:
            last_new = time.time()

        # 2. process each event
        for line in new_lines:
            event = json.loads(line)
            now = time.time()

            # TODO A (duplicates): if event["event_id"] is already in seen_ids,
            #   write the event to DUP_LOG with append() and skip it (continue).
            #   Otherwise add its id to seen_ids.
            if event["event_id"] in seen_ids:
                append(DUP_LOG, event)
                continue
            seen_ids.add(event["event_id"])
            
            ws = window_start(event["event_time"])
            
            # TODO B (late data): the event is LATE if its window is already in
            #   "finalised", OR if now >= ws + WINDOW + WATERMARK.
            #   Write late events to LATE_LOG with a "reason" field and skip them.
            if ws in finalised or now >= ws + WINDOW + WATERMARK:
                reason = "finalised" if ws in finalised else "watermark exceeded"
                late_event = {**event, "reason": reason}
                append(LATE_LOG, late_event)
                continue

            # TODO C (windowing): add the event to windows[ws]:
            #   increase "n" by 1 and "total" by the event's price.
            #   Hint: windows.setdefault(ws, {"n": 0, "total": 0.0})
            w = windows.setdefault(ws, {"n": 0, "total": 0.0})
            w["n"] += 1
            w["total"] += event["price"]

        # 3. finalise windows whose end + watermark has passed
        now = time.time()
        for ws in sorted(windows):
            # TODO D (output): if ws is not finalised and
            #   now >= ws + WINDOW + WATERMARK, print the window's start time,
            #   event count and mean price, then add ws to "finalised".
            if ws not in finalised and now >= ws + WINDOW + WATERMARK:
                w = windows[ws]
                mean_price = w["total"] / w["n"] if w["n"] > 0 else 0.0
                print(f"Window {ws}: count={w['n']}, mean_price={mean_price:.2f}")

                window_end = ws + WINDOW
                actual_delay = now - window_end
                print(f"Window {ws} ended at {window_end}, printed at {now:.1f}. Delay: {actual_delay:.1f}s")

                finalised.add(ws)

        time.sleep(0.2)

    print("Consumer idle, stopping. Late:", sum(1 for _ in open(LATE_LOG)),
          "| Duplicates:", sum(1 for _ in open(DUP_LOG)))


if __name__ == "__main__":
    consume()