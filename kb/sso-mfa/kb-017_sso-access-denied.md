---
id: KB-017
title: "“Access denied” : rôles, groupes, délais"
category: "SSO/MFA"
tags: ["access-denied", "roles", "groups", "support-l2"]
last_reviewed: "2026-01-07"
---
## Summary
“Access denied” arrive quand l’utilisateur s’authentifie, mais n’a pas les droits (rôle RoutePilot ou groupe IdP).

## Causes fréquentes
- Rôle RoutePilot non attribué
- Groupe SSO manquant
- Compte désactivé
- Changement récent (délai de propagation)

## Resolution steps
1) Vérifier que l’utilisateur existe dans le tenant.
2) Vérifier rôle (KB-005) + statut compte.
3) Si SSO actif : vérifier groupe côté IdP (via owner IAM).
4) Demander relogin après 2–5 minutes.

## Verification
Accès aux modules attendus selon rôle.

## Escalation
Si l’utilisateur est correct mais toujours bloqué : ouvrir ticket L3 avec capture + heure + tenant.

## References
- (À compléter) “Rôles & permissions”
