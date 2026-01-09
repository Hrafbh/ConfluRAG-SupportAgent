---
id: KB-039
title: "Application lente : triage L1/L2 (non technique)"
category: "Network & Connectivity"
tags: ["performance", "slow", "triage", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Triage simple pour les plaintes “RoutePilot est lent” (web), afin de distinguer réseau local vs problème général.

## Symptoms
- Chargements longs sur tableaux/tournées
- Temps d’ouverture page élevé
- Lenteur à certaines heures

## Resolution steps
1) Demander si le problème est :
   - sur un module précis (ex: Reporting)
   - sur tout le produit
2) Tester un autre navigateur / navigation privée (KB-021/KB-022).
3) Tester un autre réseau (hotspot) si possible.
4) Demander si d’autres utilisateurs du même tenant sont impactés.
5) Relever :
   - heure exacte
   - page exacte
   - volume (ex: période report très large)

## Verification
Amélioration confirmée après action ou confirmation que le problème est isolé (réseau local).

## Escalation
Si impact multi-utilisateurs ou multi-tenants : escalader L2 (potentiel incident performance).

## References
- KB-033 — Checklist connectivité
- KB-024 — Exports (si le problème concerne la génération)
