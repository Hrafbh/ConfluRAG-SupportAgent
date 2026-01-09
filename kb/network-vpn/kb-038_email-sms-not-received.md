---
id: KB-038
title: "E-mail/SMS non reçus : causes côté usage + vérifs"
category: "Network & Connectivity"
tags: ["email", "sms", "notifications", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Traitement L1 des cas : invitation non reçue, reset password, notifications e-mail/SMS absentes.

## Symptoms
- Invitation utilisateur non reçue
- Reset mot de passe jamais reçu
- SMS OTP / notifications non reçus

## Resolution steps
1) Vérifier l’adresse e-mail/numéro saisi (typos).
2) Demander de vérifier :
   - spam / promotions / quarantine (si entreprise)
3) Demander d’ajouter l’expéditeur/domaine RoutePilot en “safe sender”.
4) Relancer l’envoi (invitation / reset).
5) Pour SMS :
   - vérifier couverture réseau
   - vérifier blocage “spam SMS”
   - tester un autre numéro si possible

## Informations à collecter
- tenant, e-mail/numéro, heure d’envoi, type de message, pays opérateur (SMS).

## Verification
Le message est reçu et l’action est terminée (invitation acceptée / password reset OK).

## Escalation
Si plusieurs clients/pays impactés : escalader comme incident “messaging”.

## References
- KB-007 — Password reset
- KB-056 — Runbook notifications down
