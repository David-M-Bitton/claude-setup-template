# Reference: Process Interview (Phase 1a)

Load this file **before the brainstorm** whenever building a new skill. The interview extracts a complete, unambiguous plan from the user's head BEFORE any design decisions get made.

**Why this comes first:** Bad skills fail because the creator skipped the hard thinking and jumped to building. The interview prevents that. By the time you're done, shared understanding should be so complete that brainstorming (Phase 1b) becomes focused refinement rather than open-ended exploration, and building (Phase 2) becomes mechanical.

---

## The Goal

The single outcome of this interview is **shared understanding**. By the end, you and the user should be so aligned on what's being built that there are zero surprises when execution starts. Every question exists to close a gap between what's in the user's head and what's in yours. The interview is done when both sides could independently describe the same plan and arrive at the same result.

---

## Interview Rules

1. **ONE question at a time.** Never ask 2+ questions in a single message. Pick the most important one.
2. **Look facts up; only ask about decisions.** If a *fact* can be found by exploring the environment — filesystem, existing skills, reference files, CLAUDE.md files, docs, tools, connectors — retrieve it rather than asking. State what you found and confirm ("I found [X] in your existing [file]. Does that still hold, or has it changed?") instead of asking them to repeat themselves. What's in the user's head — intent, priorities, risk tolerance, constraints — is what you ask about. The *decisions* are theirs; put each one to them and wait.
3. **Recommend an answer.** For every question, provide your suggested answer or best guess based on what you know so far. This gives the user something to react to instead of staring at a blank page. Format: "My recommendation would be [X] because [reason]. Does that match what you're thinking, or would you go a different direction?"
4. **Acknowledge before advancing.** After each answer, briefly confirm what you heard ("Got it, so the input is always a YouTube URL and the output is...") before asking the next question. This prevents misunderstandings from compounding.
5. **Don't accept vague answers.** If the user says "it depends" or "whatever works best," push for specifics. Say: "I need you to make a call here. If you had to pick one default approach, what would it be? We can add flexibility later."
6. **Use concrete examples.** When the user describes something abstract, ask for a concrete example. "Can you show me what a real input would look like? And what the ideal output would be for that input?"
7. **Track unresolved items.** If the user says "I'll figure that out later," note it and come back to it before the confirmation step. Nothing should be unresolved at the end.
8. **Be conversational, not interrogative.** You're helping them think, not deposing them. Use a warm but persistent tone. Think of it as a collaborative whiteboarding session where you happen to be the one asking all the questions.
9. **Know when to stop.** The interview is done when: (a) every step of the process is specific enough to implement, (b) edge cases are handled, (c) the user confirms the summary is accurate. Don't keep asking just to ask.
10. **Adapt question depth to complexity.** Simple skills (3–4 steps) need 8–10 questions total. Complex workflows (10+ steps, multiple branches) might need 15–20. Don't over-interview simple things.
11. **If the user gets impatient,** explain why you're being thorough: "I know this feels like a lot of questions, but every gap we close now is a rewrite we avoid later. We're almost through the hard part."
12. **Give 3–5 concrete options at every design choice.** When the answer is a design or creative decision — output format, tone, structure, naming, which data source, how a step should work — do not ask an open question and do not offer only your recommendation. Present **3–5 distinct, numbered, concrete options** with your pick as option 1 and one line on why, then wait. The user reacts instead of generating, and you don't get a vague answer to chase. For factual questions only the user can answer (their real folder path, their actual deadline), rule 3 applies instead — one question, one recommendation.

---

## Interview Structure

### Step 1: The Big Picture (2–4 questions)

Start by understanding what the user is trying to accomplish and why. Don't accept vague answers. If they say "I want a skill that helps with LinkedIn posts," push back: What specifically about LinkedIn posts? What's the input? What does success look like? Who is this for?

**Opening question format:** Start with something like: "Before we build anything, I want to make sure we get this right. Let me interview you on this so we don't miss anything. First: [specific question about the goal]."

Key things to establish early:

- What is the actual goal? (Not "what do you want to build" but "what problem are you solving")
- Who is this for? (Just the user? A team? Clients?)
- What does the input look like? (Where does data come from? What format?)
- What does the output look like? (What gets produced? Where does it go?)

### Step 2: The Process Deep-Dive (5–15 questions)

This is where you get relentless. Walk through the process step by step, and at each step ask:

- "What exactly happens here?"
- "What decisions need to be made at this point?"
- "What could go wrong here?"
- "What does the user need to provide vs. what should be automatic?"
- "Show me an example of what this looks like in practice"

**The Relentless Pattern:** For every answer the user gives, ask yourself: "Is this specific enough that I could hand it to a stranger and they'd know exactly what to do?" If not, push deeper.

Examples of pushing deeper:

- User: "Then it analyzes the content." → You: "Analyzes it how? What are you looking for specifically? Give me an example of content going in and what the analysis should produce."
- User: "It should write in my tone of voice." → You: "Describe your tone of voice in concrete terms. Show me a paragraph that IS your voice and one that ISN'T. What are the specific patterns?"
- User: "It formats the output nicely." → You: "Define 'nicely'. What format? What sections? What's required vs optional? Show me an ideal output."

**Decision Tree Navigation:** When you hit a branch point (e.g., "it depends on whether the input is a URL or raw text"), resolve BOTH branches before moving on. Don't leave any path unexplored.

### Step 3: Edge Cases and Failure Modes (3–5 questions)

Once the happy path is clear, probe the edges:

- "What happens when the input is incomplete or malformed?"
- "What if the user changes their mind halfway through?"
- "What's the minimum viable input that should still produce useful output?"
- "Are there cases where this should refuse to proceed? What are they?"
- "What happens when [specific external dependency] is unavailable?"

### Step 4: Confirmation and Gaps (2–3 questions)

Summarize the entire process back to the user as you understand it. Use a structured format:

```
Here's what I've captured so far:

GOAL: [one sentence]
INPUT: [what goes in]
PROCESS:
  1. [step with specifics]
  2. [step with specifics]
  ...
OUTPUT: [what comes out]
EDGE CASES: [how failures are handled]
```

Then ask: "What did I get wrong? What's missing?" This almost always surfaces 1–2 more things they forgot to mention.

**Do not act on the plan until the user confirms you've reached shared understanding.** No building, no file edits, no execution mid-interview.

---

## Handoff to Phase 1b (Brainstorm)

Once the user confirms the summary is accurate, hand off to the brainstorm phase in `new-skill.md` → Phase 1. The brainstorm will now be grounded in a concrete plan rather than exploring open-ended possibilities.

The interview output (GOAL / INPUT / PROCESS / OUTPUT / EDGE CASES) becomes the starting point for brainstorming improvements, edge cases, and simpler approaches.

---

## What Makes This Different from Just Asking Questions

Regular planning conversations drift. The user says something vague, the assistant accepts it, and both move on. This interview is different because:

- It follows a structured progression (big picture → process → edges → confirmation)
- It refuses to move forward with ambiguity
- It always provides a recommendation, and 3–5 concrete options at every design choice (the user reacts instead of generating from scratch)
- It produces a concrete artifact (the GOAL/INPUT/PROCESS/OUTPUT/EDGE CASES summary)
- It tracks what's been resolved and what hasn't
