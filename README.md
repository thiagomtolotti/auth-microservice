# Auth Microservice

## Setup

### Prerequisites

- Python 3.12 or greater
- Make
- UV

### Getting Started

After cloning the repository, run:

```bash
make setup
```

This command will:
- Initialize the virtual environment
- Sync dependencies
- Generate RS256 keys for encoding/decoding JWT tokens
- Build the Docker container

After setup, run:

```bash
make dev
```

This starts the development environment so you can begin working on the code.

To run tests, use `make tests`, `make tests-watch`, or `make coverage` to generate an HTML coverage report. All test commands support the `path` argument to filter tests by location.