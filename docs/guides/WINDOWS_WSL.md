# Windows development with WSL 2

WSL runs Linux tools on a Windows computer. It gives our Windows developer a
Linux environment for the same `uv` and `make` commands used in Linux CI.
macOS developers can continue working natively. Each developer has their own
checkout, virtual environment, and local app; GitHub shares code between them.
WSL does not connect computers or publish the app.

## 1. Install Ubuntu in WSL

In **PowerShell as Administrator**, on a supported Windows 10/11 installation:

```powershell
wsl --install -d Ubuntu
```

Restart if prompted, open **Ubuntu**, and complete its Linux username/password
setup. If WSL is already installed, inspect it first with `wsl --list --verbose`.
The Ubuntu entry should show version 2. Follow Microsoft's
[installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install)
if installation or virtualization prerequisites fail.

## 2. Install tools inside Ubuntu

Run these commands in the **Ubuntu terminal**, not PowerShell:

```bash
sudo apt update
sudo apt install -y git make curl ca-certificates
curl -LsSf https://astral.sh/uv/install.sh -o /tmp/cyber-uv-install.sh
sh /tmp/cyber-uv-install.sh
. "$HOME/.local/bin/env"
uv --version
```

This uses Astral's [official uv installer](https://docs.astral.sh/uv/getting-started/installation/).
Install Linux uv even if you already installed Windows uv. Do not run the project
or uv with `sudo`.

## 3. Clone into the Linux filesystem

```bash
mkdir -p ~/git
cd ~/git
git clone https://github.com/24juangonzalez/cyber-security-systems-test.git
cd cyber-security-systems-test
git branch --show-current
uv sync --locked --group dev --extra ui
make hooks
make check
uv run cyber-path validate fixtures/industrial/vendor_access.json
make ui
```

Use your normal GitHub authentication if the repository requires it. Do not put
tokens in the clone URL. A new clone starts on the default branch. If reviewing
unmerged work, switch to the agreed branch before syncing and testing; both
developers must use the same commit to compare results.

Keep this checkout in `~/git`, rather than reusing `C:\Users\...` through
`/mnt/c`. Microsoft recommends the
[Linux filesystem for Linux development](https://learn.microsoft.com/en-us/windows/wsl/filesystems).
Do not copy or share a Windows/macOS `.venv`; uv creates a Linux `.venv` here
using the repository's Python version and lockfile. Preserve any uncommitted
work in your old checkout before moving your workflow.

Open the address printed by Streamlit in your Windows browser, normally
`http://localhost:8501`. Windows can normally access a WSL-hosted application
through [localhost forwarding](https://learn.microsoft.com/en-us/windows/wsl/networking).
Use the printed port if another instance already occupies 8501. Keep the app
bound to `127.0.0.1`; no firewall opening or public listener is required.
Stop the server with **Ctrl+C** in Ubuntu.

## 4. Open the correct interpreter in VS Code

Install Microsoft's WSL extension in Windows VS Code. From the Ubuntu checkout,
run `code .`, or use **WSL: Open Folder in WSL** from VS Code's command palette.
Check that the window indicates **WSL: Ubuntu**, then choose the project's
`.venv/bin/python` with **Python: Select Interpreter**. Install the Python
extension in the WSL environment if VS Code prompts for it.

## When something fails

Run these in Ubuntu and share the output plus the exact failing command and error:

```bash
pwd
uname -s
command -v uv
git branch --show-current
git rev-parse --short HEAD
uv --version
uv run python -c "import sys; print(sys.platform); print(sys.executable)"
```

Expected: `Linux` / `linux`, a Linux uv executable, and Python under this
checkout's `.venv/bin/`. If paths point to `C:\...`, `.venv/Scripts`, or Windows
executables under `/mnt/c`, you are mixing environments. Open Ubuntu and use the
Linux checkout instead.

WSL is a development option, not proof that the app is production-ready or that
a particular Windows error is fixed. This setup must still be tested on your
partner's machine. Native Windows CLI coverage stays in CI; Linux CI covers
the full test suite. Continue using synthetic data only.
