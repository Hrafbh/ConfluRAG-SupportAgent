---
id: KB-021
title: "Navigateurs supportés & configuration recommandée"
category: "Workstation & Mobile"
tags: ["browser", "compatibility", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Cette page liste les navigateurs recommandés pour RoutePilot et les réglages minimum pour éviter les problèmes UI (page blanche, boutons inactifs, sessions instables).

## Navigateurs recommandés (générique)
- Chrome (dernière version)
- Edge (dernière version)
- Firefox (dernière version)

## Réglages recommandés
- Autoriser les cookies (au moins pour RoutePilot)
- Autoriser le stockage local (local storage)
- Désactiver les extensions bloquantes pour test (adblock, privacy tools)
- Vérifier la date/heure automatique sur le poste

## Symptoms
- Page blanche / chargement infini
- Boutons non cliquables
- Déconnexions fréquentes
- Boucle de connexion (SSO)

## Resolution steps
1) Tester en navigation privée (pour isoler cookies/extensions).
2) Si OK en privé : vider cache/cookies du domaine RoutePilot (KB-022).
3) Tester un autre navigateur recommandé.
4) Vérifier date/heure automatique du poste.

## Verification
Navigation stable sur 2–3 modules (Planification, Exécution, Reporting) sans redirection.

## Escalation
Si le problème n’apparaît que sur un tenant spécifique : ouvrir un ticket L2 avec capture + navigateur + heure.

## References
- KB-022 — Vider cache/cookies
- KB-016 — Problèmes de session
