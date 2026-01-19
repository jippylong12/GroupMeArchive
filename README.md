# GroupMe Archive

A Python tool for archiving and analyzing GroupMe chat data.

## Features

### Group Listing (`group_created`)
Creates a file listing all your GroupMe groups with their creation timestamps.

### Group Archive (`group_archive`)
For a given group, generates three CSV files:

| File | Contents |
|------|----------|
| `historic_messages.csv` | User ID, name at time of message, message text, image attachments (URLs), timestamp |
| `message_count.csv` | User ID, total message count per user |
| `unique_names.csv` | User ID, list of all names that user has used |

### Analysis Tools (`analysis.py`)
Utilities for working with archived message data.

**Workflow:** Run `group_archive()` first to create `historic_messages.csv`, then use analysis tools.

| Function | Reads From | Outputs To |
|----------|------------|------------|
| `load_messages()` | `./historic_messages.csv` | Returns list in memory |
| `urls(messages)` | In-memory message list | Returns list of (url, timestamp) tuples |
| `download_images(group_name)` | `./historic_messages.csv` | `./Images/{group_name}/` directory |

> **Note:** All paths are relative to your current working directory when running the script.

## Requirements

- Python 3.x
- [Groupy](https://pypi.org/project/groupy/) library

```bash
pip install groupy
```

## Setup

1. **Get your API token:**
   - Go to [GroupMe Developers](https://dev.groupme.com/)
   - Log in with your GroupMe account
   - Copy your access token

2. **Create token file:**
   - Create a file named `token.txt` in the project directory
   - Paste your access token on the first line

## Usage

### List All Groups
```python
from main import group_created

with open('token.txt', 'r') as f:
    token = f.readline().strip()

group_created(token)
# Creates: Groups Created At.txt
```

### Archive a Group
```python
from groupy.client import Client

with open('token.txt', 'r') as f:
    token = f.readline().strip()

client = Client.from_token(token)

# List all groups to find the group ID you want
groups = client.groups.list()
for group in groups:
    print(f"{group.name}: {group.data['group_id']}")

# Archive a specific group
from main import group_archive
group_id = 'YOUR_GROUP_ID'
group_archive(group_id, client)
# Creates: historic_messages.csv, message_count.csv, unique_names.csv
```

### Download Images
```python
from analysis import download_images

download_images('MyGroupName')
# Downloads all images to: ./Images/MyGroupName/
```

## Output Files

### `Groups Created At.txt`
```
Group Name: 01-15-2024 14:30:00
Another Group: 12-25-2023 09:00:00
```

### `historic_messages.csv`
| Column | Description |
|--------|-------------|
| 1 | User ID |
| 2 | Display name at time of message |
| 3 | Message text |
| 4 | Comma-separated image URLs |
| 5 | Timestamp (MM-DD-YYYY HH:MM:SS) |

### `message_count.csv`
| Column | Description |
|--------|-------------|
| 1 | User ID (or "Total") |
| 2 | Message count |

### `unique_names.csv`
| Column | Description |
|--------|-------------|
| 1 | User ID |
| 2+ | Names that user has used |

## License

Do whatever you want with it. Please just credit me.
