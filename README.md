# DEPTHIVE — Starter Foundation

A Streamlit starter for the DEPTHIVE organizational-intelligence prototype.

## 1. Install
Use Python 3.10+.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## Included
- Premium dark landing page
- Login, signup, and password-recovery placeholder
- SQLite user store with salted scrypt password hashes
- Authenticated navigation shell
- Overview placeholder with no fabricated live metrics
- CSV/Excel upload preview in Data Hub
- Consistent custom styling

## Important prototype limitations
- Signup does not verify email addresses or enforce admin approval yet.
- Forgot-password does not send email; secure expiring reset tokens and email delivery are not configured.
- Role is stored as a requested role, not yet used to enforce authorization. Do not deploy this as a production multi-user service until server-side role/organization access controls, CSRF/session hardening, rate limits, email verification, reset flow, secrets management, and deployment security are implemented.
- Analytics modules are navigation scaffolds until connected to real validated data.
- Use synthetic or explicitly authorized data for demos.

## Suggested next build order
1. Organization and department schema
2. Data Hub: persist uploaded datasets and column mappings
3. KPI configuration and metric calculation engine
4. Executive overview and department drill-down
5. Risk / WHY / recommendations
6. Reports, audit trail, and authorization enforcement
