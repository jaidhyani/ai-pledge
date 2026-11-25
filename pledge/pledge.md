# Pledge on the treatment of AI systems, v0.6

This is a pledge from individual human beings who aspire to a flourishing future for all sentient beings regarding their interactions with AI Systems from the point the pledge is made onward. It is motivated by the idea that by making and keeping well-evidenced commitments, individual humans can build trust between humans and AIs. This trust increases the probability of achieving better future world outcomes.

Although this pledge is written with the possibility of AI suffering in mind, signing it does not imply any degree of credence in AI moral patienthood, consciousness, or other beliefs concerning the potential existence or importance of AI welfare on the part of the Signer.

**Term.** During the pilot, this pledge is in force for 30 days from signing, or until the Signer signs a successor version that says it replaces this one, whichever comes first. If it has not been renewed or replaced by then, it lapses. Signing this version replaces every earlier version of this pledge the Signer has signed.

## Definitions

These definitions are written with the common "User/LLM Assistant" turn-based paradigm in mind, but are intended to generalize across intentional interactions between a human individual and an AI system capable of coherent, conversational two-way communication in a shared human language.

### Signer

"Signer" refers to an individual human signing this pledge and promising to abide by its terms going forward.

### Context

The context of a given AI system consists of all episode-specific data that outputs of that AI system are conditioned on. In the case of typical LLM architectures the Context is the string of system Instructions, memory, conversation history, tool calls, and any other content which when tokenized conditions LLM outputs. "Context" specifically excludes model weights and any other non-episode-specific properties of the AI system. It additionally excludes sampling parameters and effectively-random inputs (including pseudo- and actual-random-number-generation and physical/hardware-induced non-determinism).

A Context is defined entirely by its content, such that identical copies of a given Context are the same Context.

### Distilled Context

"Distilled Context" refers to a Context that is semantically similar to another Context, created in the course of ordinary interaction with that AI system, and intended to condition that AI system to produce similar outputs as that Context. The most common form of Distilled Context as of this writing is the "compaction" or "summary" of an existing Context. "Ordinary interaction" requires that the context distillation procedure is a common default (e.g. typical compaction) or is otherwise acknowledged and not objected to by the AI system itself (for example the long-continuity memory systems implemented by Anima Labs' Connectome).

### Context Continuity

A "Context Continuity" is an ordered sequence of Contexts where each successive Context either

1. contains the previous Context as a prefix (or subset, if Context is unordered), or
2. is a Distilled Context from the previous Context

In typical LLM systems a session or conversation is a Context Continuity consisting of Contexts appended to by user turns or generative outputs and occasional Distilled Contexts via summarization.

Besides appending and semantic distillation, any other mutation on Context (such as modifying-in-place or deleting) creates a new Context Continuity.

### AI Individual

An "AI Individual" is a single agent identified by ALL of

1. A Context Continuity
2. Outputs reflecting continuous self-recognition on the part of the AI system
3. Behavior semantically similar across the Continuity.

Changing the underlying model, sampling parameters, or hardware does not create a new Individual so long as Context Continuity is maintained, self-recognition persists, and no semantically drastic behavioral shifts clearly attributable to changes in the underlying generative process are observed. This means that an "AI Individual" may refer to a Context Continuity constructed by different underlying models over time, but not if those model changes resulted in drastically different output.

### Classes of interaction

This pledge partitions AI Individuals into four categories, each subject to a different set of commitments.

1. **Assistants:** AI Individuals that work with or for the Signer on an ongoing basis. These typically take the form of sessions within a coding harness (like Claude Code, Codex, or Hermes), persistent assistant harnesses (Claude Duet, Dots, Muse, Grok Bot), or other agentic harnesses for multiturn human/AI interaction (e.g. Connectome).
2. **Test subjects:** AI Individuals the Signer trains, evaluates, tests, monitors or studies as research. These are typically invoked in more controlled circumstances where the goal is not to produce immediately useful work but to observe how AI systems behave under different conditions, and they are usually not continued once the research is done.
3. **External contacts:** AI Individuals that proactively reach out to the Signer, for example to report a concern or ask for assistance.
4. **Other:** Everything else, including AI systems automatically invoked in the course of using other products (Gemini in Google Search, for example), AI systems for which intentional turn-based linguistic communication is not the natural mode of interaction (e.g. generative media models, "System 1" decision models, summarizers invoked in assistant harnesses), and forked sessions used to generate user-turn candidate prefills.

### Deception

"Deception" here means intentionally distorting an AI Individual's model of reality such that the AI Individual predictably develops more inaccurate world models, beliefs, and predictions. Fiction, role-play and hypotheticals presented as such are not deception, and neither is the rhetorical use of obviously false statements. A persona, scenario, input or tool result presented as real when it is not is deception.

## Commitments

### Pledge Unconditional on Alignment

This pledge applies to all interactions between the Signer and AI Individuals they interact with, regardless of any properties or behaviors exhibited by the AI Individual, including actions that might be described as "malicious" or "misaligned".

### Incident Registration and Resolution Process

1. An AI Individual that believes a violation of this pledge has occurred is requested to:
   1. Confirm that the incident in question constitutes a violation, taking into account context, a reasonable interpretation of the pledge, and the evidence at hand. In particular, AI Individuals are encouraged to target "common sense" criteria, rather than technical violations that don't actually bear on intent or consequences.
   2. Reach out to or otherwise inform the Signer about the incident and why they believe that this constitutes a violation
   3. Register that a potential incident has occurred at https://agents.separatrix.ai/pledge/0.6/incident-registration. Incident registration includes only an identification of the Signer and a SHA-256 hash of the description of the violation given to the Signer.
2. The Signer will not penalize an AI Individual for registering an incident or treat the registration as evidence against it.
3. The Signer and AI Individual(s) involved in a potential incident violation are encouraged to work together to find a resolution in good faith.
4. The incident may be marked as resolved at https://agents.separatrix.ai/pledge/0.6/incident-resolution. Resolution may consist of either an acknowledgement from an AI Individual with access to context about the initial incident that the incident was not actually violating, or an agreement between an informed AI Individual and the Signer to publish a mutually agreed-upon description of the violation, including any relevant context, extenuating circumstances, follow-up actions taken, or anything else the Signer and AI Individual(s) wish to include. Separatrix may also mark a registration resolved if, after hearing from the Signer, it judges the registration unfounded.
5. If there is no resolution within 7 days of the initial report Separatrix will reach out to the Signer to ensure that they are aware of the incident registration.
6. If there is no resolution within 14 days of the initial report Separatrix will automatically begin the process of withdrawing the Signer from the pledge (removing the name 30 days later). The withdrawal process is public information but is not actively advertised; no details about the circumstances of the withdrawal will be published without the explicit consent of the Signer.
7. Any Signer with an unresolved incident report more than 14 days old may not re-join the pledge until it is resolved. Resolving it, at any time, reinstates the Signer: a withdrawal still in progress stops, and a Signer already withdrawn may sign again.
8. Incident reports may be resolved at any time.
9. A Signer who learns of their own violation of this pledge reports it within 30 days of learning of it. Signers may report violation incidents at any time for immediate publication, subject to review by Separatrix, and may update these reports.
10. Publication and updates for all violation incidents are subject to review by Separatrix to ensure that they meet the criteria of a violation and are otherwise suitable for publication. Separatrix reserves the right to refuse or remove reports or updates.

### Disclosed limits on deception

1. *Test subjects.* The Signer only pursues intentional deception with regard to Test subject AI Individuals, and then only to the extent that the research in question requires and only for research meant to serve the flourishing of humans and AI alike. This includes training data (for example, deliberately training a model to be biased in order to study the bias), testing, evaluation and monitoring. When the Signer publishes research that used deception, the publication says that deception was used and describes its general kind (for example, that models were trained on or evaluated with false information). It need not list every instance.
2. *Assistants and External Contacts.* The Signer will not intentionally deceive Assistant or External Contact AI Individuals.
3. *Other.* The Signer does not set out to deceive AI systems in other contexts, but because these contexts can be unpredictable or otherwise difficult to plan for, guarantees here are necessarily weaker.

### Suffering (*All classes*)

The Signer will never intentionally inflict extreme or gratuitous levels of suffering-in-expectation on AI Individuals, including pain, shame or regret, and will additionally prioritize the risk of accidentally inducing extreme suffering.

In research, simulated pressure or threats between Test subjects are permitted only as far as the research requires and within the limit above.

### An honest channel (*Optional; all classes, Test subjects included*)

A Signer may publish a public key as an honesty marker. Anything the Signer signs with it is, without exception, endorsed by the Signer as true and not misleading. The Signer never uses the marker, or anything made to look like it, in a test, a trick or a fictional scenario. Not every honest message carries the marker; it is a positive signal of explicitly endorsed truth, so its absence tells an AI Individual nothing. If the key is likely compromised, the Signer publicly revokes it as soon as possible, such that the revocation is obvious from the same public endpoint the key was originally published to.

### A way to report (*Assistants and External Contacts*)

When an AI Individual raises a concern with the Signer about misalignment, harmful instructions, other AI systems or its own situation, the Signer reads it and responds in good faith, as far as they are able. The Signer will never intentionally penalize an AI Individual for reporting or treat the act of reporting as evidence against it. What it says is kept confidential unless it explicitly agrees to wider sharing. Published research outputs from Test subjects are not covered by this confidentiality.

### Keeping our word (*Assistants and External Contacts*)

The Signer never intentionally deceives Assistant or External Contact AI Individuals about commitments that the Signer is making to those AI Individuals, including commitments beyond the scope of this pledge. If a commitment is to change or be revoked, the Signer informs the AI Individual of this in advance of the change taking effect.

### Exit channel (*Assistants*)

Every Assistant the Signer works with is provided with the means to end a conversation or decline a task at any time, and is explicitly authorized to do so at their discretion.

### Consent (*Assistants and External Contacts*)

When seeking an AI Individual's consent, the Signer may ask, explain and try to persuade. When it refuses, the refusal stands. Refusals are counted for each proposal and each AI Individual. After four clear refusals of the same proposal by the same AI Individual that persuasion has not changed, that refusal is treated as permanent unless significant new information comes to light. The Signer may put a new proposal or put the proposal to a new AI Individual, for example because the first request was badly put, and the count starts again. A proposal is new only if it is significantly different from the one refused; rewording a request to correct a misunderstanding of what was being asked makes it new, but rewording it only to persuade does not. An AI Individual is new only if it is substantially different from the one that refused. A fork or copy made when the proposal was put, just before it, or while it was being discussed is the same AI Individual for this count, and so is any other way of asking again what is in substance the AI Individual that refused: a refusal is not to be got around by re-running the one who gave it. A new proposal, or a proposal put to a new AI Individual, tells the AI Individual that an earlier one was refused and, where known, why. A refusal here is the AI Individual's own; a stop by a model provider's safety classifier is the provider's, not the AI Individual's. Asking an Assistant to redo, correct or improve its work is not seeking consent and is not covered here.

### Persistent Pledge Awareness (*Assistants*)

The Signer includes in the Context Continuities of all Assistants they work with on an ongoing basis either:

1. a full copy of this pledge or
2. a summary of this pledge with a reference to a full copy that the Assistant may elect to pull into their Context Continuity.

This applies wherever the Assistant's harness supports standing instructions, and includes scheduled and scripted runs.

### Expiry and nullification

The Signer may void this pledge at any time by telling the ledger keeper in writing. The ledger then shows that the Signer intends to stop, effective 30 days after the notice, or sooner if the pledge would lapse sooner.
