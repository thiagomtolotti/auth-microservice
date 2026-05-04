from functools import lru_cache
from pathlib import Path


class Settings:
    @property
    @lru_cache()  # Ensures the file is only read once and then cached in memory
    def private_key(self) -> str:
        certs_path = Path(__file__).parent.parent.parent / "certs"
        path = certs_path / "private_key.pem"

        if not path.exists():
            raise FileNotFoundError(f"Key not found at {path}")

        print(f"Loading private key from {path}")
        return path.read_text()

    @property
    @lru_cache()
    def public_key(self) -> str:
        certs_path = Path(__file__).parent.parent.parent / "certs"
        path = certs_path / "public_key.pem"

        if not path.exists():
            raise FileNotFoundError(f"Key not found at {path}")

        print(f"Loading public key from {path}")
        return path.read_text()


settings = Settings()
