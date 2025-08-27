# PotatoBot


# MCP-based Engineering Agent: Architecture & MVP Plan

## Architecture

### Core Agent

* **Orchestrator Agent**: Central brain that routes requests between MCP tools.
* **Context Manager**: Stores project context (repos, APIs, Jira projects, Confluence docs, Qase test suites).
* **Policy & Guardrails**: Approval workflows for PR creation, reviewer assignment, Jira automation.

### MCP Servers

1. **GitHub MCP**

   * Create branches, commits, and PRs.
   * Ensure each PR is **<500 LOC** and represents a **self‑contained deliverable**.
   * Assign the **correct team reviewers** automatically based on repo ownership rules.
   * Propose initial code skeletons and link to API/test changes.
   * PR & Commit Rules
      - Conventional Commit enforced:
      - feat:, fix:, chore:, refactor:, test:, etc.
      - PR titles must match the same format.
      - PR size cap: ≤ 500 lines of code.
      - Agent splits larger scaffolds into multiple PRs.
      - Each PR is a self-contained deliverable (compiles, tests run).
      - CI hook: validate commit/PR format + line count.

2. **Jira MCP**

   * Create/update tickets.
   * Link to Confluence and GitHub PRs.
   * Maintain traceability from architecture → API → code/test.

3. **Confluence MCP**

   * Retrieve related architecture/design docs.
   * Propose updates and attach Jira references.

4. **Internal API MCP** *(protobuf/gRPC aware)*

   * Parse `.proto` files from the central repo [`AlphaFounders/protos`](https://github.com/AlphaFounders/protos).
   * Access **private repos** via **SSH keys**.
   * Propose **API changes first** (before code skeletons).
   * Validate backward compatibility.
   * Use **Buf** to generate idiomatic Go code from `.proto` files.
   * Generate contract tests.
   * MCP-GitHub must support multi-repo workflows (PRs across both protos and service repos).
   * Workflow:
      - Propose/edit .proto in protos repo.
      - Use Buf to generate Go stubs.
      - Commit generated code in the service repo (internal/api/, pkg/api/).
      - Open linked PRs (one in protos, one in service repo).
      - Both PRs reference the same Jira ticket.

5. **Qase MCP**

   * Fetch test cases.
   * Link unit tests to Qase IDs.
   * Ensure coverage traceability.

6. **Analytics MCP**

   * Pull usage metrics to guide design decisions.
   * Correlate bugs/incidents to high-traffic features.

7. **Flagsmith MCP** *(optional)*

   * Interact with **Flagsmith API** for feature flag creation and rollout.
   * Attach flag references to Jira tickets and PR descriptions.

## Agent Flow (Stepwise)

1. **Architecture Proposal**

   * Agent drafts architecture (Confluence update + Jira epic).
   * Reviewer (tech lead/architect) approves.

2. **API Changes (protobuf-first)**

   * Internal API MCP checks current `.proto`.
   * Suggests changes/new services.
   * Opens PR with updated `.proto` files.
   * Contract tests proposed automatically.

3. **API Contract Testing**

   * Auto-generate tests to validate gRPC contracts.
   * Add these in a `contract_tests` package in Go.
   * CI enforces compatibility with existing clients.

4. **Unit Test & Code Skeleton Generation**

   * Generate **idiomatic Go, functional style**, with testability as first-class.
   * Reference Qase test cases directly in comments or metadata.
   * PR created with:

     * `api/` (protobuf + generated stubs)
     * `internal/` (domain logic)
     * `pkg/` (reusable libraries)
     * `tests/` (unit + contract tests)
   * Assign reviewers automatically.
   * Ensure each PR follows **conventional commit**, is **<500 LOC**, and is self-contained.

5. **Iteration & Review**

   * Developers refine.
   * Agent continues to propose updates/test coverage.

## MVP Plan (Refined)

* **Milestone 1**: Base agent with GitHub + Jira MCP.
* **Milestone 2**: Add Internal API MCP for `.proto` parsing, Buf codegen, and API-first workflow.
* **Milestone 3**: Add Qase MCP and link unit tests to test cases.
* **Milestone 4**: Implement Confluence + Analytics MCP integrations.
* **Milestone 5**: Reviewer assignment + policy guardrails + CI/CD contract testing.
* **Milestone 6**: Optional Flagsmith MCP for feature flag integration.

## Risks & Mitigations

* **Proto parsing complexity** → Use Buf or protoc plugins.
* **Test traceability** → Qase IDs embedded in test metadata.
* **Reviewer assignment accuracy** → Map repo paths → GitHub teams config.
* **CI noise** → Dry-run mode before automated PRs.
* **PR bloat** → Enforce max 500 LOC per PR; split into multiple PRs if larger.
