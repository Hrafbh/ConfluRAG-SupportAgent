---
id: KB-028
title: "GPS/localisation : permissions & diagnostics simples"
category: "Workstation & Mobile"
tags: ["gps", "location", "mobile", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
La localisation est utilisée pour certaines fonctions (navigation, ETA, preuve terrain). Cette page couvre les blocages les plus fréquents.

## Symptoms
- Carte ne se centre pas
- “Localisation désactivée”
- ETA incohérents côté driver
- App demande permission en boucle

## Resolution steps
1) Vérifier que la localisation du téléphone est activée.
2) Vérifier la permission RoutePilot :
   - Autoriser pendant l’utilisation (recommandé)
3) Vérifier mode économie d’énergie (peut limiter GPS).
4) Redémarrer l’app.
5) Tester en extérieur (GPS faible en intérieur).

## Verification
La position se met à jour et la carte fonctionne.

## Escalation
Si un tenant complet signale des ETA incohérents : ouvrir ticket L2 (potentiel incident données/ETA).

## References
- KB-057 — Runbook carte/ETA incohérents
