# Jira-style backlog

[Jira backlog](https://sigmalabs-team-mf7diwd5.atlassian.net/jira/software/projects/KAN/boards/1?filter=&groupBy=none&atlOrigin=eyJpIjoiMGVkNjAyYjdlZjBkNGM5NDkyOGQ5MGVmNmQ0MDdiMGMiLCJwIjoiaiJ9)

## Epics

- Access and Verification
- Account Visibility
- Promise-to-pay Journey
- Routing and Exception handling
- Reporting and Audit trail

## Story fields

- Story ID
- Epic
- Title
- User story statement
- Business value
- Acceptance criteria
- Dependencies
- Notes or assumptions

## Prioritisation

### High
- 2FA Authentication
- Plain-English summary dashboard
- Payment option
- Direct card and open banking payment
- Promise-to-pay rule validation
- Mandatory partial deposit
- Automated account hold flag to legacy database
- Automated audit logging
- Account reference number forgotten

### Medium
- Unified "Speak to Specialist" callback form
- Identity verification fails
- Broken promise trigger exception handling
- Supervisor exception and adoption dashboard
- Customer abandoning self-service portal

### Low
- Automated scheduled SMS/Email reminders
- Confirmation receipt generation

### Connection to ROI model and future-state workflow
High priority stories focus on the main self-service path such as 2FA authentication and simple plain-English account balances to direct card payments and promise-to-pay rule validation. This is high as getting the main flow working right away means customers can resolve their debt instantly.Moreover, allowing automated audit logging under this immediately removes the 3.31 hours of manual spreadsheet admin per agent every day, giving our team back crucial time on day one.

Medium priority stories focus on exception handling and supervisor adoption dashboards. This involves the unified "Speak to Specialist" callback form and broken promise trigger exception handling. These features ensures that if a customer gets stuck or misses a payment date, their account is instantly passed to an agent with their full history attached. It also gives supervisors the live dashboard they need to shift team targets away from raw call volume to meaningful customer outcomes.

Low priority stories focus on automated reminders and confirmation receipts. They are great features that improve the customer experience and keep payment plans on track over time, but they are not essential to the main self-service flow. They can be implemented later once the high and medium priority stories are complete.