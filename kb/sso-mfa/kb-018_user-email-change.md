---
id: KB-018
title: "Changement d’e-mail utilisateur : impacts & procédure"
category: "SSO/MFA"
tags: ["email-change", "identity", "support-l2"]
last_reviewed: "2026-01-07"
---
## Summary
Changer l’e-mail d’un utilisateur peut impacter SSO, invitations et historique. À faire proprement.

## Règles
- Si SSO/SCIM actif : l’e-mail est une identité → changer côté IdP d’abord.
- Éviter de créer un “nouveau compte” si l’ancien contient historique.

## Resolution steps
1) Confirmer : ancien e-mail, nouveau e-mail, tenant, rôle.
2) Vérifier si nouveau e-mail existe déjà (doublon).
3) Effectuer la mise à jour (selon politique) ou demander IAM de le faire.
4) Forcer relogin (sessions invalidées si possible).

## Verification
Connexion avec nouvel e-mail + accès correct.

## Escalation
Si SCIM : traiter via IAM uniquement (RoutePilot devient “read-only” sur identité).

## References
- (À compléter) “Provisioning SCIM”
