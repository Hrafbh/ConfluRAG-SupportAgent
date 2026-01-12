---
id: KB-041
title: "Statut plateforme : comment vérifier & communiquer"
category: "Network & Connectivity"
tags: ["status", "incident", "communication", "support-l1"]
last_reviewed: "2026-01-08"
---
## Summary
Procédure L1/L2 pour vérifier si RoutePilot rencontre un incident global et pour communiquer proprement (sans spéculer).

## Quand utiliser
- Plusieurs utilisateurs signalent “ça ne marche pas”
- Erreurs simultanées sur login, mobile, exports, ou chargement
- Dégradation perçue sur plusieurs régions/tenants

## Resolution steps
1) Vérifier les signaux internes disponibles :
   - message interne / canal incident (si existant)
   - page statut (si existante) ou annonce Ops
2) Si aucun signal disponible :
   - collecter 3 exemples minimum (tenant, heure, module, capture)
   - qualifier : total down vs lent vs module spécifique
3) Répondre au client/utilisateur :
   - accuser réception
   - indiquer que l’équipe vérifie
   - donner un délai de prochaine mise à jour (ex: 30–60 min)

## Modèle de message (support)
Bonjour, merci pour votre signalement. Nous avons identifié une dégradation potentielle et l’équipe est en cours d’investigation.  
Nous vous tenons informés dès que nous avons une mise à jour. Prochaine communication au plus tard : **[heure]**.

## Verification
Confirmation d’incident (ou non) et communication envoyée.

## Escalation
Si incident confirmé : activer runbook “plateforme indisponible” (KB-053).

## References
- KB-053 — Runbook plateforme indisponible
- KB-060 — Template communication major incident
