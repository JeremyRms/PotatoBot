"""
Environment helpers for loading secrets into process env.
"""

import os
from typing import Optional

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # If PyYAML isn't installed, we'll skip file parsing gracefully


def ensure_github_token(verbose: bool = True) -> bool:
    """Ensure GITHUB_TOKEN is set in os.environ.

    Returns True if the token is present or successfully loaded from
    fastagent.secrets.yaml; otherwise False.
    """
    if os.getenv("GITHUB_TOKEN"):
        return True

    secrets_path = "fastagent.secrets.yaml"
    if not os.path.exists(secrets_path):
        if verbose:
            print("⚠️  fastagent.secrets.yaml not found; GITHUB_TOKEN not set in environment")
        return False

    if yaml is None:
        if verbose:
            print("⚠️  PyYAML not installed; cannot read fastagent.secrets.yaml")
        return False

    try:
        with open(secrets_path, "r") as f:
            secrets = yaml.safe_load(f) or {}
            token: Optional[str] = secrets.get("GITHUB_TOKEN")
            if token:
                os.environ["GITHUB_TOKEN"] = token
                if verbose:
                    print("✅ Loaded GITHUB_TOKEN from fastagent.secrets.yaml")
                return True
            else:
                if verbose:
                    print("⚠️  GITHUB_TOKEN not found in fastagent.secrets.yaml")
                return False
    except Exception as exc:  # pragma: no cover
        if verbose:
            print(f"❌ Failed to read fastagent.secrets.yaml: {exc}")
        return False
