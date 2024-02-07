# Development
To run/develop this project locally:

1. Clone this repository
2. Setup an environment
    ```sh
    python3 -m venv ./.venv
    source ./.venv/bin/activate
    ```
3. Install dependendencies
    ```sh
    pip install -e ".[dev]"
    ```
4. Make any changes necessary
5. Run the QA suite
    ```sh
    make qa
    ```