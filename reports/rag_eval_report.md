# RAG Evaluation Report

- Date: 2026-01-18 01:37:13
- Model: `all-MiniLM-L6-v2`
- Tests: **8**
- Routing: **ON**

## Metrics

- Hit@1: **75.00%**
- Hit@3: **75.00%**
- Hit@5: **87.50%**
- MRR: **0.7750**

## Outputs

- Details CSV: `reports/rag_eval_details.csv`
- This report: `reports/rag_eval_report.md`

## Notes

- Le scoring combine distance vectorielle + bonus mots-clés (titre/tags/doc).
- Déduplication par `page_id` pour éviter les doublons dans le top-k.
