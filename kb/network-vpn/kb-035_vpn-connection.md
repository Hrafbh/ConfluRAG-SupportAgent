---
id: KB-035
title: "VPN : connexion et erreurs fréquentes (interne)"
category: "Network & Connectivity"
tags: ["vpn", "access", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Guide non technique pour les cas où l’accès à certains outils internes nécessite un VPN (console, backoffice, etc.).

## Symptoms
- Accès console admin impossible hors VPN
- Ressources internes inaccessibles
- Déconnexions VPN fréquentes

## Resolution steps
1) Vérifier si la ressource nécessite VPN (selon politique interne).
2) Se déconnecter/reconnecter au VPN.
3) Tester l’accès après 2 minutes (propagation).
4) Changer de réseau (Wi-Fi ↔ 4G) si instable.
5) Redémarrer poste si VPN bloqué.

## Informations à collecter
- nom VPN, message d’erreur, heure, réseau utilisé.

## Verification
Accès à la ressource interne OK.

## Escalation
Si le VPN ne fonctionne pas du tout : escalader IT interne (pas produit RoutePilot).

## References
- KB-033 — Checklist connectivité
