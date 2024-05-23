# Translator-AI

Translator-AI is an API designed to translate documents into multiple languages.

"""

## Project Structure

This project follows a typical structure for FastAPI web applications, plus definitions for additional resources. Here is an overview of the key directories
and files:

- `main.py`: This is the entrypoint of the application.
- `src/translator/`: Contains the main application code.
    - `models.py`: This file includes the SQLAlchemy models.
    - `schemas.py`: This file includes the Pydantic models.
    - `router.py`: This file contains the API definitions.
    - `service.py`: This file includes the main business logic.
    - `tasks.py`: This file contains background tasks.
    - `external_services.py`: This file includes business logic to access external APIs.

- `tests/`: Contains unit tests for the application functionality.

- `docker-compose.yaml`: Docker Compose file to orchestrate the application and any associated services.

- `.env`: A file for setting environment variables. This file is not tracked by version control.

Please refer to the individual directories and files for more detailed documentation about each component.
"""

## Setup

1. Set your OpenAI API key in the `.env` file under `OPENAI_API_KEY`.

## Running the Project

To start the project, use Docker Compose:

```bash
docker-compose up -d
```

To stop the project, use:

```bash
docker-compose down
```

The application should now be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Testing

The project includes simple unit tests. You can manually test the API using the `test_main.http` file.

## FastAPI Endpoints

### Swagger API Documentation

Access the Swagger UI to explore and test the API:

```
GET http://127.0.0.1:5000/
Accept: application/json
```

### Translate Endpoint

To translate text into multiple languages, use the following endpoint:

```
POST http://127.0.0.1:5000/translate
Content-Type: application/json

{
  "text": "Hello, world!",
  "languages": [
    "es", "fr", "de", "it", "ru", "ja", "ar", "ko", "vi", "zh"
  ]
}
```

### Trigger Translation

To trigger a translation process, use the following endpoint:

```
POST http://127.0.0.1:5000/translate/<translation_id>/trigger
Content-Type: application/json
```

### Get Translation

To retrieve a translation, use the following endpoint:

```
GET http://127.0.0.1:5000/translate/<translation_id>
Content-Type: application/json
```

## Future Improvements

- Implement additional tests.
- Add validation for supported languages
- Add authentication and authorization.
- Decouple background tasks, potentially using a pub/sub model.
- Test the performance of models and prompts for translation.