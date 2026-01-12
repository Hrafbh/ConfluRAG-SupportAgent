---
id: KB-053
title: "Runbook — Plateforme indisponible (L1/L2)"
category: "Incidents & Runbooks"
tags: ["runbook", "incident", "platform", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Runbook orienté L1/L2 : qualifier, collecter, communiquer et escalader correctement en cas d’indisponibilité.

## Detection
- Multiples tickets “ça ne charge pas”
- Login KO pour plusieurs utilisateurs
- Mobile + web impactés

## Immediate actions (first 15 minutes)
1) Ouvrir un ticket incident (P1) avec template KB-044.
2) Collecter 3 exemples : tenant, module, heure, captures.
3) Vérifier si incident déjà déclaré (KB-041).
4) Communiquer un accusé réception (KB-047) + prochaine update.

## Mitigation / Workaround (si applicable)
- Proposer hotspot / autre navigateur (si isolé)
- Sinon : pas de workaround → communiquer clairement

## Escalation
- Escalader L3/Tech immédiatement si multi-tenants.
- Activer “Major Incident Comms” (KB-060) si impact large.

## Post-incident
- Mettre à jour KB-052 (Known Issues) si récidive
- Préparer PIR si nécessaire (KB-059)

## References
- KB-041, KB-044, KB-047, KB-060, KB-059
