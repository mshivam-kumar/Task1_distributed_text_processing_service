# Distributed Text Processing Service

A simple distributed system that processes text using Docker containers. The client sends requests to a central server, which forwards them to specialized text processing services.

## How It Works

```
Client  --->  Central Server  --->  Text Services
                                    - Uppercase
                                    - Lowercase
                                    - Reverse
                                    - Word Count
```

The client talks only to the central server. The server then routes requests to the correct service based on what operation you choose.

## Project Structure

```
├── client/                 # User interface
├── central_server/         # Routes requests & logs
├── uppercase_service/      # Converts to UPPERCASE
├── lowercase_service/      # Converts to lowercase
├── reverse_service/        # Reverses text
├── wordcount_service/      # Counts words
├── docker-compose.yml      # Docker configuration
└── README.md
```

## Requirements

- Docker
- Docker Compose

## How to Run

1. Start all services:
   ```bash
   sudo docker compose up --build
   ```

2. Open another terminal and connect to client:
   ```bash
   sudo docker attach client
   ```

3. Follow the menu to process text.

## Example Usage

```
========================================
   Text Processing Service Menu
========================================
  1. Convert text to UPPERCASE
  2. Convert text to lowercase
  3. Reverse text
  4. Count number of words
  5. Exit
========================================

Enter choice: 1
Enter text: Hello World
Result: HELLO WORLD

Enter choice: 4
Enter text: This is a test
Result: 4

Enter choice: 3
Enter text:
Error: Input text cannot be empty

Enter choice: 5
Exiting...
```

## Error Handling

The system handles:
- Empty input text
- Invalid menu choices
- Service unavailable errors

## Logging

All requests are logged by the central server in `/app/logs/server.log`.

## Adding New Services

1. Create a new folder with `app.py` and `Dockerfile`
2. Add `/health` and `/process` endpoints
3. Add service to `docker-compose.yml`
4. Register in `central_server/app.py`

## Stop Services

```bash
docker compose down
```
