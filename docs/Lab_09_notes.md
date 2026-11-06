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

---

## **Step 2 Question**

* **What problem does sharing `make_features` prevent?**
It prevents **training–serving skew**, a discrepancy where the data preprocessing logic used during model training differs from the preprocessing logic applied to live requests in production.

* **What would happen if the API had its own copy?**
If the API maintained a separate copy of the feature engineering code, any minor update, bug fix, or accidental change to one copy (e.g., altering one-hot encoding columns, default missing-value handling, or column ordering) would instantly cause a mismatch. The model would receive features it wasn't trained to interpret, leading to **silent failure, corrupted predictions, or runtime exceptions**.

## **Step 4 Answers**

1. **Which data was this model trained on?**
* **`training_data_sha256`** (along with `n_training_rows`). The SHA-256 hash gives a cryptographically unique fingerprint of the exact parquet dataset file used, proving precisely which version of the training data generated the weights.

2. **Which model is serving right now?**
* **`model_version`** (timestamp `20261102-044416`) and **`model_type`** (`LinearRegression`). The version string allows monitoring tools and logs to instantly track which deployed iteration is actively answering inference requests.

## **Step 7 answers**
| Request | Status | Message |
|---|---|---|
| `rainfall_mm` = -5 | 422 | Input should be greater than or equal to 0 |
| `market` = "Narnia" | 422 | Input should be 'Owino', 'Nakasero', 'Kalerwe', 'Mbale Central', 'Gulu Main' or 'Unknown' |
| `date` = "not-a-date" | 422 | Input should be a valid date or datetime, invalid character in year |


#### **Question:** Why a 422 better than a 500, or than returning a prediction anyway?

* **A 422 (Unprocessable Entity)** explicitly and cleanly tells the client *what* is wrong with their input right at the API boundary before any heavy code runs.
* **A 500 (Internal Server Error)** indicates a raw server crash or unhandled exception, which is bad practice because it hides the real validation problem and leaks internal stack traces.
* **Returning a prediction anyway** with garbage or invalid input would cause a **silent failure** ("garbage in, garbage out"), giving the user a fake, meaningless price without any warning that their request was broken.

## **Step 8: Training-serving skew**

1. {
    "predicted_price": -6577.1,
    "model_version": "20261102-044416"
    }

2. {
    "predicted_price": 3682.27,
    "model_version": "20261102-044416"
    }

* **Did the service crash?**
* **No.** The API returned an HTTP 200 OK successfully. This highlights the danger of **silent failures**, the system looks healthy on the outside, but its internal logic is corrupted.


* **Did the prediction change?**
* **Yes.** Because the input features were divided by 1000 without the model weights being retrained to match, the model interpreted the rainfall entirely wrong, resulting in a distorted, incorrect price prediction.


* **What does this tell you about why `/health` should report the model version?**
* It ensures transparency. While `/health` confirms the service is running, adding version and metadata tracking lets monitoring tools verify that the deployed code and model artifact match expectations.


* **What additional field could you add to the metadata to detect a feature-code change?**
* A **`features_code_sha256`** hash. If a checksum of `features.py` is computed during training and stored in `model_metadata.json`, the API startup script could compare it against the current file hash and instantly flag or notify engineers of a change in feature.

---

## **Step 10 (Containerization)**

#### **Questions**

1. **Why must the scikit-learn version in the image match the one that trained the model?**
* Joblib/pickle serialization stores internal object states and structural bindings tied directly to the exact scikit-learn version. If versions mismatch, deserialization can fail or produce silent numerical drift/errors.


2. **Why is `data/` left out of the image?**
* The dataset is massive, changes frequently, and is only needed for *training* (`train.py`), not for live *inference*. Keeping raw data out of the production container keeps image size lightweight and secure.

## **Step 11: Reproducibility**
```bash
# 1. Run the container and test initial output
$ sudo docker run -d --name price -p 8000:8000 price-service
c1269cf7dbdcf03cbc1978210926256cf94be963b1ae63b73f08ebd130d02119

$ python -m src.api.test_client
--- health: HTTP 200
{'status': 'ok', 'model_version': '20261102-044416', 'model_type': 'LinearRegression'}
--- predict (valid): HTTP 200
{'predicted_price': 3028.56, 'model_version': '20261102-044416'}
--- predict (invalid): HTTP 422
{'detail': [{'type': 'literal_error', 'loc': ['body', 'market'], ...}]}

# 2. Restart container and re-run client
$ sudo docker restart price
price

$ python -m src.api.test_client
--- health: HTTP 200
{'status': 'ok', 'model_version': '20261102-044416', 'model_type': 'LinearRegression'}
--- predict (valid): HTTP 200
{'predicted_price': 3028.56, 'model_version': '20261102-044416'}
--- predict (invalid): HTTP 422
{'detail': [{'type': 'literal_error', 'loc': ['body', 'market'], ...}]}

Look at that output—both predictions returned exactly `3028.56` before and after the container restart, proving 100% reproducibility via containerization!

Here is the markdown block you can drop directly into your `docs/Lab_9_notes.md` (or `docs/Lab_09_notes.md`) file to capture Step 11 and Step 12 cleanly.
```
---

**Observation:** The predicted price is **identical** (`3028.56`) before and after restarting the container. This proves that the environment, dependencies, code, and model weights are completely encapsulated and deterministic within the Docker image.

---

### **Step 12 Answers**

1. **Where does preprocessing happen at inference time?**
* Preprocessing happens directly inside the `/predict` API endpoint by importing and executing the centralized `make_features()` function on incoming request payloads.


2. **How does your design prevent training–serving skew? Which Step showed it can still happen and how?**
* Using a single, shared `make_features()` module for both training and inference guarantees identical transformation logic. Step 8 demonstrated that skew can still happen if someone modifies preprocessing parameters or units (e.g., changing rainfall divisors) without retraining the model, resulting in silent prediction drift.


3. **What should `/health` prove?**
* It should prove that the service is up and running while exposing key metadata fields (`model_version` and `model_type`) so clients and monitoring tools can verify exactly which model artifact is actively handling live traffic.


4. **Which information belongs with a model version, and why?**
* Information such as training data hashes (`training_data_sha256`), feature schema lists, model metrics (`train_r2`), and training row counts belong with the version because they establish an immutable lineage, audit trail, and guarantee reproducibility.


5. **When would batch inference be a better choice than this API for market prices?**
* Batch inference is better for bulk operations like generating end-of-day commodity price reports, populating data warehouses, or running heavy analytical dashboards where sub-second real-time response latency is unnecessary.
