---
id: KB-024
title: "Exports PDF/CSV : erreurs fréquentes & correctifs"
category: "Workstation & Mobile"
tags: ["export", "pdf", "csv", "reporting", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Guide L1/L2 pour traiter les incidents “export ne marche pas”, “fichier vide”, “format incorrect”.

## Symptoms
- Export bloqué / bouton inactif
- Fichier téléchargé vide
- CSV illisible (séparateur, encodage)
- PDF incomplet (mise en page)

## Resolution steps
1) Vérifier le navigateur (KB-021) et tester en navigation privée.
2) Vérifier filtre/report sélectionné :
   - dates correctes
   - période non vide
3) Tester un autre format (CSV vs PDF).
4) Vérifier si un bloqueur de popups est actif.
5) Si CSV illisible :
   - recommander l’ouverture via Excel avec séparateur “,” ou “;” selon région.

## Informations à collecter (si escalade)
- tenant, page exacte, filtres appliqués, heure, format, capture.

## Verification
Export généré et contient des lignes attendues.

## Escalation
Si plusieurs utilisateurs impactés : escalader comme incident L2.

## References
- KB-021 — Navigateurs supportés
- KB-052 — Known Issues Log (si déjà identifié)
