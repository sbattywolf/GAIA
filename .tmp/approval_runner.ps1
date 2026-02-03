Set-Location 'E:\Workspaces\Git\GAIA'
$env:TELEGRAM_BOT_TOKEN='8560309642:AAHFhGAzcVNkY1hLwuSMedy-FRh5I0Dyc28'
$env:CHAT_ID='784711097'
# ensure repo root is on PYTHONPATH so `from gaia import ...` works
$env:PYTHONPATH=(Get-Location).Path
python scripts\approval_listener.py --timeout 1800