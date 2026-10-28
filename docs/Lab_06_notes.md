# Lab 06 Notes: DuckDB vs. PySpark Performance

## Setup: Data Skew
* **~70%** of the rows belong to *Owino*, intentionally configured to create heavy data skew.

---

## Step 3 — Performance Evaluation
1. **Speed Comparison:** DuckDB was faster by **~9.4 seconds** (~7.8x faster than Spark).
2. **Execution Trigger:** `summary.show()` (and `summary.explain()`).
   * **Why:** Defining `summary = ...` is a **transformation** (lazy evaluation, builds a DAG without loading data). An **action** like `summary.show()` forces Spark to actually execute the plan, read files, shuffle, and compute results.

---

## Step 4 — Reading the Spark Plan
1. **Exchanges (Shuffles):** 
   * **`groupBy`** triggers an exchange via `hashpartitioning` to group keys.
   * **`orderBy`** triggers an exchange via `rangepartitioning` to sort globally.
2. **Dependencies:** 
   * `filter` is **narrow** (executed independently per partition with no shuffle).
   * `groupBy` is **wide** (requires a shuffle to bring matching keys together).
3. **Column Pruning:** Shown by the line `ReadSchema: struct<market:string,price:bigint>`.

---

## Step 5 — Data Skew and Repartitioning
1. **Partition Imbalance:** Repartitioning into 6 buckets by `market` results in extreme unevenness because *Owino* holds millions of rows while smaller markets hold very few.
2. **Stragglers:** The worker processing the massive *Owino* partition takes much longer, causing a **straggler effect** that stalls the entire stage and degrades performance.

## Step 6 — Cache or Not?

### 1. Did caching help?
* **No, in this specific run, caching actually made it slower** (`use_cache=False` took ~4.8s while `use_cache=True` took ~10.3s). 
* **Why:** Running locally, the operating system's file cache already kept the Parquet data in memory after the first read. Spark's internal caching added unnecessary serialization and Block Manager overhead, making it slower than just re-reading or re-evaluating the lightweight dataset.

### 2. Would it help if only **one** action were run on `df`?
* **No.** If only a single action is executed, caching **never helps** and always hurts performance. 
* Caching introduces a performance penalty because Spark must spend time serializing and storing data blocks. If no subsequent actions reuse that cached DataFrame, that overhead is pure waste with zero benefit. Caching is only designed for scenarios with multiple actions or iterative algorithms (like machine learning training loops).

---

## Step 7 — Decision Memo

### Benchmark Summary Table
| Job | Time (s) |
|---|---|
| DuckDB, 5M rows | 0.679s |
| Spark local, 5M rows | 11.084s |
| Spark without cache (2 actions) | 4.809s |
| Spark with cache (2 actions) | 10.314s |

### Scenario Recommendations

* **A. A weekly report on 500,000 rows stored in one Parquet file:**
  * **Recommendation:** **DuckDB**
  * **Rationale:** At 500k rows, the dataset is small enough to fit easily in memory. DuckDB executes single-node vectorised analytical queries in fractions of a second with zero administrative or JVM overhead.

* **B. 2 TB of mobile-money transaction logs processed nightly with fault tolerance:**
  * **Recommendation:** **Apache Spark**
  * **Rationale:** At 2 TB, the data far exceeds single-node memory limits. Spark provides distributed processing across a cluster and automatically handles fault tolerance via lineage tracking, making it ideal for massive distributed workloads.

* **C. A 3 GB file on a lecturer's laptop with 16 GB of RAM:**
  * **Recommendation:** **DuckDB**
  * **Rationale:** A 3 GB file fits comfortably inside a 16 GB laptop's RAM. DuckDB reads and queries columnar files like Parquet directly and efficiently without the configuration complexity and heavier resource demands of a Spark master node.