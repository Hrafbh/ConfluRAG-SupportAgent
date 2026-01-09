---
id: KB-025
title: "Upload de fichiers (photos POD) : échecs & solutions"
category: "Workstation & Mobile"
tags: ["upload", "pod", "photo", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Résolution des échecs d’upload (photo POD, pièces jointes) côté web ou mobile, sans diagnostic technique profond.

## Symptoms
- “Upload failed”
- Photo POD ne s’enregistre pas
- Chargement infini
- Fichier refusé (format/taille)

## Causes fréquentes (non techniques)
- Taille de fichier trop grande
- Format non supporté
- Réseau instable (mobile)
- Permissions caméra/stockage refusées

## Resolution steps
1) Vérifier format et taille :
   - recommander JPG/PNG
   - réduire la taille (photo moins lourde)
2) Tester un autre réseau (4G vs Wi-Fi) si mobile.
3) Vérifier permissions (caméra/stockage) si mobile (KB-029).
4) Sur web : tester navigation privée, désactiver extensions pour test.
5) Réessayer après déconnexion/reconnexion.

## Verification
La photo est visible dans la livraison et consultable dans le détail.

## Escalation
Si le problème touche plusieurs drivers : escalader comme incident “POD upload”.

## References
- KB-029 — Photo/signature POD : caméra & droits
- KB-040 — Mobile : sync lente/KO
