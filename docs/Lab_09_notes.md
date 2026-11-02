# Lab 09 notes

## Why the producer sometimes makes event_time earlier than current_time
This is done to simulate late-arriving data (or out-of-order events), where an event occurs at point $A$ in time, but due to network issues or transmission lag, it doesn't reach the stream processor until point $B$.

### Real-World Example: Uber Driver in a Basement Garage
Imagine an Uber driver dropping off a passenger in a subterranean parking garage where cellular service drops out completely:

* **Local Buffering:** The driver's phone keeps recording trip status and location pings locally, stamping each with the exact moment it occurred (`event_time`).
* **The Delay:** A short while later, the driver pulls out onto the open street and cellular connection is restored, flushing the buffered events to Uber's servers in a burst.
* **The Result:** When Uber's stream processing backend receives the packets, the server's system clock (`processing_time`) is ahead of the `event_time` stamped inside the packet due to the basement lag. Uber relies on `event_time` to ensure accurate trip timelines and pricing despite temporary network drops.

## Step 2

### Does the Result appear immediately the window ends?
No. Window results do not appear immediately when the window closes.

### Why not?
Stream processing systems use a watermark to allow for network latency and out-of-order/late-arriving data. If the system finalized results the exact second a window ended, any events delayed in transit would be incorrectly discarded as late data.

### What the delay is.
The delay is equal to the watermark duration (WATERMARK = 20 seconds). A window's result is only outputted once wall-clock time reaches:$$\text{Window Start} + \text{Window Length} + \text{Watermark}$$

### The constant controlling it.
The **WATERMARK** constant.

## Event time & Processing time
If the window logic used processing_time instead of event_time, early windows for example Window 1793575130, and Window 1793575140 would have incorrect counts because of network lag, producer batching, disk I/O, or consumer sleep intervals (time.sleep(0.2)), events belonging to an earlier event-time window would arrive later at the consumer. If ingestion time dictated the window, those events would be stamped with the current wall-clock time and shifted into later processing-time windows, distorting historical accuracy and inflating later window counts.

## Events in data/stream/late_events.jsonl
1. 18 events were routed here. The late events that were accepted into their correct window because they arrived inside the watermark isn't logged.

2. 
    | WATERMARK | Late events logged | Delay before a window prints |
    |---|---|---|
    | 5 | 25 | ~5.1 |
    | 20 | 18 | ~20.1 |
    | 40 | 0 | ~40.1 |

3. 
* **Fraud Alert:** I would choose the **WATERMARK** of 5 because a fraudulent activity must be flagged in real-time other than waiting for a longer time period.

* **Daily price report:** I would choose the **WATERMARK** of 40 because financial market reports must be accurate and complete hence waiting a longer period allows the system to capture records from different markets.

## Duplicate Analysis
1. 12 **duplicates** were caught.
2. The window event counts (n) and price totals increase because duplicate events are no longer skipped, they are processed multiple times, causing the same event to be counted over and over again.
3. For a stream of 10 million events a day, seen_ids grows infinetly in memory, and consumes memory until programs runs of out of memory. One way to limit it is to use a Time-To-Live cache that only stores event IDs from the last fixed amount of time. This limits creates a risk of making the system fail to recognize duplicates that may arrive late after their ID has been removed from cache.

## **Step 7 Answers**

1. **What happened to `offset`, `windows`, and `seen_ids`?**
* The three variables were wiped out completely because they were stored in local memory. `offset` went back to `0`, `windows` started as an empty dictionary, and `seen_ids` was reset to an empty set.

2. **What does the restarted consumer do with events it had already counted?**
* Since `offset` reset to `0`, the restarted consumer **re-read the broker log from the very beginning**. It re-processed all historical events, re-added them to the fresh memory structures, and **re-printed window metrics** for windows it had already reported before the interruption.

3. **What would you have to save (checkpoint) so that a restart continues correctly?**
* **The Read Offset / File Position** (so it knows where it left off in `events.jsonl`).
* **Window State Aggregations** (`n` and `total` per window `ws`) and the **`finalised` set** (so already-published windows aren't re-printed).
* **Deduplication State (`seen_ids`)** (stored in a persistent key-value store or checkpoint file to keep tracking duplicates accurately).

Here is the complete guide and notes for **Step 8**, formatted with markdown asterisks and structured sections for your lab documentation (`docs/Lab_09_notes.md`):

---

## **Step 8 — Stream Architecture Diagram & Batch vs. Streaming Notes**

#### **Batch vs. Streaming in Market-Price Domains**

* **When would a 5-minute batch job have been good enough for this market-price domain?**
* **Use Case:** End-of-day summary reports, historical price trend analysis, billing calculations, or analytical dashboards where decisions do not require second-by-second precision.
* **Why:** When minor reporting delays of a few minutes have zero financial impact, batch jobs are simpler to build, debug, and maintain than continuous stream pipelines.

* **When to use streaming?**
* **Use Case:** High-frequency algorithmic trading, automated stop-loss execution, real-time fraud detection, or instantaneous consumer price alert systems.
* **Why:** When business operations rely on immediate reactions where a delay of even a few minutes can result in severe financial loss or missed risk mitigation.


