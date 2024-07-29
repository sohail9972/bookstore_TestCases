| Requests                 | Status Code |
|--------------------------|-------------|
| health(/health)          | 200         |
| get(/books)              | 200         |
| post(/books)             | 200         |
| put(/books/{book_id})    | 200         |
| get(/book/{book_id})     | 200         |
| delete(/books/{book_id}) | 200         |
| signup(/signup)          | 200         |
| login(/login)            | 200         |

# Test Strategy :
- This document outlines the testing strategy employed for the FastAPI application, including the approach to unit tests and integration tests.
- Ensuring reliability and maintainability, and addressing challenges encountered during the process.

> # Unit Tests

Unit tests are designed to test individual functions or methods in isolation.

### Isolation: 
Testing individual functions or methods without dependencies on other parts of the application.

### Mocking:
Using mocking to simulate dependencies and isolate the unit under test.

### Edge Cases: 
Writing tests for edge cases and unexpected inputs to ensure robustness.

### Example:

Testing individual CRUD operations for a book (**test_create_post**, **test_update_book**, **test_get_book**, **test_delete_book**).


> # Integration Tests
Integration tests verify the interaction between multiple components or services.

### End-to-End Scenarios: 
Testing complete workflows to ensure all parts of the system work together as expected.
### Database Integration: 
Using a real database (SQLite in-memory) to test database interactions.
### API Testing: 
Using TestClient to test API endpoints and their interactions.

### Example:

Testing the full CRUD lifecycle for a book (**test_create_update_get_delete_EndToEnd_book**).

## Reliability:

### Consistent Test Environment: 
Using an isolated and consistent in-memory SQLite database for testing.
### Deterministic Tests: 
Writing tests that produce the same results every time they are run.
### Automated Testing: 
Integrating tests into a continuous integration (CI) pipeline to automatically run tests on code changes.

## Maintainability:

### Clear Naming Conventions: 
Using descriptive names for test functions to make them easily understandable.
### Reusable Helpers: 
Creating helper functions (headers(), create_payload(), etc.) to avoid code duplication and simplify test setup.
### Regular Refactoring: 
Periodically reviewing and refactoring test code to keep it clean and efficient.
### Documentation: 
Documenting the purpose and usage of tests to provide context for future developers.


# Challenges:

- I was new so started to work on the Fast API from Scratch.
- Connecting Databases and mocking was new experience.
- Generating unique data while hitting the APIs.
- Understanding of GitHub actions setup.
- Docker is new to me, I need to get my hands on over it.
- Managing test data, especially for integration tests, can become complex and cumbersome.