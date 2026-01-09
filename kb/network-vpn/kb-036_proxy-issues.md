---
id: KB-036
title: "Proxy : erreurs d’accès au SaaS (401/403) — diagnostic simple"
category: "Network & Connectivity"
tags: ["proxy", "access", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Certaines entreprises clientes utilisent un proxy. Cette page aide à qualifier rapidement si un proxy bloque l’accès à RoutePilot.

## Symptoms
- 403/Access forbidden sur RoutePilot
- Téléchargements bloqués
- Fonctionne sur 4G mais pas sur réseau entreprise client

## Resolution steps (L1/L2)
1) Demander si le client utilise un proxy/filtrage.
2) Tester depuis un autre réseau (hotspot) :
   - si OK → suspicion proxy
3) Demander au client :
   - d’autoriser le domaine RoutePilot
   - d’autoriser les téléchargements (CSV/PDF) si bloqués
4) Collecter infos pour whitelist si nécessaire (KB-037).

## Verification
Accès web OK depuis réseau entreprise.

## Escalation
Si besoin d’action IT client : fournir un message clair + éléments à autoriser (domaines) via procédure.

## References
- KB-037 — Whitelist IP request
- KB-024 — Exports PDF/CSV
