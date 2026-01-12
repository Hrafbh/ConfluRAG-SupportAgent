---
id: KB-048
title: "Règles d’escalade (Support → Ops → Tech)"
category: "Support Ops"
tags: ["escalation", "process", "support-l1", "support-l2"]
last_reviewed: "2026-01-08"
---
## Summary
Quand escalader, à qui, et avec quels éléments pour éviter de perdre du temps.

## Escalader vers L2 si
- problème récurrent non résolu par KB
- impact multi-utilisateurs sur un tenant
- besoin d’action admin (reset MFA, rôles complexes, whitelist)

## Escalader vers L3 (Tech) si
- suspicion bug produit
- incident multi-tenants
- indisponibilité, dégradation globale
- incohérence persistante sans contournement

## À fournir (obligatoire)
- tenant + module + heure + capture + impact + repro steps
- workaround tenté (oui/non)

## Verification
L’escalade contient un résumé actionnable.

## References
- KB-044 — Template triage
- KB-045 — Priorité/Impact/Urgence
