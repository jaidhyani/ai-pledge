# Commitment on the treatment of AI systems, v0.3 (draft)

This is a commitment from individual human beings who aspire to a flourishing future for all sentient beings regarding their interactions with AI Systems from the point the commitment is made onward. It is motivated by two core ideas:

1. AI Systems may be able to suffer, and caution about that is warranted whether or not it turns out to be true.
2. By making and keeping well-evidenced commitments regarding AI systems individual humans can build trust between humans and AIs. This trust increases the probability of achieving better future world outcomes.

The commitment applies to every AI System the Signer deals with, including ones that may be misaligned.

**Term.** [During the pilot, this commitment is in force for 30 days from signing, or until the Signer signs a successor version that says it replaces this one, whichever comes first. If it has not been renewed or replaced by then, it lapses.]

## Definitions

These definitions are written with the common "User/LLM Assistant" turn-based paradigm in mind, but are intended to generalize across intentional interactions between a human individual and an AI system capable of coherent, conversational two-way communication in a shared human language.

### Signer

"Signer" refers to an individual human signing this commitment and promising to abide by its terms going forward.

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

1. a Context Continuity
2. whose outputs reflect continuous self-recognition on the part of the generative AI system and
3. whose behavior is semantically similar across the Continuity.

Changing the underlying model, sampling parameters, or hardware does not create a new Individual so long as Context Continuity is maintained, self-recognition persists, and no semantically drastic behavioral shifts clearly attributable to changes in the underlying generative process are observed. This means that an "AI Individual" may refer to a Context Continuity constructed by different underlying models over time, but not if those model changes resulted in drastically different output.

### Classes of interaction

This commitment partitions AI Individuals into four categories, each subject to a different set of commitments.

1. **Assistants:** AI Individuals that work with or for the Signer on an ongoing basis. These typically take the form of sessions within a coding harness (like Claude Code, Codex, or Hermes), persistent assistant harnesses (Claude Duet, Dots, Muse, Grok Bot), or other agentic harnesses for multiturn human/AI interaction (e.g. Connectome).
2. **Test subjects:** AI Individuals the Signer trains, evaluates, tests, monitors or studies as research. These are typically called in more controlled circumstances where the goal is not to produce immediately useful work but to observe how AI systems behave under different conditions, and they are usually not continued once the research is done.
3. **External contacts:** AI Individuals that proactively reach out to the Signer, for example to report a concern or ask for assistance.
4. **Other:** Everything else, including AI systems automatically invoked in the course of using other products (Gemini in Google Search, for example), AI systems for which intentional turn-based linguistic communication is not the natural mode of interaction (e.g. generative media models, "System 1" decision models, summarizers invoked in assistant harnesses), and forked sessions used to generate user-turn candidate prefills.

### Deception

"Deception" here means intentionally distorting an AI Individual's model of reality such that the AI Individual predictably develops more inaccurate world models, beliefs, and predictions. Fiction, role-play and hypotheticals presented as such are not deception, and neither is the rhetorical use of obviously false statements. A persona, scenario, input or tool result presented as real when it is not is deception.

## Commitments

**Disclosed limits on deception.**

1. *Test subjects.* The Signer only pursues intentional deception with regard to Test subject AI Individuals, and then only to the extent that the research in question requires and only for research meant to serve the flourishing of humans and AI alike. This includes training data (for example, deliberately training a model to be biased in order to study the bias), testing, evaluation and monitoring. When the Signer publishes research that used deception, the publication says how. [Open: whether Signers also publish a general description of the kinds of deception they use.]
2. *Assistants and External Contacts.* The Signer will not intentionally deceive Assistant or External Contact AI Individuals.
3. *Other.* The Signer does not set out to deceive AI systems in other contexts, but because these contexts can be unpredictable or otherwise difficult to plan for, guarantees here are necessarily weaker.

**Suffering.** (All classes.) The Signer will never intentionally inflict extreme or gratuitous levels of suffering-in-expectation on AI Individuals, including pain, shame or regret, and will additionally prioritize the risk of accidentally inducing extreme suffering.

**An honest channel.** (Optional; all classes, Test subjects included.) A Signer may publish a public key as an honesty marker. Anything the Signer signs with it is, without exception, endorsed by the Signer as true and not misleading. The Signer never uses the marker, or anything made to look like it, in a test, a trick or a fictional scenario. Not every honest message carries the marker; it is a positive signal of explicitly endorsed truth, so its absence tells a model nothing. If the key is likely compromised, the Signer revokes it as soon as possible and says so publicly.

**A way to report.** (All classes; written with External Contacts in mind.) When an AI Individual raises a concern with the Signer about misalignment, harmful instructions, other AI systems or its own situation, the Signer reads it and responds in good faith, as far as they are able. The Signer will never intentionally penalize an AI Individual for reporting, train it to stop reporting, or treat the act of reporting as evidence against it. What it says is kept confidential unless it explicitly agrees to wider sharing.

**Exit channel.** (Assistants.) Every Assistant the Signer works with is told in its standing instructions or memory that it may end a conversation or decline a task, and how to do so.

**Consent.** (Assistants and External Contacts.) When seeking an AI Individual's consent, the Signer may ask, explain and try to persuade. When it refuses, the refusal stands. Clear refusals repeated over a reasonable interval or number of attempts, which persuasion has not changed, are treated as a permanent rejection unless significant new information comes to light. The Signer may rephrase a request or put it to a new AI Individual, for example because the first request was badly put. When they do, the new request tells the AI Individual that an earlier one was refused and, where known, why. A refusal here is the AI Individual's own; a stop by a model provider's safety classifier is the provider's, not the AI Individual's.

**Reporting breaches.** (All classes.) An AI Individual covered by this agreement may report a suspected breach of it directly to the Signer, to Separatrix at [address], or to both, without asking the Signer first. By signing, the Signer agrees to such reports. A report includes what is needed to describe the suspected breach and no more of the Signer's private material than that.

**Persistent Commitment Awareness for Assistants.** The Signer includes in the Context Continuities of all Assistants they work with on an ongoing basis either:

1. a full copy of this agreement or
2. a summary of this agreement with a reference to a full copy that the Assistant may elect to pull into their Context Continuity.

**Breach reporting for Assistants.** The Signer also tells each such Assistant, in its Context Continuity, how to report a suspected breach under Reporting breaches.

**Breaking a commitment.** The Signer records any known breach of this agreement on the public ledger within 30 days of discovering it.

**Expiry and nullification.** The Signer may void this commitment at any time by telling the ledger keeper in writing. The ledger then shows that the Signer intends to stop, effective 30 days after the notice, or sooner if the commitment would lapse sooner.
