# Data Science (Systems & Technologies) (BSCS-3)

## DSC3103 · Advent Semester 2026

# DATA SCIENCE (SYSTEMS & TECHNOLOGIES)

**From raw streaming logs to scalable, enterprise-grade data platforms.**

Dear Students,

Welcome to Data Science (Systems & Technologies). We are thrilled to guide you through this course, which forms the operational and infrastructural backbone for Computer Science, Software Engineering, and Data Science students. While modeling and analytics get much of the spotlight, real-world data science relies on robust systems: distributed processing engines, fault-tolerant streaming pipelines, containerized environments, and cloud data warehouses. Throughout this course, you will learn how to architect end-to-end data pipelines using technologies like PostgreSQL, Apache Parquet, Apache Kafka, PySpark, Docker, and BI serving layers. You will master data modeling, shuffle optimization, distributed ML execution, role-based security, and micro-batch processing. The engineering skills you build here will empower you to handle petabyte-scale datasets and build production-ready data platforms.

Please ensure Python 3.10+, Docker, and PySpark are properly configured on your machine prior to our Week 2 setup lab. Bring your curiosity, system-thinking mindset, and a readiness to write code.

Best wishes.

**Ready to build enterprise data platforms?**

This is the right Course for you.

---

## When, Where & Who

### Meeting Times

| Day | Time |
|---|---|
| Monday | 16:00hrs – 18:00hrs |
| Friday | 11:00hrs – 13:00hrs |

### Venue

Room N1, N2 & N11A

### Course Facilitators

**Brian Senabulya**

bsenabulya@ucu.ac.ug

---

## Course Objectives

By the end of this course, you will be able to:

- ✓ Design and implement data pipelines (ingestion → storage → processing → serving).
- ✓ Compare and choose appropriate storage systems (relational, NoSQL, data lake/warehouse concepts).
- ✓ Work with distributed/big-data processing tools at a working level.
- ✓ Leverage Cloud Platforms for Data Solutions.
- ✓ Build simple APIs/dashboards to serve data products.
- ✓ Understand and apply data governance, quality basics, and security best practices.
- ✓ Deploy a small end-to-end project on limited infrastructure.

---

## Assessment Criteria

Your final grade is made up of the following components:

| Assessment Component | Weight |
|---|---:|
| Attendance | 5% |
| Presentation and participation | 15% |
| Assignments | 40% |
| Final Exam | 40% |
| **Total** | **100%** |

---

## Course Technologies & Tools

We will use the following technologies for interactive learning throught the course.

### Moodle

Access course content, assignments, and quizzes.

### Python

The core programming language for data science systems.

### Visual Studio Code

Your editor for code development and project work.

### Jupyter Notebook

Interactive coding, experimentation and learning.

### NumPy

For numerical Computations.

### pandas

For data analysis, manipulation and preparation.

### Apache Spark/PySpark

For processing and analysis of large amounts of Data.

### Docker

For creation and running of Isolated Environments.

---

## Course Outline

- ✓ From Software systems to Data Systems.
- ✓ Reliable ETL/ELT and Pipeline Engineering.
- ✓ Analytical storage and Data Architecture.
- ✓ Workflow Automation and Orchestration(Airflow, DAGS).
- ✓ Distributed Batch Processing(PySpark).
- ✓ Streaming and Event Driven Systems(Kafka).
- ✓ From Model/Analytics to a Data Product(Docker).
- ✓ Reliability and Governance.

---

# Weekly Course Content

## Week 1 - From Software Systems to Data Systems (1)

### Learning Outcomes

- ✓ Identify the stages of a modern data lifecycle and classify common data sources/formats.
- ✓ Profile a dataset for schema, missingness, duplicates, invalid values and suspicious distributions.
- ✓ Apply reproducible cleaning rules without silently destroying source evidence.
- ✓ Explain sampling, bias, correlation/causation and data leakage at a practical level.

### Course Materials and Activities

- Week_1_Notes. File
- Lab01 Folder
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

### Quiz_01

- Opened: Monday, 7 September 2026, 4:45 PM
- Closed: Monday, 7 September 2026, 5:05 PM

---

## Week 2- From Software Systems to Data Systems(2)

### Course Materials and Activities

- Lab_02 Folder
- Lab 02_01 Folder
- Assignment one
  - Opened: Tuesday, 1 September 2026, 9:00 AM
  - Due: Monday, 7 September 2026, 4:35 PM
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 3: Reliable ETL/ELT and Pipeline Engineering

### Learning Outcomes

- ✓ Distinguish ETL and ELT and select an appropriate pattern.
- ✓ Decompose ingestion, validation, transformation and loading into modular stages.
- ✓ Implement logging, configuration and error handling.
- ✓ Design idempotent/repeatable pipeline behaviour for a defined dataset.

### Course Materials and Activities

- Week_03_Notes File
- Lab_03 File
- Lab_03_files Folder
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 4: Analytical Storage and Data Architecture

### Learning Outcomes

- ✓ Differentiate OLTP and OLAP workloads.
- ✓ Compare row-oriented and columnar storage using evidence.
- ✓ Use Parquet and DuckDB for analytical querying.
- ✓ Design a simple star schema and justify partition/index choices.

### Course Materials and Activities

- Test 01 Assignment
  - Due: Friday, 25 September 2026, 12:00 AM
- Assignment_02
  - Opened: Saturday, 19 September 2026, 8:00 AM
  - Due: Sunday, 27 September 2026, 11:59 PM
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 5: Workflow Automation and Orchestration

### Learning Outcomes

- ✓ Represent a pipeline as a dependency graph/DAG.
- ✓ Schedule and parameterize a workflow.
- ✓ Configure retries and observe task state/logs.
- ✓ Recover from a deliberately injected workflow failure.

### Course Materials and Activities

- Week 05 Notes File
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 6: Workflow Automation and Orchestration

### Course Materials and Activities

- Lab_05 Folder
- Lab 05-Reference Folder
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 7: Distributed Batch Processing

### Course Materials and Activities

- DSC3103- Data Science Lecture BigBlueButton
- Class Exercise Folder
- Quiz Two
  - Opened: Monday, 19 October 2026, 4:00 PM
  - Closed: Monday, 19 October 2026, 6:30 PM
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 8: Distributed Batch Processing

### Learning Outcomes

- ✓ Explain scale-up vs scale-out and the role of partitions.
- ✓ Implement transformations with PySpark DataFrames.
- ✓ Identify operations likely to trigger expensive shuffles.
- ✓ Choose among Pandas, DuckDB and Spark based on workload and operational cost.

### Course Materials and Activities

- Week 08 Notes File
- Lab 08 Folder
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 9: Streaming and Event-Driven Data Systems

### Learning Outcomes

- ✓ Distinguish batch and streaming processing requirements.
- ✓ Implement a producer/consumer or equivalent event flow.
- ✓ Compute time-windowed metrics over a stream.
- ✓ Explain ordering, event time, processing time and late-data implications.

### Course Materials and Activities

- Assignment_three
  - Opened: Tuesday, 20 October 2026, 4:00 PM
  - Due: Monday, 26 October 2026, 4:00 PM
- Lab 09_01 Folder
- Sample_Qtn File
- Test_02 Assignment
  - Opened: Friday, 30 October 2026, 11:10 AM
  - Due: Friday, 30 October 2026, 1:24 PM
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---

## Week 10: From Model/Analytics to a Data Product

### Learning Outcomes

- ✓ Separate training, inference and feature-processing responsibilities.
- ✓ Persist and reload a model artifact with metadata.
- ✓ Expose predictions/analytics through a validated REST API.
- ✓ Package the service in a reproducible container.

### Course Materials and Activities

- Week 10 Notes File
- Lab 10 Folder
- Assignment_04
  - Opened: Thursday, 29 October 2026, 5:00 PM
  - Due: Friday, 6 November 2026, 11:00 AM
- Learner/ Student's Feedback

"Dear Learner/Student, please give feedback to your instructor/teacher for this topic.

---
