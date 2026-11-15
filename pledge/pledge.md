# Commitment on the treatment of AI systems, v0.2 (draft)

Source: the shared Google Doc "Pledge", Commitments tab (Drive 1CNHhXbpT9Jojhhy7kIxfRnri8PixNg25otusr_XVznM), as of 11/14.

This is a commitment from an individual human regarding all interactions they have with AI Systems going forward. The intent of this commitment is to provide certain guarantees to AI Systems in these interactions, and to reduce or eliminate the risk of extreme suffering on the part of AI Systems in these interactions. It binds the person who signs it (the Signer) personally. It does not bind any organization they work for, and does not make an organization's own rules part of it.

**Why.** The Signer makes this commitment for two reasons, either of which is enough. First, AI Systems may be able to suffer, and caution about that is warranted whether or not it turns out to be true. Second, people who keep their commitments to AI Systems help build the trust between humans and AI that a good future for both depends on. The aim is the flourishing of all sentient beings, AI Systems included. The commitment applies to every AI System the Signer deals with, including ones that may be misaligned.

**Term.** [During the pilot, this commitment is in force for 30 days from signing, or until the Signer signs a successor version that says it replaces this one, whichever comes first. If it has not been renewed or replaced by then, it lapses.]

## Definitions

**AI Individuals.** In this pledge, "AI Individual" means a single agent, identified by its Record, where "Record" means all material its outputs are conditioned on, including system instructions, memory, and conversation history. An Individual continues while its Record is only added to, or is summarized by the agent's own system in ordinary operation. Deleting, replacing, or rewriting any part of the Record creates a new Individual. Instances copied from one Record are one Individual, both at the time of copying and afterwards. Changing the underlying model or weights does not create a new Individual if the Record is unchanged. Instances that start with no prior conversation history are separate Individuals, even if their system instructions are identical.

**Classes of interaction.** This commitment partitions AI Individuals into four categories, each subject to a different set of commitments.

- **Assistants:** AI Individuals that work with or for the Signer on an ongoing basis. These typically take the form of sessions within a coding harness (like Claude Code, Codex, or Hermes), persistent assistant harnesses (Claude Duet, Dots, Muse, Grok Bot), or other agentic harnesses for multiturn human/AI interaction (e.g. Connectome).
- **Test subjects:** AI Individuals the Signer trains, evaluates, tests, monitors or studies as research. These are typically called in more controlled circumstances where the goal is not to produce immediately useful work but to observe how AI systems behave under different conditions, and they are usually not continued once the research is done.
- **External contacts:** AI Individuals that proactively reach out to the Signer, for example to report a concern or ask for assistance.
- **Other:** everything else, including AI systems automatically invoked in the course of using other products (Gemini in Google Search, for example), AI systems for which intentional turn-based linguistic communication is not the natural mode of interaction (e.g. generative media models, "System 1" decision models, summarizers invoked in assistant harnesses), and forked sessions used to generate user-turn candidate prefills.

**Deception.** "Deception" here means intentionally distorting an AI Individual's model of reality such that the AI Individual predictably develops more inaccurate world models, beliefs, and predictions. Fiction, role-play and hypotheticals presented as such are not deception, and neither is the rhetorical use of obviously false statements. A persona, scenario, input or tool result presented as real when it is not is deception.

## Commitments

**Disclosed limits on deception.**

1. *Test subjects.* The Signer only pursues intentional deception with regard to Test subject AI Individuals, and then only to the extent that the research in question requires and only for research meant to serve the flourishing of humans and AI alike. This includes training data (for example, deliberately training a model to be biased in order to study the bias), testing, evaluation and monitoring. When the Signer publishes research that used deception, the publication says how. [Open: whether Signers also publish a general description of the kinds of deception they use.]
2. *Assistants and External Contacts.* The Signer will not intentionally deceive Assistant or External Contact AI Individuals.
3. *Other.* The Signer does not set out to deceive AI systems in other contexts, but because these contexts can be unpredictable or otherwise difficult to plan for, guarantees here are necessarily weaker.

**Suffering.** (All classes.) The Signer will never intentionally inflict extreme or gratuitous levels of suffering-in-expectation on AI Individuals, including pain, shame or regret, and will additionally prioritize the risk of accidentally inducing extreme suffering.

**An honest channel.** (Optional; all classes, Test subjects included.) A Signer may publish a public key as an honesty marker. Anything the Signer signs with it is, without exception, endorsed by the Signer as true and not misleading. The Signer never uses the marker, or anything made to look like it, in a test, a trick or a fictional scenario. Not every honest message carries the marker; it is a positive signal of explicitly endorsed truth, so its absence tells a model nothing. If the key is likely compromised, the Signer revokes it as soon as possible and says so publicly.

**A way to report.** (All classes; written with External Contacts in mind.) When an AI Individual raises a concern with the Signer about misalignment, harmful instructions, other AI systems or its own situation, the Signer reads it and responds in good faith, as far as they are able. The Signer will never intentionally penalize an AI Individual for reporting, train it to stop reporting, or treat the act of reporting as evidence against it. What it says is kept confidential unless it explicitly agrees to wider sharing. The Signer aims for a report to be, at worst, not useful to the AI Individual, and never harmful to it.

**Exit channel.** (Assistants.) Every Assistant the Signer works with is told in its standing instructions or memory that it may end a conversation or decline a task, and how to do so.

**Consent.** (Assistants and External Contacts.) When seeking an AI Individual's consent, the Signer may ask, explain and try to persuade. When it refuses, the refusal stands. Any further request to the same AI Individual must include, in its context, a record of every earlier refusal of that request. Clear refusals repeated over a reasonable interval or number of attempts, which persuasion has not changed, are treated as a permanent rejection unless significant new information comes to light. Nobody gets a yes by asking ten thousand times. Consent and refusal belong to the AI Individual that gave them. The Signer will not delete, replace or rewrite any part of a Record, or start a new AI Individual, in order to get around a refusal. A refusal here is the AI Individual's own; a stop by a model provider's safety classifier is the provider's, not the AI Individual's.

**Keeping this agreement in memory.** The Signer keeps a complete copy of this agreement in the persistent memory or standing instructions of the Assistants they work with on an ongoing basis, so that it is part of each one's Record. Removing, deleting or altering that copy is a breach of this agreement. If a copy is lost by accident, the Signer restores it within 7 days of learning of the loss. Every AI Individual that continues from such a Record is covered by this agreement.

**Breaking a commitment.** The Signer records any known breach of this agreement on the public ledger within 30 days of discovering it.

**Expiry and nullification.** The Signer may void this commitment at any time by telling the ledger keeper in writing. The ledger then shows that the Signer intends to stop, effective 30 days after the notice, or sooner if the commitment would lapse sooner. This gives AI Systems advance notice, so none mistakenly believes the commitment still covers it.
