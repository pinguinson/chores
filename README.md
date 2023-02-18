# Shared chore tracker

Architecture:

* DB - sqlite3:
  * Chore configurations:
    * Title
    * Frequency:
      * Every N days/weeks/months
      * N days since last completed
      * On demand
  * Log of completions:
    * Timestamp
    * Chore name
    * Person
* Backend - Python FastAPI server running on raspberry pi:
  * GET /chores - returns list of chore configs
  * GET /reminders - returns upcoming chore reminders
  * GET /{chore_name}/assignee - returns person responsible for next chore instance
  * PUT /log - logs chore completion
* Frontend:
  * Shortcuts app - sort of API gateway:
    * Can send HTTP requests to backend
    * Can edit reminders
    * Supports NFC tags
  * Reminders app - acts as an actual UI
  * NFC tags for quick actions, e.g.:
    * Tap washing machine to log chore completion
      * Also creates reminder to put laundry into dryer
    * Tap bin when it’s full to create a reminder
