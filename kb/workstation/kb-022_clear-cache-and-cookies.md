---
id: KB-022
title: "Vider cache/cookies : résolution rapide UI"
category: "Workstation & Mobile"
tags: ["cache", "cookies", "session", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Procédure L1 pour corriger les problèmes de session, d’affichage et de connexion liés au cache/cookies.

## Symptoms
- “Session expired” en boucle
- Page blanche après login
- Erreurs d’affichage (menus manquants)
- Conflits après une mise à jour (release)

## Resolution steps
1) Tester d’abord en navigation privée.
2) Si navigation privée OK :
   - vider cache + cookies pour le domaine RoutePilot uniquement
   - fermer toutes les tabs RoutePilot
3) Revenir sur RoutePilot et se reconnecter.

## Bonnes pratiques support
- Demander le navigateur + version.
- Demander si l’erreur est apparue “après une mise à jour” ou “après changement SSO”.

## Verification
Connexion stable et affichage normal des menus.

## Escalation
Si l’utilisateur ne peut pas se connecter du tout : appliquer KB-015 (erreurs login) puis escalader si nécessaire.

## References
- KB-021 — Navigateurs supportés
- KB-016 — Problèmes de session
