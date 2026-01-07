---
id: KB-006
title: "Demande d’accès / changement de rôle : process interne"
category: "Onboarding & Access"
tags: ["process", "access-request", "support-ops", "l1"]
last_reviewed: "2026-01-07"
---
## Summary
Process standard pour traiter une demande d’accès (nouvel utilisateur, changement de rôle, accès console).

## Informations à collecter
- Tenant + e-mail utilisateur
- Rôle demandé + justification
- Urgence (bloquant / non bloquant)
- App concernée (web / mobile / console admin)

## Resolution steps (L1/L2)
1) Vérifier si l’utilisateur existe déjà.
2) Vérifier si le rôle demandé est cohérent (principe du moindre privilège).
3) Appliquer le changement (ou inviter si nouveau).
4) Confirmer par message : rôle appliqué + délai d’effet (relogin).
5) Documenter la demande (ticket interne ou log).

## Cas particuliers
- Accès console admin : validation obligatoire (responsable produit/ops).
- SCIM : changement côté IdP, pas dans RoutePilot.

## Escalation
Si demande hors politique ou conflit entre équipes, escalader à l’owner IAM/Support Ops.

## References
- (À compléter) “Rôles & permissions”
