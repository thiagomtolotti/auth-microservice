from pathlib import Path

private_key: str = ""
public_key: str = ""


def setup_environment():
    print("Setting up environment variables...")

    load_certs()


def load_certs():
    global private_key, public_key

    certs_path = Path("certs")
    private_key_path = certs_path / "private_key.pem"
    public_key_path = certs_path / "public_key.pem"

    if not private_key_path.exists() or not public_key_path.exists():
        raise FileNotFoundError(
            "Certificate files not found. Please ensure they were generated correctly."
        )

    with open(private_key_path) as key_file:
        private_key = key_file.read()

    with open(public_key_path, "r") as key_file:
        public_key = key_file.read()
