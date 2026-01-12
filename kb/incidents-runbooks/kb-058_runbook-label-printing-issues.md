---
id: KB-058
title: "Runbook — Impression étiquettes KO"
category: "Incidents & Runbooks"
tags: ["runbook", "labels", "printing", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Runbook L1/L2 pour un incident d’impression d’étiquettes (format cassé, PDF KO, scan impossible).

## Detection
- Plusieurs sites/entrepôts impactés
- Étiquettes coupées ou illisibles
- PDF export ne s’ouvre pas

## Immediate actions
1) Confirmer si l’impact est local (1 imprimante) ou global.
2) Demander :
   - modèle imprimante
   - type étiquette
   - exemple PDF (si partage possible)
3) Tester workaround :
   - impression depuis autre navigateur (KB-021)
   - échelle 100% (KB-031)
4) Communiquer workaround + délai update.

## Escalation
Si multi-sites : escalader L3 (potentiel changement export/format).

## References
- KB-031, KB-024, KB-021
