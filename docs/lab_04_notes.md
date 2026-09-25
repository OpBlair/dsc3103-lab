# Lab 4 Notes

## Step 2: Schema Trade-off
When we turned our flat file into a star schema, we traded away pipeline simplicity and extra join/storage overhead in return for a cleaner structure, less data repetition, and easier querying down the line.

## Step 5: Performance Observations
Running the same query (average price per market) for both setups gave these numbers:

* **Flat Parquet Query Time:** 0.0031s
* **Star Schema Query Time:** 0.0323s

*Note: These times aren't fixed and change a bit each time you run the script. In this specific run, the flat Parquet file was faster.*

**Observation:** Even though both queries finish super fast because our dataset is only 889 rows, the star schema takes a bit longer because it has to do a join between the fact table and the market dimension table. The flat Parquet file can just calculate the average directly without any extra joins.

## Step 6: Architecture Decision Justification

### Is a star schema worth the added complexity at our current data size?
Honestly, at 889 rows, a star schema isn't really worth it for performance. DuckDB scans the flat Parquet file so efficiently that doing joins just adds unnecessary overhead and extra code complexity for a small dataset.

However, setting it up this way makes sense when thinking about scaling and organization:

* **Less redundancy:** Keeping markets and commodities in their own tables (`dim_market`, `dim_commodity`) stops us from repeating text strings all over the place in the fact table.
* **BI Tools friendly:** If we hook this up to tools like Tableau or PowerBI later, they natively expect a dimensional model anyway.
* **Scaling:** While duplicate text doesn't hurt at 889 rows, it would bloat storage and network I/O if we were dealing with millions of rows.

**Conclusion:** Right now, the flat Parquet file is simpler and faster for our current workload. But building the star schema gives us a proper analytical foundation that would actually matter if the dataset grows much larger.