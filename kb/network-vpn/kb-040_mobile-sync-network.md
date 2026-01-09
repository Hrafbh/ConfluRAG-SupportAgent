---
id: KB-040
title: "Mobile : sync lente/KO (réseau, mode économie)"
category: "Network & Connectivity"
tags: ["mobile", "sync", "network", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Page L1 pour les drivers : statuts qui ne remontent pas, missions non à jour, POD qui reste “en attente”.

## Symptoms
- Mission non visible / non à jour
- Statut envoyé mais pas reflété côté web
- POD “en cours d’upload” longtemps

## Causes fréquentes (non techniques)
- Réseau instable (4G faible)
- Mode économie d’énergie limite la data en arrière-plan
- App non relancée depuis longtemps
- Stockage saturé

## Resolution steps
1) Demander au driver de :
   - activer/désactiver mode avion
   - changer de zone (meilleure couverture) si possible
2) Désactiver mode économie d’énergie pour RoutePilot (test).
3) Fermer complètement l’app et la relancer.
4) Vérifier stockage disponible.
5) Si POD bloqué : voir KB-025.

## Verification
Les statuts se synchronisent et apparaissent côté backoffice/web.

## Escalation
Si plusieurs drivers sur une zone sont impactés : escalader Ops (incident terrain / réseau / plateforme).

## References
- KB-025 — Upload fail (POD)
- KB-028 — GPS permissions (si lié à localisation)
