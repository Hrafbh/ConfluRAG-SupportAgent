---
id: KB-056
title: "Runbook — Notifications e-mail/SMS en panne"
category: "Incidents & Runbooks"
tags: ["runbook", "notifications", "email", "sms", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Runbook L1/L2 pour une panne de notifications (invitation, reset password, alertes e-mail/SMS).

## Detection
- Multiples cas “e-mail non reçu” sur différents clients
- SMS OTP/notification non reçus sur plusieurs pays

## Immediate actions
1) Confirmer que ce n’est pas un cas isolé :
   - vérifier 3 tenants minimum
2) Collecter :
   - type message (invitation/reset/OTP)
   - heure envoi
   - pays/opérateur (SMS)
3) Informer les utilisateurs :
   - accusé réception
   - workaround (ex : renvoyer plus tard, alternative e-mail)

## Workarounds possibles (si applicables)
- Utiliser un autre canal (e-mail au lieu SMS) selon politique
- Renvoyer après 15–30 minutes
- Vérifier spam/quarantine côté client (KB-038)

## Escalation
Si multi-tenants : escalader Tech immédiatement.

## Post-incident
Mettre à jour KB-052 et envisager un message major incident (KB-060).

## References
- KB-038, KB-047, KB-060, KB-052
