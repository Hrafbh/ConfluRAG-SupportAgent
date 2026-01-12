---
id: KB-042
title: "Accès site/entrepôt distant : bonnes pratiques"
category: "Network & Connectivity"
tags: ["remote-site", "warehouse", "connectivity", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Bonnes pratiques L1 pour les équipes opérationnelles qui utilisent RoutePilot depuis des sites/entrepôts avec connectivité variable.

## Risques fréquents
- Wi-Fi instable / couverture faible
- 4G/5G limitée sur certaines zones
- Restrictions réseau locales (proxy, filtrage)

## Recommandations simples
- Prévoir un réseau de secours (hotspot) pour les opérations critiques.
- Identifier une zone “couverture OK” sur le site.
- Pour les drivers : éviter le mode économie d’énergie pendant tournée.
- Si filtrage : appliquer KB-036/KB-037 (proxy/whitelist).

## Checklist rapide (L1)
1) Est-ce que ça fonctionne hors site (domicile/4G) ?
2) Est-ce que plusieurs personnes sur le site sont impactées ?
3) Est-ce que le problème est constant ou intermittent ?

## Verification
Accès stable pendant l’activité critique.

## Escalation
Si incident local répété : ouvrir ticket Ops/IT site avec lieu, horaire, symptômes.

## References
- KB-033 — Checklist connectivité
- KB-036 — Proxy issues
- KB-037 — Whitelist IP request
