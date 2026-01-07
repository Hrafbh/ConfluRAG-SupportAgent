---
id: KB-004
title: "Inviter un utilisateur : règles & bonnes pratiques"
category: "Onboarding & Access"
tags: ["users", "invite", "roles", "support-l1"]
last_reviewed: "2026-01-07"
---
## Summary
Guide L1 pour inviter un utilisateur, attribuer le bon rôle et éviter les problèmes de permissions.

## Règles
- 1 e-mail = 1 compte
- Les rôles doivent être attribués selon les responsabilités (éviter Admin par défaut)
- Pour les drivers : privilégier un rôle “Driver” strict

## Resolution steps
1) Admin/Manager ouvre “Administration > Utilisateurs”.
2) “Inviter” : e-mail + prénom/nom (optionnel).
3) Choisir rôle (Dispatcher/Manager/Driver/Viewer).
4) Envoyer invitation.
5) Si besoin, ajouter tags internes (ex: `warehouse-casa`, `team-north`).

## Erreurs fréquentes
- “Utilisateur déjà existant” : utiliser “Rechercher” puis réactiver ou changer rôle.
- “Access denied” après invitation : vérifier rôle + groupes SSO (si activé).

## Verification
L’utilisateur se connecte et voit les modules attendus (pas plus).

## Escalation
Si le compte est provisionné via SCIM, ne pas modifier à la main : escalader à l’Admin IAM.

## References
- (À compléter) “Rôles & permissions”
