# Smart-Recovery Portal Prototype

Single-file Flask click-through prototype of the Smart-Recovery self-service debt portal for Legacy Trust Bank. It follows the flow mapped in [`../smart_recovery_portal.png`](../smart_recovery_portal.png), simplified for a rapid prototype, and covers both the main happy path and the exception/routing paths.

This is a **UI/flow prototype only**: all customer data is fake, there is no real database, payment gateway, or SMS/OTP provider. Story IDs referenced below are the real backlog IDs from [`../Jira.csv`](../Jira.csv).

## Run it

```bash
cd submissions/prototype
pip install flask
python3 app.py
```

Open `http://127.0.0.1:5001`. Demo values that trigger the success paths:
- Account reference: any non-empty value (e.g. `ACC-2024-58213`)
- Date of birth: `1985-04-12`, OTP: `123456`
- Payment card: anything except `0000000000000000` (which simulates a decline)
- Promise-to-pay date: any date within the next 30 days

## Screens

### 1. Landing (`/`)
- **User story:** KAN-30 — Account reference number forgotten
- **Key data shown:** account reference input field
- **Validation/business rule:** reference field cannot be empty; a "forgotten reference" link is always available
- **Next step:** submits to Identity Verification

### 2. Forgotten reference (`/forgot-reference`)
- **User story:** KAN-30 — Account reference number forgotten
- **Key data shown:** static help text with the expected reference format
- **Validation/business rule:** none — informational only
- **Next step:** back to Landing

### 3. Identity verification (`/verify`)
- **User story:** KAN-10 — 2FA Authentication
- **Key data shown:** date of birth and one-time passcode inputs
- **Validation/business rule:** account details stay hidden until both DOB and OTP match; blocks access on failure (per US-01 "block account details until verification succeeds")
- **Next step:** success → Account Summary; failure → generic Exception screen (reason: identity verification failed)

### 4. Account summary (`/summary`)
- **User story:** KAN-17 — Plain-English Account Summary Dashboard
- **Key data shown:** total balance, past-due amount, fees applied, account reference, plain-English status, last payment received (amount and date)
- **Validation/business rule:** only reachable once `verified` is set in session; unverified visitors are redirected to Landing
- **Next step:** Choose Payment Option

### 5. Choose payment option (`/payment-options`)
- **User story:** KAN-18 — Payment option
- **Key data shown:** three routing choices (pay now, promise to pay, speak to specialist), plus a link back to Account Summary
- **Validation/business rule:** requires prior verification
- **Next step:** branches to Pay Now, Promise to Pay, Speak to a Specialist, or back to Account Summary

### 6. Pay now (`/pay`)
- **User story:** KAN-20 — Direct card and open banking payment
- **Key data shown:** current balance, amount field pre-filled with balance, card number field
- **Validation/business rule:** amount must be greater than zero and not exceed the balance; the demo card `0000000000000000` simulates a declined payment
- **Next step:** success → Payment Confirmation; failure → generic Exception screen (reason: payment failed)

### 7. Payment confirmation (`/payment-confirmation`)
- **User story:** KAN-21 — Confirmation receipt generation
- **Key data shown:** amount paid, remaining balance, confirmation/receipt message
- **Validation/business rule:** only reachable after a successful payment in session
- **Next step:** back to Account Summary

### 8. Promise to pay (`/promise-to-pay`)
- **User story:** KAN-22 (rule validation) and KAN-23 (mandatory partial deposit)
- **Key data shown:** calculated 5% deposit, first-payment date picker, repayment frequency, dates shown in UK `dd/mm/yyyy` format
- **Validation/business rule:** first payment date must fall within the next 30 days (mirrors the "maximum 30-day promise" guardrail); deposit is mandatory and taken immediately; an inline link offers Speak to a Specialist for customers wanting a longer arrangement
- **Next step:** success → Promise Confirmed; invalid date → generic Exception screen (reason: promise-to-pay invalid)

### 9. Promise confirmed (`/ptp-confirmation`)
- **User story:** KAN-24 — Automated account hold flag to legacy database
- **Key data shown:** deposit taken, first payment date, remaining balance, account-hold confirmation
- **Validation/business rule:** only reachable after a valid promise is recorded in session; hold flag prevents duplicate agent contact while the plan is active
- **Next step:** back to Account Summary

### 10. Speak to a specialist (`/specialist`)
- **User story:** KAN-27 — Unified "Speak to Specialist" callback form
- **Key data shown:** contact number, preferred callback window
- **Validation/business rule:** single unified callback queue regardless of which screen the customer came from
- **Next step:** Routed to Agent

### 11. Routed to agent (`/routed-to-agent`)
- **User story:** KAN-15 — Routing and exception handling (epic)
- **Key data shown:** confirmation that the case and account context have been handed to a specialist
- **Validation/business rule:** dead-end confirmation screen — preserves context for agent handoff instead of leaving the customer stuck
- **Next step:** return to Landing (end of journey)

### 12. Exception / retry (`/exception`)
- **User story:** KAN-15 — Routing and exception handling (epic)
- **Key data shown:** contextual failure message (identity verification, payment, or promise-to-pay)
- **Validation/business rule:** generic handler for every simulated failure trigger described above; always offers a retry link back to the originating screen
- **Next step:** retry the failed step, or escalate to Speak to a Specialist

## Simplifications vs. the source diagram

- Exception handling for verification, payment, and promise-to-pay failures is consolidated into one generic `/exception` screen instead of three separate error pages, since the business rule (retry or escalate) is identical in each case.
- No persistence beyond the browser session; refreshing after closing the app resets the demo.
