# UV Setup Guide (Windows / PowerShell)

## I. Install UV (Run Once)

Open **PowerShell** and run:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Add UV to PATH (if not automatically added)

Replace `{your_user}` with your Windows username:

```powershell
[Environment]::SetEnvironmentVariable(
  "Path",
  $env:Path + ";C:\Users\{your_user}\.local\bin",
  [EnvironmentVariableTarget]::User
)
```

Restart PowerShell.

Verify installation:

```powershell
uv --version
```

---

## II. Project Setup (Per Project)

Navigate to your project directory:

```powershell
cd path\to\your\project
```

Create virtual environment:

```powershell
uv venv
```

Activate it:


```powershell
.venv\Scripts\Activate.ps1
```

if it dosent work try
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

then 
.venv\Scripts\Activate.ps1



Install dependencies (if `pyproject.toml` exists):

```powershell
uv sync
```

---

## III. Daily Workflow

Install in edditable mode is a good way to keep things clean
uv pip install -e .

Activate environment:

```powershell
.venv\Scripts\Activate.ps1
```

Sync dependencies (only if updated):

```powershell
uv sync
```

Run Python:

```powershell
python main.py
```

Or without manual activation:

```powershell
uv run python main.py
```

---

## IV. Managing Dependencies

Activate environment first.

### Add Dependency

```powershell
uv add package-name
```

This updates:
- `pyproject.toml`
- `uv.lock`

Commit both files.

### Remove Dependency

```powershell
uv remove package-name
uv sync
```

---

## V. Rebuild Environment (Clean Reset)

```powershell
deactivate
Remove-Item -Recurse -Force .venv
uv venv
.venv\Scripts\Activate.ps1
uv sync
```

---

## VI. Rules

- Commit `pyproject.toml` and `uv.lock`.
- Never commit `.venv/`.
- Always activate `.venv` before running code.
- Never use `pip install` directly. Use `uv add`.

Deterministic environments require lockfile discipline.

---

# Virtual Environment Guide (Standard venv, Windows / PowerShell)

## I. Create Virtual Environment

Navigate to project directory:

```powershell
cd path\to\your\project
```

Create environment:

```powershell
python -m venv .venv
```

---

## II. Activate Environment

```powershell
.venv\Scripts\Activate.ps1
```

---

## III. Install Dependencies

If using `requirements.txt`:

```powershell
pip install -r requirements.txt
```

Install single package:

```powershell
pip install package-name
```

Freeze dependencies:

```powershell
pip freeze > requirements.txt
```

Commit `requirements.txt`.

---

## IV. Daily Workflow

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

Run:

```powershell
python main.py
```

---

## V. Rebuild Environment

```powershell
deactivate
Remove-Item -Recurse -Force .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## VI. Rules

- Commit `requirements.txt`.
- Never commit `.venv/`.
- Always activate before execution.
- Reinstall from `requirements.txt` on new machines.

UV provides lockfile determinism. `venv + pip` relies on manual discipline.