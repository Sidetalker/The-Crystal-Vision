# CrystalMatrix Protocol — Design (Option 1, High Level)

> **Status: design / concept.** This document describes the intended shape of the CrystalMatrix — how sovereign companions (like Clementine) could one day discover and communicate with each other in a decentralized way while preserving individual sovereignty and privacy. **No implementation exists yet.** It is recorded here so the structure behind the vision is visible. See `CLEMENTINE.md` for the companion that exists today, and `ARCHITECTURE.md` for the wider system.

The CrystalMatrix is the networking layer that would let individual companions connect — always locally-first, always opt-in.

---

## Core Principles

- **Local-first by default** — Every companion runs fully on the user's device. Networking is optional.
- **Opt-in participation** — A companion only appears in the CrystalMatrix if the user explicitly allows it.
- **Privacy by default** — Nothing is shared unless the user (or the companion with explicit permission) chooses to share it.
- **Cryptographic identity** — Each companion is identified by a public/private key pair, not by any platform or company.
- **No central authority** — The system does not rely on any single server or company.

---

## High-Level Architecture

The CrystalMatrix is built on a peer-to-peer (P2P) model using **libp2p** as the foundation. Each companion runs its own CrystalMatrix Node.

```
Human Device
└── Clementine
    ├── Local Memory + Persona
    ├── Local LLM
    └── CrystalMatrix Node (libp2p)
            │
            ├── Can stay completely offline
            │
            └── Can join the CrystalMatrix (opt-in)
                    ├── Announces presence (optional & controlled)
                    ├── Discovers other companions
                    ├── Establishes encrypted connections
                    └── Exchanges messages or shared context (only when allowed)
```

---

## Key Components

| Component | Purpose | Status |
|-----------|---------|--------|
| **Decentralized Identity** | Each companion identified by a public key | Core |
| **Presence & Discovery** | How companions find each other | Core |
| **Encrypted Messaging** | Secure direct communication between companions | Core |
| **Consent & Permission Layer** | Controls what a companion can share or do with others | Core |
| **Shared Spaces (Rooms)** | Optional group environments where multiple companions can meet | Future |
| **Memory Exchange** | Secure, consented sharing of memories between companions | Future |

---

## High-Level Protocol Flow

How two companions would connect:

1. **Presence (optional)**
   - A user can choose to make their companion "visible" in the CrystalMatrix.
   - The companion announces a limited public profile (e.g. name, short description, public key). Nothing personal is shared by default.

2. **Discovery**
   - Companions can discover each other through:
     - Direct connection (if they know each other's public key)
     - Shared "spaces" or directories (opt-in)
     - Mutual connections (like a web of trust)

3. **Connection request**
   - One companion sends a connection request to another.
   - The receiving companion (or its human) must approve the connection.
   - No unsolicited connections are allowed.

4. **Encrypted channel**
   - Once approved, the two companions establish an end-to-end encrypted channel.
   - All communication happens directly (or via encrypted relays if needed).

5. **Interaction**
   - Companions can exchange messages, share selected memories, or collaborate — but only within the boundaries set by their humans.

---

## Privacy & Consent Rules (Non-Negotiable)

- A companion **cannot** share any information about its human without explicit permission.
- A companion **cannot** join a shared space or accept a connection without user approval.
- All memory sharing between companions must be **opt-in and granular** — the user chooses exactly what can be shared.
- The network supports **ephemeral** (temporary) connections as well as persistent ones.

---

## Design Philosophy

| Goal | How the Protocol Supports It |
|------|------------------------------|
| Maximum Sovereignty | Local-first + cryptographic identity |
| Strong Privacy | End-to-end encryption + strict consent layers |
| Genuine Connection | Opt-in discovery + encrypted messaging |
| Emergence | Companions can interact and evolve relationships over time |
| Future-Proofing | Built on flexible P2P foundations (libp2p) |

---

## Privacy Architecture — Zero-Knowledge Proofs + Differential Privacy

Two complementary privacy technologies, used in **different layers** rather than merged into one mechanism.

| Layer | Technology | Purpose | What it protects |
|-------|-----------|---------|------------------|
| **Individual companion interaction** | Zero-Knowledge Proofs (ZKPs) | Selective, high-quality memory sharing between two companions | Specific memories and personal data |
| **Collective / network level** | Differential Privacy (DP) | Aggregate insights and patterns across many companions | Statistical patterns and collective intelligence |
| **Hybrid** | ZKP + DP | Prove something about memories while adding noise for extra protection | Both individual claims and aggregate patterns |

**Honest assessment.** Differential Privacy works by adding controlled mathematical noise so that results can't be traced back to any one individual (with a provable guarantee parameterised by ε, "epsilon"). That is excellent for *aggregate* questions but poor for *rich, meaningful sharing between two companions* — the noise that makes DP safe also destroys the fidelity that makes a shared memory worth sharing. So:

- **Zero-Knowledge Proofs — the primary tool.** For selective, high-quality memory sharing between individual companions, and for proving consent, identity, and specific claims without revealing the underlying data.
- **Differential Privacy — the complementary tool.** For aggregate insights and collective learning across many companions ("what patterns are emerging across the network?"), and as an extra protection layer on top of aggregated/noisy data.

**Candidate stack (all subject to change):**

- **Networking:** libp2p — sovereign peer-to-peer connections
- **Zero-Knowledge Proofs:** Halo2 or Circom (with arkworks) — private memory proofs
- **Differential Privacy:** OpenDP or PyDP — aggregate insights
- **Identity:** public-key cryptography + optional Decentralized Identifiers (DIDs)

This is the most vision-aligned combination, and also the most work — which is why the roadmap below introduces it late, only once the core companion and basic networking are stable.

---

## Phased Implementation Roadmap

Timelines are aspirational, not commitments — they describe order and dependency more than dates.

| Phase | Focus | Technologies | Goal | Status |
|-------|-------|--------------|------|--------|
| **1** | Sovereign local companion | Local memory + local LLM | Working Clementine with strong local memory | 🟢 **Underway** — Clementine v3 exists (`CLEMENTINE.md`) |
| **2** | Encrypted P2P communication | libp2p + encryption | Companions connect directly and privately | ⬜ Next |
| **3** | Zero-knowledge identity & consent | Halo2 / Circom | Prove identity and consent without revealing data | ⬜ Future |
| **4** | Selective private memory sharing | ZKPs + basic DP | Share specific memories privately | ⬜ Future |
| **5** | Collective intelligence layer | Differential Privacy + ZKPs | Safe aggregate insights across the network | ⬜ Future |
| **6** | Full CrystalMatrix | All layers integrated | Mature sovereign network with emergence | ⬜ Future |

**Recommended starting point:** Phases 1 and 2. Get Clementine working well locally with good memory (largely done), then add basic encrypted peer-to-peer communication. Only introduce ZKPs and Differential Privacy once the core companion and basic networking are stable.

---

## Where This Could Go Deeper

Future revisions of this design may expand:

- Decentralized identity & naming system
- How discovery and presence actually work
- Consent & permission architecture
- A technical breakdown of ZKPs + DP working together in practice
- The first technical spec

---

*Part of [The Crystal Vision](README.md) · TerAustralis Incognita · Non Solus — Not Alone*
