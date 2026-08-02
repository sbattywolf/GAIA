# Glossary

## Status markers

- **Established:** canonical working vocabulary.
- **Partial:** in active architectural discussion.
- **Proposed:** candidate requiring validation.

## Established terms

- **GAIA:** local-first Personal AI Operating System with specialised collaborators and explicit capabilities.
- **Identity:** durable definition of what GAIA is.
- **Core:** minimal internal coordination layer preserving coherence and essential contracts; exact scope is open.
- **Collaborator:** bounded digital role with a specific responsibility.
- **Domain:** coherent area of responsibility.
- **Capability:** explicit contract for action or access with constraints.
- **Resource:** anything GAIA may reference or affect.
- **Shared Context:** scoped context shared across parts of GAIA.
- **Local-First:** preference for local ownership, control, and execution, with remote services explicit and replaceable.
- **Human Control:** important decisions and sensitive actions remain visible, governable, and correctable.

## Partially established terms

- **Memory:** structured retention, retrieval, correction, and forgetting over time.
- **Planner:** coordination function combining intents, collaborators, capabilities, resources, and policy.
- **Policy:** rule or constraint governing allowed behaviour.
- **Approval:** explicit authorisation before an action.
- **Audit:** record of important decisions, actions, approvals, denials, changes, and interactions.
- **Boundary:** separation between responsibilities or trust zones.
- **Adapter:** component connecting GAIA to an external system while limiting coupling.
- **Tool:** callable operation or external capability.
- **Workflow:** sequence or graph coordinating work and state.
- **Registry:** discoverable catalogue of components.
- **Runtime:** environment executing inference, tools, workflows, or computation.
- **Model:** AI model used for reasoning or other AI functions.

## Proposed/external terms

- **Event:** recorded occurrence such as message, tool call, state change, approval, or failure.
- **Run:** bounded execution from trigger to result, action, or failure.
- **Agent:** external ecosystem term; prefer Collaborator for GAIA-native roles.
- **MCP:** Model Context Protocol for connecting AI applications to tools and data.
- **RAG:** retrieval-augmented generation.
- **LLM:** large language model.
- **Vector Store:** embedding and similarity-search storage.
- **Connector:** integration to an external source or service.
- **Plugin:** packaged extension to a host system.
- **Event Bus:** publish/consume mechanism; not currently required.
- **Knowledge Base:** curated or indexed information for retrieval and grounding.
