# GroupMe Archive

A modern CLI tool for archiving and analyzing GroupMe chat data.

## Features

- **Standardized Archiving**: Export messages, user counts, and unique names to CSV.
- **Image Downloading**: Bulk download all images shared within a group.
- **Modern CLI**: Beautiful output with progress indicators using `typer` and `rich`.
- **Flexible Auth**: Support for environment variables, token files, or CLI options.

## Installation

```bash
pip install .
```

For development:
```bash
pip install -e ".[all]"
```

## Setup & Authentication

The tool needs a GroupMe Access Token. You can obtain one from the [GroupMe Developers](https://dev.groupme.com/) site.

You can provide the token in three ways (checked in order):
1. Command line option: `--token YOUR_TOKEN`
2. Environment variable: `export GROUPME_ACCESS_TOKEN=YOUR_TOKEN`
3. Token file: Create a `token.txt` file in your working directory containing only the token.

## Usage

Once installed, use the `groupme-archive` command:

### List all groups
Shows a list of all your groups with their IDs and creation dates.
```bash
groupme-archive list-groups
```

### Archive a group
Exports message history and statistics for a specific group ID.
```bash
# If you don't know the ID, run without arguments to see a list
groupme-archive archive

# To archive a specific group
groupme-archive archive --group-id 12345678
```
This creates:
- `historic_messages.csv`
- `message_count.csv`
- `unique_names.csv`

### Download images
Downloads all images from an existing archive CSV.
```bash
groupme-archive download-images MyGroupName
```
Images will be saved to `./Images/MyGroupName/`.

## Output Files

| File | Description |
|------|-------------|
| `historic_messages.csv` | Full message history with attachments and timestamps. |
| `message_count.csv` | Message count per user ID. |
| `unique_names.csv` | List of all display names used by each user ID. |

## License

Do whatever you want with it. Please just credit me.
