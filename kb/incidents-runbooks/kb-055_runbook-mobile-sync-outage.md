---
id: KB-055
title: "Runbook — Sync mobile KO (terrain)"
category: "Incidents & Runbooks"
tags: ["runbook", "mobile", "sync", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Runbook L1/L2 pour traiter un incident où les statuts/POD remontent mal depuis le mobile.

## Detection
- Plusieurs drivers : missions non à jour
- POD en attente d’upload sur une zone
- Web backoffice ne reflète pas les statuts

## Immediate actions
1) Collecter zone géographique + opérateurs réseau si SMS/data concernés.
2) Demander aux drivers de tester :
   - relancer app
   - changer réseau si possible (KB-040)
3) Vérifier si l’incident est localisé (1 site/zone) ou global.
4) Communiquer workaround si existant (KB-047).

## Escalation
Si impact large ou multi-zones : escalader Tech (incident).

## Post-incident
Ajouter un item dans KB-052 si récurrent.

## References
- KB-040 — Mobile sync
- KB-025 — Upload fail
- KB-047 — Communication
