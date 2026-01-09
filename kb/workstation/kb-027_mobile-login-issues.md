---
id: KB-027
title: "Mobile : problèmes de login / session"
category: "Workstation & Mobile"
tags: ["mobile", "login", "session", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Résolution L1 des problèmes de connexion mobile : mot de passe, MFA, sessions, bascule web/mobile.

## Symptoms
- Login échoue sur mobile mais OK sur web
- Boucle de login
- “Session expired” rapide
- MFA bloquante

## Resolution steps
1) Confirmer e-mail exact et tenant (si applicable).
2) Tester la connexion web (KB-015 pour messages d’erreur).
3) Forcer la reconnexion mobile :
   - se déconnecter si possible
   - fermer l’app complètement
   - relancer l’app
4) Vérifier l’heure automatique du téléphone.
5) Si MFA : appliquer KB-012 / KB-013 selon cas.
6) Si persistant : réinstaller l’app (KB-026).

## Verification
Login mobile OK + chargement des tournées.

## Escalation
Si impact multi-utilisateurs : escalader comme incident “auth mobile”.

## References
- KB-015 — Erreurs login
- KB-012/KB-013 — MFA
