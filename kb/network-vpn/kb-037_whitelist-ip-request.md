---
id: KB-037
title: "Whitelist IP client : process & infos à collecter"
category: "Network & Connectivity"
tags: ["whitelist", "ip", "client-it", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Procédure L2 pour gérer une demande de whitelist côté client (accès à RoutePilot depuis un réseau filtré).

## Informations à collecter (obligatoire)
- Tenant / nom client
- Environnement concerné (prod/staging si applicable)
- Contexte : blocage proxy/firewall, message exact
- Contact IT client (e-mail)
- Deadline / urgence

## Resolution steps
1) Valider que le besoin est légitime (réseau filtré confirmé).
2) Fournir au client la liste des domaines/URL RoutePilot à autoriser.
3) Si le client exige une whitelist IP :
   - fournir les IP publiques officielles (document interne)
   - noter les contraintes (plage, région)
4) Suivre jusqu’à confirmation “accès OK”.

## Verification
Le client confirme accès depuis son réseau entreprise.

## Escalation
Si la demande dépasse la politique (IP non disponibles / cas complexe) : escalader Ops/Tech owner.

## References
- KB-036 — Proxy issues
