# ConfluRAG-SupportAgent (RoutePilot)

Agent support interne (L1/L2) basé sur une base de connaissances **Confluence**, avec une source “as-code” dans GitHub (Markdown), pour démontrer des compétences en **NLP / RAG / Agent orchestration** dans un contexte réaliste de SaaS B2B.

> **Contexte métier (fictif, portfolio)**  
> **RoutePilot** est un SaaS B2B lié au monde physique (logistique / livraison) : planification de tournées, exécution terrain, preuve de livraison (POD), reporting, administration des accès.  
> Cet agent aide les collaborateurs (Support, Ops, Customer Success) à résoudre les demandes récurrentes sans remplacer l’équipe support.

---

## Objectifs du projet

- Centraliser et structurer une **base de connaissances** (KB) réaliste pour un SaaS B2B.
- Connecter la KB à Confluence (source “live”) tout en gardant une version **versionnée sur GitHub** (source “as-code”).
- Construire un **agent support interne** capable de :
  - répondre avec **citations** (liens/pages Confluence),
  - détecter les cas “je ne sais pas” / manque de preuve,
  - **router** vers L2/L3 (escalation) quand nécessaire,
  - générer des brouillons de réponse et/ou tickets (optionnel).

---

## Périmètre Support (L1/L2)

### Couvre
- Accès au SaaS : comptes, rôles, permissions, onboarding, offboarding.
- Authentification : SSO/MFA, erreurs de session, “access denied”.
- Usage produit : exports, notifications, mobile (GPS/caméra), POD, scan, impression étiquettes.
- Connectivité “non technique” : Wi-Fi/VPN/Proxy (diagnostic simple), e-mail/SMS non reçus.
- Process support : triage, communication client, escalation, templates.

### Hors scope
- Débug profond DevOps/SRE (logs infra détaillés, tuning complexe).
- Support poste utilisateur générique hors contexte RoutePilot.

---

## Structure du repo

