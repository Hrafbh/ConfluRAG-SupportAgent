---
id: KB-057
title: "Runbook — Carte/ETA incohérents (triage support)"
category: "Incidents & Runbooks"
tags: ["runbook", "eta", "map", "triage", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Runbook L1/L2 pour qualifier “ETA incohérents” sans diagnostic technique profond.

## Detection
- Managers se plaignent d’ETA trop optimistes/pessimistes
- Carte ne correspond pas au terrain (retards non reflétés)

## Immediate actions
1) Demander :
   - zone concernée
   - période (depuis quand)
   - exemples de tournées/livraisons
2) Vérifier côté mobile :
   - localisation activée (KB-028)
   - sync OK (KB-040)
3) Vérifier si le problème est sur 1 site ou multi-sites.
4) Communiquer : “en cours de vérification” + délai update (KB-047).

## Escalation
Si multi-tenants/zones : escalader L3 avec exemples concrets (IDs tournées si disponibles).

## Post-incident
Documenter workaround si existant dans KB-052.

## References
- KB-028, KB-040, KB-047, KB-052
