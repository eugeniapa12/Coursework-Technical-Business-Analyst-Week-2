# Phase 1 Scope & Prioritisation

## ADKAR assessment
A change model covering Awareness, Desire, Knowledge, Ability and Reinforcement for 3 stakeholder groups: Collection Agents, Customer, Team Leaders and Supervisors. 

### Collection Agents

| ADKAR element | Rating |  Why |
|---|---|---|
| Awareness | High | Agents experience daily friction from manual reconciliation and fragmented spreadsheets. |
| Desire | Medium-Low | Worried that the self-service won't reduce their workload if customers mismanage payment plans or set up unrealistic promises. |
| Knowledge | Medium | Currently rely on local spreadsheet workarounds and legacy databases. They don't have any training on the new automated systems.|
| Ability | Medium | Can handle complex cases, but used to manual spreadsheet checks. Need clear training and guidance. |
| Reinforcement | Low | If the change fails/break, agents will revert to their old habits of manual reconciliation. |

### Customer

| ADKAR element | Rating |  Why |
|---|---|---|
| Awareness | Medium-Low | Customers know they have overdue debt, but are unaware of the 24/7 self-service portal to view balances, make card payments or set up payment promises. |
| Desire | High | Prefer to resolve debt privately on their own schedule without waiting on hold or negotiation with agents. |
| Knowledge | Low | No experience with the new system, require simple UI explanations showing clear balances (OPP-01) and flexible schedule choices (OPP-03). |
| Ability | Medium | If the system doesn't fail, ability is somewhat high, depending on the user's digital literacy. If system fails, rating will drop. |
| Reinforcement | High | Instant email/SMS confirmation for payments and automate reminders/follow-ups for upcoming promise dates to reinforce trust and keep customers on track without agent calls. |

### Team Leaders and Supervisors

| ADKAR element | Rating |  Why |
|---|---|---|
| Awareness | High | They see duplicated outreach, broken promises that aren't being detected and lack of visibility across spreadsheets every day. |
| Desire | Medium | Want operational improvement, but worried that the customers will set up their own payment plans that will lead to broken promises that land back onto the team. |
| Knowledge | Low | Require clear visibility of the portal's built-in guardrails and how self-service payment arrangements flow back into the core databases without causing errors. |
| Ability | Medium | Can manage team capacity but need more real time reporting tools to monitor the system so that it is working correctly and can detect any errors/broken automated promises. |
| Reinforcement | Low | If supervisors are judged based on the volume of calls the team handles, then they will want more manual phone calls, ignoring the portal entirely.  |

### Change risks & Mitigation Actions

| Change risks | Mitigation actions |
|---|---|
| Unrealistic promise-to-pay setups resulting in many broken promises that flood back to agents | Enforce strict system guardrails, mentioned in the portal UI. (E.g. maximum 30-day promise, partial deposit, limit on automated promise.) If a customer requests a plan outside these limits, the portal will transition to a request special terms callback form. |
| Duplicate agent contact during active promises where agents unknowingly call customers who have already set up a self-service promise as status updates aren't visible in real time | Once a PTP is set up, the system instantly flags their account to stop agents from calling them by accident as the account is removed from the calling list.  |
| Customers with lower digital literacy/experiencing financial vulnerability get confused by the portal interface and may give up during the setup, resulting in calling the agents. | Make the portal UI simple, with clear explanations on their balance and step by step progress bars. If customer is still struggling, UI has a "call us" option or a callback request so they don't abandon the setup entirely. |
| Supervisor reinforcement risk - they may ignore the enw system as they are judged on reward call KPI. | Fix team targets before going live. Their KPI should be based on portal success rates, fast handling of flagged cases or long term payment completion instead of call volumes. |


## In scope - Phase 1

- Identity verification: 
    - Two-factor authentication (e.g. email and mobile phone verification, OTP verification) to verify customer identity before disclosing financial balances.
- Account summary and balance breakdown:
    - Plain english summary of account balance, overdue amounts, active arrangement status and interest/fees. High ROI percentage.
- Direct payment processing:
    - Integrated credit/debit card and bank transfer payment processing with instant confirmation and receipts.
- Promise-to-pay capture:
    - Self-service promise-to-pay setup with clear terms, maximum limits and automated reminders. This includes mandatory partial deposit to ensure commitment and reduce broken promises.
- Eligible payment-plan selection:
    - Customers can select from predefined payment plans based on their financial situation and preferences.
- Portal outcome reporting:
    - Customers receive real-time updates on the status of their promises and payments. This is via email/SMS notifications and a portal dashboard that shows upcoming payment dates, amounts due, and any changes to their plan.
- Management and operational reporting:
    - Supervisors and team leaders can access dashboards and reports to monitor portal usage, promise-to-pay success rates, and overall operational efficiency. This includes tracking the number of self-service setups, broken promises, and customer feedback. This allows for full operational visibility.

## Out of scope - Phase 1

- Automated case routing:
    - Requires complex ruling with human judgement and the database lacks vulnerability markers. Automating case routing without these flags risks pushing vulnerable customers into automated contact loops which in turn violates FCA rules.
- Bespoke repayment negotiation:
    - Customers cannot negotiate over custom settlement terms or request special arrangements. This requires human judgement and is out of scope for Phase 1.
- Complex hardship assessment:
    - Customers cannot request hardship assessments or financial vulnerability checks. This requires human judgement and is out of scope for Phase 1. The portal will give them a "speak to specialist" option to request a callback for these cases.
- Advanced personalisation:
    - Customers cannot personalise their portal experience beyond the basic account summary and payment plan selection as this requires smart features such as AI-driven payment recommendations and predictive analytics which are out of scope for Phase 1. We need a solid baseline data on how customers actually use the basic portal.

## Deliverable planning

| Deliverable | Deadline | Time required / Potential blockers | Justification |
|---|---|---|---|
| To-Be workflow | 18/08/26 | 5 hours / Incorrect/optimistic ROI ranking | Shows the Smart-Recovery journey and its exception paths |
| Prioritised Jira backlog | 19/08/26 | 8 hours | Translating the To-Be process map into specific, buildable user stories with acceptance criteria. Allows the abstract workflow to become concrete deliverables for the development team. |
| AI-built prototype | 20/08/26 | 8 hours / Data availability and model accuracy | Developing a prototype using GitHub Copilot to assist in the Smart-Recovery process. Potential blockers include the availability of clean data and ensuring the model's recommendations are accurate and compliant. |
| State of the Product executive briefing slide deck | 21/08/26 | 5 hours | Using the pyramid principle to structure arguments, clearly explain why Legacy Trust should act now, what Phase 1 delivers and why the proposal is credible. |

## Dependencies and constraints

Note the most important delivery and operating constraints.

Examples:
- legacy system data availability
- compliance approval for messages and audit trail
- agent workflow alignment for routed cases

## Why this scope is credible

Write 1-2 paragraphs linking the chosen scope to:
- Week 1 top-ranked opportunities
- measurable value
- delivery feasibility
- change and adoption risk
