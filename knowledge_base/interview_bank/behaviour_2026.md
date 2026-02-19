---
title: Behavioural Interview Answers 2026
category: interview
subcategory: behavioural
tags: [leadership, conflict, teamwork, communication, problem-solving]
priority: medium
last_updated: 2026-02
---

# Behavioural Interview Bank

---

## 1. Self Introduction

### Tell me about yourself

My name is Yiming Shen, you can call me Ryan. I’m currently pursuing a Master’s in Data Science and Artificial Intelligence at the University of Waterloo. I also completed my Bachelor’s in Statistics and Computing at Waterloo with excellent academic standing.

Through my academic training, I’ve built a strong foundation in machine learning, statistics, and data-driven problem solving. Beyond academics, I’ve completed five co-op terms across government, banking, fintech, and technology organizations, where I worked closely with stakeholders to turn messy data into actionable insights.

Technically, I’m comfortable with Python and R for modeling and analysis, and I have hands-on experience building end-to-end pipelines using SQL, Power BI, and Tableau. More recently, I’ve been developing more production-oriented skills such as Spark and AWS to expand into scalable ML systems.

Personally, I’m very passionate about extracting patterns from complex data and building solutions that create real impact.

---

## 2. Work Experience Stories (STAR Format)

---

### CIBC – Data Pipeline Optimization

**Situation:**  
During my 8-month co-op at CIBC, I worked with the End Point Print and Digital Output team. They manage enterprise printer networks across Canada. Data was stored in an internal SQL Server instance, and my task was to build dashboards to monitor performance and usage.

**Task:**  
Build an end-to-end data pipeline and ensure dashboards refresh efficiently as data volume grows.

**Action:**  
- Built SQL views for aggregation and filtering  
- Deployed On-Premises Data Gateway  
- Designed Power BI dashboards with scheduled refresh  

Later, I faced performance issues caused by increasing data size. Even after enabling incremental refresh, performance was unstable.

Using a diagnostic mindset, I:
- Broke the problem into SQL layer, gateway layer, and BI layer  
- Discovered that query folding was failing  
- Reordered transformation steps to ensure filtering was pushed down to SQL  
- Simplified Power Query steps  

**Result:**  
Refresh became fast and stable. The dashboards were adopted by stakeholders, and I received an “Outstanding” performance rating.

---

### Kaggle – Fixing Data Leakage in Time Series

**Situation:**  
In a Kaggle competition on S&P 500 forecasting, I built a time-series ML pipeline.

**Task:**  
Develop a strategy within 2 months and maximize adjusted Sharpe ratio.

**Action:**  
During validation, I noticed unusually high performance. That raised a red flag for potential data leakage.

Using controlled experiments:
- Removed wavelet decomposition features  
- Observed validation performance dropped to realistic levels  
- Investigated wavelet implementation  
- Discovered symmetric windowing introduced look-ahead bias  
- Replaced with strictly one-sided causal filtering  

**Result:**  
Validation became more conservative but reliable. I learned the importance of leakage-aware modeling in time series.

---

## 3. Core Soft Skills

---

### Communication

- Identify audience (technical vs leadership)
- Align explanation with business objectives
- Use simple visuals to communicate impact
- Continuously check for understanding

Example:  
When explaining Sharpe Ratio performance in Kaggle, I used a simple cumulative return line chart to visually show how our strategy behaved during market volatility.

---

### Conflict Handling

**Example – Feature Engineering Disagreement**

**Situation:**  
In the Kaggle project, teammates disagreed on adding new features vs using PCA for dimensionality reduction.

**Action:**  
- Scheduled structured 30-minute discussion  
- Let both sides present reasoning  
- Designed controlled experiment keeping everything else fixed  

**Result:**  
Found adding features was more stable across folds. Reached consensus and moved forward.

Key principles:
- Understand root cause of disagreement  
- Use data or experiments to resolve conflict  
- Avoid ego-based argument  

---

### Time Management

- Break large tasks into milestones  
- Set mini-deadlines  
- Prioritize client-facing deliverables  
- Time-box lower priority tasks  

Example:  
At Horizn, I handled 3 concurrent tasks. I clarified priorities with my manager and allocated time accordingly. Delivered all tasks on time.

---

### Stress Handling

When deadlines cluster together:
- Break tasks into small milestones  
- Reduce uncertainty through planning  
- Maintain a clean workspace  
- Use hobbies (badminton, swimming) to decompress  

For team stress:
- Increase transparency  
- Provide short progress updates  
- Reduce uncertainty within the team  

---

### Problem Solving

Framework:
1. Break problem into components  
2. Isolate variables  
3. Run small controlled experiments  
4. Close knowledge gaps via learning  

Example:  
At CIBC, diagnosed refresh issue by isolating BI, gateway, and SQL layers.

---

### Adaptability

Example – Philips Lighting:

**Situation:**  
Worked as procurement intern without supply chain background.

**Action:**  
- Proactively asked colleagues  
- Took notes  
- Self-learned business terms  

**Result:**  
Fully independent within one month.

---

## 4. Common Behavioural Questions

---

### Tell me about a failure

In a STAT course, I spent days preparing but didn’t get expected results. I reflected and realized learning curves are not linear. I focused on improving strategy instead of doubting effort.

Lesson:
- Reflect objectively  
- Avoid emotional spiral  
- Improve system, not just effort  

---

### How do you handle criticism?

When my manager wasn’t satisfied with my first dashboard version:
- Collected feedback individually  
- Identified conflicting stakeholder requirements  
- Created shared documentation  
- Facilitated short alignment discussion  

Result:  
Clear requirements, improved version accepted.

---

### What is your greatest strength?

Adaptability and structured problem solving.

---

### What is your weakness?

Leadership experience — currently improving by volunteering for presentation and coordination roles.

---

### Where do you see yourself in 5 years?

Short-term: Complete Master’s and deepen ML system skills.  
Mid-term: Become a strong data scientist and transition toward MLE.  
Long-term: Work on impactful AI systems where curiosity drives continuous learning.

---

## 5. Decision-Making Framework

When facing disagreement:
- Clarify assumptions  
- Use data as evidence  
- Propose low-cost experiment  
- Move forward with evidence  

---

## 6. Interview Reflection Principle

Across all experiences:

- Transparency  
- Feedback loop  
- Ownership mindset  
- Treat work as end-to-end responsibility  
- Deliver MVP early  
- Iterate quickly  

