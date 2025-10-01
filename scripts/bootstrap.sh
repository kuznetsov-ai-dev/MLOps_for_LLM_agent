# /scripts/bootstrap.sh
#!/usr/bin/env bash
# путь: /scripts/bootstrap.sh
set -euo pipefail

echo "[*] Создаю venv и ставлю dev-зависимости..."
make deps

echo "[*] Устанавливаю pre-commit хуки..."
make precommit-install

echo "[✓] Готово. Запусти 'make check' и 'make format' для проверки стиля."
