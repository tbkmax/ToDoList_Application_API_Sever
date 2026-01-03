
---

### 1. Users Table

This table stores account information. It is the parent table for everything else.

|**Column Name**|**Data Type**|**Constraints**|**Description**|
|---|---|---|---|
|`id`|`UUID`|**PK**, Default: `gen_random_uuid()`|Unique identifier for each user.|
|`email`|`VARCHAR(255)`|`UNIQUE`, `NOT NULL`|User's login email.|
|`password_hash`|`TEXT`|`NOT NULL`|The hashed password (never store plain text).|
|`created_at`|`TIMESTAMPTZ`|Default: `NOW()`|Timestamp of account creation.|

### 2. Categories Table

Allowing users to group tasks (e.g., "Work," "Personal") makes the API much more useful.

| **Column Name** | **Data Type** | **Constraints**                        | **Description**                           |
| --------------- | ------------- | -------------------------------------- | ----------------------------------------- |
| `id`            | `UUID`        | **PK**, Default: `gen_random_uuid()`   | Unique identifier for the category.       |
| `user_id`       | `UUID`        | **FK** (Users.id), `ON DELETE CASCADE` | Links the category to a specific user.    |
| `name`          | `VARCHAR(50)` | `NOT NULL`                             | Name of the category (e.g., "Groceries"). |

### 3. Tasks Table

This is the core table where the actual to-do items live.

| **Column Name** | **Data Type**  | **Constraints**                      | **Description**                       |
| --------------- | -------------- | ------------------------------------ | ------------------------------------- |
| `id`            | `UUID`         | **PK**, Default: `gen_random_uuid()` | Unique identifier for the task.       |
| `user_id`       | `UUID`         | **FK** (Users.id), `NOT NULL`        | Ensures every task belongs to a user. |
| `category_id`   | `UUID`         | **FK** (Categories.id), `SET NULL`   | Optional link to a category.          |
| `title`         | `VARCHAR(255)` | `NOT NULL`                           | The task summary.                     |
| `description`   | `TEXT`         |                                      | Detailed notes about the task.        |
| `is_completed`  | `BOOLEAN`      | Default: `FALSE`                     | The status of the task.               |
| `due_date`      | `TIMESTAMPTZ`  |                                      | When the task needs to be done.       |
| `priority`      | `INT`          | Default: `0`                         | Numeric scale (e.g., 1=Low, 3=High).  |
| `updated_at`    | `TIMESTAMPTZ`  | Default: `NOW()`                     | Automatically updated on changes.     |
| created_at      | `TIMESTAMPTZ`  | Default: `NOW()` at created time     | No updated                            |

---
