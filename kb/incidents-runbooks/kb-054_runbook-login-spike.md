---
id: KB-054
title: "Runbook — Pic d’échecs login (SSO/MFA)"
category: "Incidents & Runbooks"
tags: ["runbook", "login", "sso", "mfa", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Runbook L1/L2 pour un pic d’échecs de connexion : distinguer erreur utilisateur vs problème global SSO.

## Detection
- Plusieurs utilisateurs signalent “Access denied” ou boucles login
- Augmentation des demandes reset MFA / compte bloqué

## Immediate actions
1) Demander le message exact + captures (KB-046).
2) Vérifier si changement récent (SSO, groupes, policy MFA).
3) Tester avec un compte pilote (si possible) sur un tenant impacté.
4) Communiquer : accusé réception + délai update (KB-047).

## Quick checks (support)
- Cookies/session : KB-016
- Access denied : KB-017
- Compte bloqué : KB-008
- Reset MFA : KB-013

## Escalation
Si multi-tenants ou suspicion IdP : escalader Tech/IAM avec 3 exemples (heure + tenant + erreur).

## Post-incident
Mettre à jour KB-052 si un workaround est identifié.

## References
- KB-017, KB-016, KB-013, KB-047, KB-052
