"""Smart-Recovery self-service portal - single-file Flask click-through prototype for Legacy Trust Bank.

Rapid prototype only: no real database, payment gateway, or SMS/OTP provider.
All customer data below is fake and all "validation" is simulated with hardcoded values
so the main path and the exception paths (see submissions/smart_recovery_portal.png) can both be demoed.

Run with: python3 app.py   (serves http://127.0.0.1:5001)
"""
from datetime import date, timedelta

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
# prototype only, never reuse in a real deploy
app.secret_key = "smart-recovery-prototype-not-for-production"

# ---------------------------------------------------------------------------
# Fake customer data and hardcoded "business rules" used to trigger success/fail paths
# ---------------------------------------------------------------------------
CUSTOMER = {
    "name": "Alex Morgan",
    "account_ref": "ACC-2024-58213",
    "balance": 1240.50,
    "past_due": 310.00,
    "fees": 45.00,
    "status": "Overdue - action required",
    "last_payment_date": "2026-07-15",
    "last_payment_amount": 75.00,
}
VALID_DOB = "1985-04-12"  # matches the fake customer above, used for the 2FA demo
VALID_OTP = "123456"  # simulated OTP, a real build would text/email a one-time code
DEPOSIT_RATE = 0.05  # mandatory partial deposit rule (KAN-23), 5% for now
MAX_PROMISE_DAYS = 30  # promise-to-pay date cap (KAN-22)
# UK format, used everywhere a date is shown to the customer
DISPLAY_DATE_FORMAT = "%d/%m/%Y"


def format_date(iso_date_string):
    """Render an ISO (yyyy-mm-dd) date string in the UK format used across the portal."""
    return date.fromisoformat(iso_date_string).strftime(DISPLAY_DATE_FORMAT)


# ---------------------------------------------------------------------------
# Shared page shell (kept in one file per the "single-file" prototype brief)
# ---------------------------------------------------------------------------
LAYOUT_HEAD = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Smart-Recovery | Legacy Trust Bank</title>
<style>
  :root {
    --navy: #0b3d5c;
    --navy-dark: #082c43;
    --accent: #1f8a70;
    --error: #b23a2e;
    --bg: #f4f6f8;
    --card: #ffffff;
    --text: #1c2b36;
    --muted: #5b6b78;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
  }
  header {
    background: var(--navy);
    color: #fff;
    padding: 18px 24px;
  }
  header .brand { font-size: 1.15rem; font-weight: 700; letter-spacing: 0.3px; }
  header .sub { font-size: 0.85rem; color: #cfe0ec; margin-top: 2px; }
  .progress {
    display: flex;
    gap: 6px;
    max-width: 720px;
    margin: 18px auto 0;
    padding: 0 24px;
  }
  .progress span {
    flex: 1;
    text-align: center;
    font-size: 0.72rem;
    padding: 6px 4px;
    border-radius: 4px;
    background: #e3e9ed;
    color: var(--muted);
  }
  .progress span.active { background: var(--accent); color: #fff; font-weight: 600; }
  main {
    max-width: 640px;
    margin: 24px auto 60px;
    padding: 0 24px;
  }
  .card {
    background: var(--card);
    border-radius: 10px;
    padding: 28px 30px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  h1 { font-size: 1.35rem; margin: 0 0 6px; color: var(--navy-dark); }
  .story-tag {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--navy);
    background: #dce9f0;
    border-radius: 20px;
    padding: 3px 10px;
    margin-bottom: 14px;
  }
  p.lead { color: var(--muted); margin-top: 0; }
  label { display: block; font-size: 0.85rem; font-weight: 600; margin: 14px 0 6px; }
  input, select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #c7d1d8;
    border-radius: 6px;
    font-size: 0.95rem;
  }
  .row { display: flex; gap: 12px; }
  .row > div { flex: 1; }
  .btn {
    display: inline-block;
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 11px 20px;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    margin-top: 18px;
  }
  .btn.secondary { background: var(--navy); }
  .btn.ghost { background: transparent; color: var(--navy); border: 1px solid var(--navy); }
  .btn-row { display: flex; gap: 12px; flex-wrap: wrap; }
  .summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 20px; margin: 18px 0; }
  .summary-grid .label { font-size: 0.78rem; color: var(--muted); }
  .summary-grid .value { font-size: 1.05rem; font-weight: 700; color: var(--navy-dark); }
  .banner-error {
    background: #fbeae7;
    border: 1px solid var(--error);
    color: var(--error);
    padding: 12px 14px;
    border-radius: 6px;
    font-size: 0.9rem;
    margin-bottom: 16px;
  }
  .banner-success {
    background: #e6f3ee;
    border: 1px solid var(--accent);
    color: #12543f;
    padding: 12px 14px;
    border-radius: 6px;
    font-size: 0.9rem;
    margin-bottom: 16px;
  }
  .hint { font-size: 0.8rem; color: var(--muted); margin-top: 8px; }
  footer.note {
    max-width: 640px;
    margin: 0 auto 40px;
    padding: 0 24px;
    font-size: 0.75rem;
    color: var(--muted);
  }
</style>
</head>
<body>
<header>
  <div class="brand">Legacy Trust Bank &mdash; Smart-Recovery</div>
  <div class="sub">Self-service debt resolution portal (prototype)</div>
</header>
"""

LAYOUT_FOOT = """
<footer class="note">Prototype build &middot; all customer data is fictional &middot; see README.md for screen-by-screen notes.</footer>
</body>
</html>
"""

STEPS = ["Verify", "Account summary", "Choose option", "Complete"]


def progress_html(current_index):
    """current_index of -1 hides the bar (used on exception/off-path screens)."""
    if current_index < 0:
        return ""
    spans = "".join(
        '<span class="{cls}">{label}</span>'.format(
            cls="active" if i == current_index else "", label=label
        )
        for i, label in enumerate(STEPS)
    )
    return '<div class="progress">{}</div>'.format(spans)


def render_page(title, story_id, body, step=-1):
    template = LAYOUT_HEAD + \
        progress_html(step) + "<main><div class=\"card\">" + \
        body + "</div></main>" + LAYOUT_FOOT
    return render_template_string(template, title=title, story_id=story_id)


# ---------------------------------------------------------------------------
# 1. Landing page - KAN-30 (account reference forgotten flow starts here)
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def landing():
    error = None
    if request.method == "POST":
        account_ref = request.form.get("account_ref", "").strip()
        if not account_ref:
            error = "Enter your account reference to continue."
        else:
            session.clear()
            session["account_ref"] = account_ref
            return redirect(url_for("verify"))

    body = """
    <span class="story-tag">Landing</span>
    <h1>Welcome back</h1>
    <p class="lead">Enter your account reference to start resolving your account.</p>
    {error_banner}
    <form method="post">
      <label for="account_ref">Account reference</label>
      <input id="account_ref" name="account_ref" placeholder="ACC-2024-58213" autofocus>
      <div class="btn-row">
        <button class="btn" type="submit">Continue</button>
        <a class="btn ghost" href="{forgot_url}">Forgotten your reference?</a>
      </div>
    </form>
    """.format(
        error_banner='<div class="banner-error">{}</div>'.format(
            error) if error else "",
        forgot_url=url_for("forgot_reference"),
    )
    return render_page("Landing", "KAN-30", body)


@app.route("/forgot-reference")
def forgot_reference():
    body = """
    <span class="story-tag">Forgotten reference &middot; KAN-30</span>
    <h1>Find your account reference</h1>
    <p class="lead">Your account reference is on any letter or email we've sent you, formatted like <strong>ACC-2024-58213</strong>.</p>
    <a class="btn" href="{}">Back to sign in</a>
    """.format(url_for("landing"))
    return render_page("Forgot reference", "KAN-30", body)


# ---------------------------------------------------------------------------
# 2. Identity verification (2FA) - KAN-10, fail path -> KAN-19
# ---------------------------------------------------------------------------
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "account_ref" not in session:
        return redirect(url_for("landing"))

    if request.method == "POST":
        dob = request.form.get("dob", "").strip()
        otp = request.form.get("otp", "").strip()
        if dob == VALID_DOB and otp == VALID_OTP:
            session["verified"] = True
            return redirect(url_for("summary"))
        return redirect(
            url_for("exception", reason="verification_failed", retry_to="verify")
        )

    body = """
    <span class="story-tag">Identity verification &middot; KAN-10</span>
    <h1>Verify it's you</h1>
    <p class="lead">Account details stay hidden until verification succeeds.</p>
    <form method="post">
      <label for="dob">Date of birth</label>
      <input id="dob" name="dob" type="date">
      <label for="otp">One-time passcode</label>
      <input id="otp" name="otp" placeholder="6-digit code" maxlength="6">
      <div class="hint">Prototype demo values: DOB 1985-04-12, OTP 123456</div>
      <button class="btn" type="submit">Verify</button>
    </form>
    """
    return render_page("Verify identity", "KAN-10", body, step=0)


# ---------------------------------------------------------------------------
# 3. Account summary - KAN-17
# ---------------------------------------------------------------------------
@app.route("/summary")
def summary():
    if not session.get("verified"):
        return redirect(url_for("landing"))

    balance = session.get("balance", CUSTOMER["balance"])
    body = """
    <span class="story-tag">Account summary &middot; KAN-17</span>
    <h1>Hi {name}, here's your account</h1>
    <p class="lead">Status: <strong>{status}</strong></p>
    <div class="summary-grid">
      <div><div class="label">Total balance</div><div class="value">&pound;{balance:.2f}</div></div>
      <div><div class="label">Past due</div><div class="value">&pound;{past_due:.2f}</div></div>
      <div><div class="label">Fees applied</div><div class="value">&pound;{fees:.2f}</div></div>
      <div><div class="label">Account reference</div><div class="value">{account_ref}</div></div>
      <div><div class="label">Last payment received</div><div class="value">&pound;{last_payment_amount:.2f} on {last_payment_date}</div></div>
    </div>
    <a class="btn" href="{next_url}">Continue</a>
    """.format(
        name=CUSTOMER["name"],
        status=CUSTOMER["status"],
        balance=balance,
        past_due=CUSTOMER["past_due"],
        fees=CUSTOMER["fees"],
        account_ref=CUSTOMER["account_ref"],
        last_payment_amount=CUSTOMER["last_payment_amount"],
        last_payment_date=format_date(CUSTOMER["last_payment_date"]),
        next_url=url_for("payment_options"),
    )
    return render_page("Account summary", "KAN-17", body, step=1)


# ---------------------------------------------------------------------------
# 4. Choose payment option - KAN-18
# ---------------------------------------------------------------------------
@app.route("/payment-options")
def payment_options():
    if not session.get("verified"):
        return redirect(url_for("landing"))

    body = """
    <span class="story-tag">Choose an option &middot; KAN-18</span>
    <h1>How would you like to resolve this?</h1>
    <div class="btn-row">
      <a class="btn" href="{pay_url}">Pay now</a>
      <a class="btn secondary" href="{ptp_url}">Set up a promise to pay</a>
      <a class="btn ghost" href="{spec_url}">Speak to a specialist</a>
    </div>
    <p class="hint"><a href="{summary_url}">&larr; Back to account summary</a> to double-check your balance first</p>
    """.format(
        pay_url=url_for("pay"),
        ptp_url=url_for("promise_to_pay"),
        spec_url=url_for("specialist"),
        summary_url=url_for("summary"),
    )
    return render_page("Choose payment option", "KAN-18", body, step=2)


# ---------------------------------------------------------------------------
# 5. Pay now - KAN-20, failure -> generic exception
# ---------------------------------------------------------------------------
@app.route("/pay", methods=["GET", "POST"])
def pay():
    if not session.get("verified"):
        return redirect(url_for("landing"))

    balance = session.get("balance", CUSTOMER["balance"])
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", "0"))
        except ValueError:
            amount = 0
        card_number = request.form.get("card_number", "").strip()
        # simulated failure triggers: zero/over-balance amount, or the demo "declined" card
        if amount <= 0 or amount > balance or card_number == "0000000000000000":
            return redirect(url_for("exception", reason="payment_failed", retry_to="pay"))
        session["balance"] = round(balance - amount, 2)
        session["last_payment"] = amount
        return redirect(url_for("payment_confirmation"))

    body = """
    <span class="story-tag">Pay now &middot; KAN-20</span>
    <h1>Make a payment</h1>
    <p class="lead">Current balance: &pound;{balance:.2f}</p>
    <form method="post">
      <label for="amount">Amount to pay (&pound;)</label>
      <input id="amount" name="amount" type="number" step="0.01" value="{balance:.2f}">
      <label for="card_number">Card number</label>
      <input id="card_number" name="card_number" placeholder="16-digit card number">
      <div class="hint">Prototype demo: card number 0000000000000000 simulates a declined payment</div>
      <button class="btn" type="submit">Pay</button>
    </form>
    """.format(balance=balance)
    return render_page("Pay now", "KAN-20", body, step=3)


@app.route("/payment-confirmation")
def payment_confirmation():
    if not session.get("verified") or "last_payment" not in session:
        return redirect(url_for("landing"))

    body = """
    <span class="story-tag">Payment confirmation &middot; KAN-21</span>
    <h1>Payment received</h1>
    <div class="banner-success">&pound;{amount:.2f} was applied to your account. A confirmation receipt has been emailed to you.</div>
    <div class="summary-grid">
      <div><div class="label">Remaining balance</div><div class="value">&pound;{balance:.2f}</div></div>
    </div>
    <a class="btn" href="{summary_url}">Back to account summary</a>
    """.format(
        amount=session["last_payment"],
        balance=session.get("balance", CUSTOMER["balance"]),
        summary_url=url_for("summary"),
    )
    return render_page("Payment confirmation", "KAN-21", body, step=3)


# ---------------------------------------------------------------------------
# 6. Promise-to-pay - KAN-22 / KAN-23, failure -> generic exception
# ---------------------------------------------------------------------------
@app.route("/promise-to-pay", methods=["GET", "POST"])
def promise_to_pay():
    if not session.get("verified"):
        return redirect(url_for("landing"))

    balance = session.get("balance", CUSTOMER["balance"])
    deposit = round(balance * DEPOSIT_RATE, 2)
    min_date = date.today() + timedelta(days=1)
    max_date = date.today() + timedelta(days=MAX_PROMISE_DAYS)

    if request.method == "POST":
        chosen = request.form.get("first_payment_date", "")
        try:
            chosen_date = date.fromisoformat(chosen)
        except ValueError:
            chosen_date = None
        # business rule: promise date must fall within the 30-day window (KAN-22)
        if chosen_date is None or not (min_date <= chosen_date <= max_date):
            return redirect(url_for("exception", reason="ptp_invalid", retry_to="promise_to_pay"))
        session["ptp_date"] = chosen
        session["ptp_deposit"] = deposit
        session["balance"] = round(balance - deposit, 2)
        return redirect(url_for("ptp_confirmation"))

    body = """
    <span class="story-tag">Promise to pay &middot; KAN-22 / KAN-23</span>
    <h1>Set up a promise to pay</h1>
    <p class="lead">A mandatory deposit of &pound;{deposit:.2f} (5% of balance) is required today to confirm your plan.</p>
    <form method="post">
      <label for="first_payment_date">First payment date</label>
      <input id="first_payment_date" name="first_payment_date" type="date" min="{min_date}" max="{max_date}">
      <label for="frequency">Repayment frequency</label>
      <select id="frequency" name="frequency">
        <option value="weekly">Weekly</option>
        <option value="monthly">Monthly</option>
      </select>
      <div class="hint">Promises can only be scheduled up to {max_days} days out ({max_date_display}). Need longer? <a href="{spec_url}">Speak to a specialist</a> instead.</div>
      <button class="btn" type="submit">Confirm promise &amp; pay deposit</button>
    </form>
    """.format(
        deposit=deposit,
        min_date=min_date.isoformat(),
        max_date=max_date.isoformat(),
        max_date_display=max_date.strftime(DISPLAY_DATE_FORMAT),
        max_days=MAX_PROMISE_DAYS,
        spec_url=url_for("specialist"),
    )
    return render_page("Promise to pay", "KAN-22", body, step=3)


@app.route("/ptp-confirmation")
def ptp_confirmation():
    if not session.get("verified") or "ptp_date" not in session:
        return redirect(url_for("landing"))

    body = """
    <span class="story-tag">Promise confirmed &middot; KAN-24</span>
    <h1>Your promise to pay is set up</h1>
    <div class="banner-success">Deposit of &pound;{deposit:.2f} received. Your account is now flagged on hold so agents won't call while your plan is active.</div>
    <div class="summary-grid">
      <div><div class="label">First payment date</div><div class="value">{ptp_date}</div></div>
      <div><div class="label">Remaining balance</div><div class="value">&pound;{balance:.2f}</div></div>
    </div>
    <a class="btn" href="{summary_url}">Back to account summary</a>
    """.format(
        deposit=session["ptp_deposit"],
        ptp_date=format_date(session["ptp_date"]),
        balance=session.get("balance", CUSTOMER["balance"]),
        summary_url=url_for("summary"),
    )
    return render_page("Promise confirmed", "KAN-24", body, step=3)


# ---------------------------------------------------------------------------
# 7. Speak to a specialist - KAN-27, then routed to agent
# ---------------------------------------------------------------------------
@app.route("/specialist", methods=["GET", "POST"])
def specialist():
    if request.method == "POST":
        session["callback_phone"] = request.form.get("phone", "").strip()
        session["callback_window"] = request.form.get("window", "")
        return redirect(url_for("routed_to_agent"))

    body = """
    <span class="story-tag">Speak to a specialist &middot; KAN-27</span>
    <h1>Request a callback</h1>
    <p class="lead">A specialist will call you back with your full account context already available.</p>
    <form method="post">
      <label for="phone">Contact number</label>
      <input id="phone" name="phone" placeholder="07123 456789">
      <label for="window">Preferred callback time</label>
      <select id="window" name="window">
        <option value="morning">Morning</option>
        <option value="afternoon">Afternoon</option>
        <option value="evening">Evening</option>
      </select>
      <button class="btn" type="submit">Request callback</button>
    </form>
    """
    return render_page("Speak to a specialist", "KAN-27", body)


@app.route("/routed-to-agent")
def routed_to_agent():
    body = """
    <span class="story-tag">Routed to agent &middot; KAN-15</span>
    <h1>You're all set</h1>
    <div class="banner-success">Your case has been routed to a collections specialist with your account history attached. We'll call you during your preferred window.</div>
    <a class="btn" href="{}">Return to start</a>
    """.format(url_for("landing"))
    return render_page("Routed to agent", "KAN-15", body)


# ---------------------------------------------------------------------------
# Generic exception/retry screen - covers verification, payment and PTP failures
# ---------------------------------------------------------------------------
EXCEPTION_MESSAGES = {
    "verification_failed": "We couldn't verify your identity with those details.",
    "payment_failed": "Your payment couldn't be processed.",
    "ptp_invalid": "That promise date isn't within the allowed 30-day window.",
}


@app.route("/exception")
def exception():
    reason = request.args.get("reason", "")
    retry_to = request.args.get("retry_to", "landing")
    message = EXCEPTION_MESSAGES.get(reason, "Something went wrong.")

    body = """
    <span class="story-tag">Exception handling &middot; KAN-15</span>
    <h1>We hit a snag</h1>
    <div class="banner-error">{message}</div>
    <div class="btn-row">
      <a class="btn" href="{retry_url}">Try again</a>
      <a class="btn ghost" href="{spec_url}">Speak to a specialist instead</a>
    </div>
    """.format(message=message, retry_url=url_for(retry_to), spec_url=url_for("specialist"))
    return render_page("Exception", "KAN-15", body)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
