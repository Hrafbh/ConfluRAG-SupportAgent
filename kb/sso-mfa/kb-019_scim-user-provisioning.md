---
id: KB-019
title: "Provisioning utilisateurs (SCIM) : règles simples"
category: "SSO/MFA"
tags: ["scim", "provisioning", "iam", "support-l2"]
last_reviewed: "2026-01-07"
---
## Summary
Avec SCIM, les utilisateurs (création/désactivation) sont gérés par l’IdP. Le support doit savoir quoi faire et quoi éviter.

## Ce que SCIM gère
- Création / désactivation comptes
- (souvent) attributs : nom, e-mail, groupes

## Règles support
- Ne pas “corriger à la main” dans RoutePilot si SCIM fait autorité.
- Pour un accès manquant : vérifier groupe IdP → rôle RoutePilot.
- Pour un offboarding : désactiver côté IdP (sync ensuite).

## Verification
- Sync effectué (ou attendu) + compte visible correctement.

## Escalation
Si sync incohérente : fournir tenant + e-mail + groupe attendu + heure dernière modif.

## References
- (À compléter) “SSO setup overview”
