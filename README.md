# Log Ingestor Project

The Log Ingestor is a simple Flask-based application for ingesting, searching, and filtering logs. This README provides information on how to run the project, the system design, a list of features implemented, and identified issues.

## How to Run the Project

### Prerequisites

- Python 3
- Pip (package installer for Python)
- Virtualenv (optional but recommended)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/log-ingestor.git
    ```

2. Navigate to the project directory:

    ```bash
    cd log-ingestor
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    virtualenv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Open two terminals.

7. In the first terminal, run the Flask application:

    ```bash
    python app.py
    ```

    The application will run on http://localhost:3000/.

8. In the second terminal, run the CLI with the desired command:

    ```bash
    python cli.py --ingest-json '{"level": "info", "message": "Log message", "resourceId": "123", "timestamp": "2023-01-01T12:00:00Z"}'
    ```

    You can also run other CLI commands such as search or filter.

## System Design

The Log Ingestor uses Flask as the backend framework, SQLite as the database, and provides RESTful APIs for log ingestion, searching, and filtering.

## Features Implemented

1. **Log Ingestion**
    - Endpoint: `/ingest`
    - Method: POST
    - Example CLI Input:

        ```bash
        python cli.py --ingest-json '{"level": "info", "message": "Log message", "resourceId": "123", "timestamp": "2023-01-01T12:00:00Z"}'
        ```

    - Additional methods:
        - Ingest from JSON file:

            ```bash
            python cli.py --ingest-file path/to/logs.json
            ```

        - Ingest from command-line arguments:

            ```bash
            python cli.py --ingest-level "info" --ingest-message "Log message" --ingest-resourceId "123" --ingest-timestamp "2023-01-01T12:00:00Z"
            ```

2. **Log Search**
    - Endpoint: `/search`
    - Method: POST
    - Example CLI Input:

        ```bash
        python cli.py --search "level=error message=Failed to connect"
        ```

3. **Log Filtering**
    - Endpoint: `/filter`
    - Method: GET
    - Example CLI Input:

        ```bash
        python cli.py --filter-level "error" --filter-resourceId "456" --filter-timestamp "2023-09-01T00:00:00Z" --filter-traceId "789"
        ```

    - Combining Filters:
        - Example CLI Input:

            ```bash
            python cli.py --filter-level "error" --filter-resourceId "456" --filter-timestamp "2023-09-01T00:00:00Z" --filter-traceId "789" --filter-spanId "123"
            ```

## Identified Issues

1. Issue: When providing timestamp filters, the application currently requires both start and end timestamps.
   - Example CLI Input:

       ```bash
       python cli.py --filter-timestamp-start "2023-09-01T00:00:00Z" --filter-timestamp-end "2023-09-10T23:59:59Z"
       ```

2. Issue: The application may not handle certain edge cases and may lack robust error handling.

Feel free to contribute or open issues for any identified problems or feature requests.

