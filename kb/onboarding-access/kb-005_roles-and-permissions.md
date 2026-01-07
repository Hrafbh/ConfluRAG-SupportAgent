---
id: KB-005
title: "Rôles & permissions (Dispatcher, Manager, Driver, Viewer)"
category: "Onboarding & Access"
tags: ["rbac", "roles", "permissions", "support-l1"]
last_reviewed: "2026-01-07"
---
## Summary
Table simple des rôles RoutePilot pour répondre vite aux demandes “je ne vois pas X / je ne peux pas faire Y”.

## Rôles (résumé)
- Admin : gestion tenant, utilisateurs, paramètres.
- Manager : lecture KPI, validation, exports, suivi global.
- Dispatcher : création/édition tournées, affectations, support terrain.
- Driver : exécution via mobile, statuts, POD (photo/signature).
- Viewer : lecture seule (suivi, rapports).

## Symptômes classiques
- “Je ne vois pas l’onglet Reporting” → rôle trop restrictif (souvent Driver/Viewer).
- “Je ne peux pas éditer une tournée” → Viewer/Manager au lieu de Dispatcher.
- “Je ne peux pas inviter des utilisateurs” → pas Admin.

## Resolution steps
1) Identifier le rôle actuel.
2) Appliquer le rôle minimal nécessaire.
3) Demander à l’utilisateur de se déconnecter/reconnecter.

## Escalation
Si SSO/SCIM actif : modifier côté IdP (groupe), puis resynchroniser.

## References
- (À compléter) “Access denied”
