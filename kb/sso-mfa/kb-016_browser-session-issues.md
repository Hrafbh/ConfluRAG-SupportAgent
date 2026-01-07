---
id: KB-016
title: "Problèmes de session (cookies/cache) : résolution"
category: "SSO/MFA"
tags: ["cookies", "cache", "session", "support-l1"]
last_reviewed: "2026-01-07"
---
## Summary
Les problèmes de session génèrent souvent des boucles login, des pages blanches ou des “session expired”.

## Resolution steps (L1)
1) Ouvrir RoutePilot en navigation privée (test rapide).
2) Si OK en privé :
   - vider cache/cookies pour le domaine RoutePilot
   - désactiver extensions bloquantes (adblock) pour test
3) Tester un autre navigateur supporté (KB-021).
4) Vérifier date/heure du poste (auto).

## Verification
Connexion stable + navigation entre modules sans redirection.

## Escalation
Si problème uniquement sur un tenant : suspicion configuration SSO → escalader IAM.

## References
- (À compléter) “Navigateurs supportés”
