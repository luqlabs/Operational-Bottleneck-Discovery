📦 Logistics Intelligence: Inbound Lead Time & SLA Analytics

Live Dashboard: https://operational-bottleneck-discovery-mq6rh2lub5ftmeq9tjtbsp.streamlit.app/

📌 Executive Summary

This project provides an Operational Intelligence solution designed to dissect inefficiencies in inbound logistics. The core problem addressed is the "Unfair KPI Assessment" trap: where team performance is traditionally measured from the moment a truck arrives (Strict SLA), ignoring the unavoidable warehouse queuing time before verification begins.

By engineering a dual-metric approach, this dashboard empirically proves a 23.6% efficiency gap caused by external bottlenecks rather than internal staff performance.



🖼️ Dashboard Interface

> *Modern UI built with Streamlit, featuring custom CSS for a high-end "Dark-Mode" Operational Command Center experience.*

*Visuals include: Phase-based Funnel Analysis, SLA Breach Distributions, and Dynamic KPI Comparison.*



🔴 The Challenge: Data Entropy & "Dark Data"

The raw data originated from three disparate logistics systems with high levels of "noise" and structural inconsistency:

  * **Timestamp Fragmentation:** Mixed date formats (DD/MM vs MM/DD) and overlapping logs.
  * **Structural Chaos:** Shifted columns and missing crucial handover timestamps.
  * **Sensitive Information:** Unstructured logs containing private vendor and serial number data.

🤖 The Solution: AI-Augmented Recovery with Human Validation

I implemented a sophisticated **AI-driven pattern recognition** workflow, but maintained a strict **Human-in-the-loop** verification process:

1.  **AI-Restructuring:** Leveraged LLMs to map "Data Hell" into a clean Star Schema.
2.  **Manual Accuracy Audit:** Personally verified AI-generated outputs against original logs to ensure zero hallucinations in timestamp conversion.
3.  **Automated Anonymization:** Encrypted sensitive vendor identities for corporate security compliance.



🛠️ Data Pipeline & Logic

1.  **Ingestion:** Loading multi-format CSV/Excel inbound logs.
2.  **Engineering (Python & Pandas):** \* **Strict SLA Logic:** $Done - Arrival \le 4$ Days.
      * **Actual Team Performance:** $Done - Verification \le 4$ Days.
3.  **Optimization:** Implemented `st.cache_data` to ensure fluid interaction even with large datasets.

💡 Key Operational Insights (The "Aha\!" Moments)

**The Bottleneck Discovery:** The **Verification** phase was identified as the primary lag point (avg. 4.3 days), shifting the focus from "working faster" to "verifying smarter."
SLA Divergence:** Proved that while the system reports 38.2% efficiency, the actual team velocity is **61.8%** once queueing time is excluded.
The "Arrival Spike" Effect:** Visualized how bulk arrivals on specific days overwhelm capacity, proving that delays are volume-driven, not performance-driven.
Data-Driven Strategy:** Identified that 16.7% of breaches stem from "Physical Mismatches" at the entry gate, recommending a digitization of the initial check-in process.

<img width="1390" height="577" alt="Dashboard Operasional 2" src="https://github.com/user-attachments/assets/2432c241-2157-4eb8-8b2d-39bbcddf1214" />
<img width="1266" height="694" alt="Dashboard Operasional" src="https://github.com/user-attachments/assets/1c8ede7d-b6b5-4a1f-a0cb-b225db045f77" />

