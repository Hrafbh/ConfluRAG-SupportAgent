---
id: KB-002
title: "Onboarding client : étapes standard (checklist)"
category: "Onboarding & Access"
tags: ["onboarding", "checklist", "tenant", "support-l1"]
last_reviewed: "2026-01-07"
---
## Summary
Checklist d’onboarding pour créer un tenant, activer les accès, sécuriser l’entrée en production et éviter 80% des incidents “jour 1”.

## Checklist (L1/L2)
1) Identifier : nom client, contact admin, fuseau horaire, langue.
2) Créer le tenant (ou vérifier qu’il existe).
3) Créer le compte Admin initial + inviter les utilisateurs clés.
4) Définir rôles : Dispatcher / Manager / Driver / Viewer.
5) Configurer paramètres de base :
   - plages horaires opérationnelles
   - types de missions (livraison/ramassage)
   - règles POD (photo obligatoire, signature, etc.)
6) Vérifier l’accès à l’app web (navigateur supporté) + app mobile.
7) Test “bout en bout” :
   - créer une tournée test
   - affecter un driver
   - simuler un statut + POD
8) Former : 30 minutes sur “tournées + statuts + POD”.

## Verification
Le client confirme : connexion OK, 1 tournée test exécutée, POD visible dans le reporting.

## Escalation
Si blocage SSO/SCIM ou erreur persistante, escalader avec tenant_id + horodatage + capture erreur.

## References
- (À compléter) “Créer tenant + Admin”
