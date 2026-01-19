import csv
import datetime
import logging
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Generator

import requests

logger = logging.getLogger(__name__)

class GroupMeClient:
    """A lightweight client for the GroupMe API."""
    BASE_URL = "https://api.groupme.com/v3"

    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"X-Access-Token": token})

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()["response"]

    def list_groups(self) -> List[Dict[str, Any]]:
        """List all groups the user is in."""
        groups = []
        page = 1
        while True:
            batch = self._get("groups", params={"page": page, "per_page": 100})
            if not batch:
                break
            groups.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return groups

    def get_group(self, group_id: str) -> Dict[str, Any]:
        """Get details for a specific group."""
        return self._get(f"groups/{group_id}")

    def list_messages(self, group_id: str) -> Generator[Dict[str, Any], None, None]:
        """Yield all messages for a group, from newest to oldest."""
        before_id = None
        while True:
            params = {"limit": 100}
            if before_id:
                params["before_id"] = before_id
            
            try:
                batch = self._get(f"groups/{group_id}/messages", params=params)
                messages = batch.get("messages", [])
                if not messages:
                    break
                    
                for msg in messages:
                    yield msg
                
                before_id = messages[-1]["id"]
                # Respectful rate limiting
                time.sleep(0.1)
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 304: # No more messages
                    break
                raise

def formatted_timestamp(ts: Any) -> str:
    """Convert timestamp to formatted string."""
    return datetime.datetime.fromtimestamp(int(ts)).strftime('%m-%d-%Y %H:%M:%S')

def list_attachments(attachments: List[Dict[str, Any]]) -> str:
    """Return comma-separated string of image attachment URLs."""
    urls = [a['url'] for a in attachments if a['type'] == 'image']
    return ','.join(urls)

class Exporter:
    def __init__(self, client: GroupMeClient):
        self.client = client

    def list_groups_summary(self) -> Dict[str, str]:
        """List all groups and their creation times."""
        groups = self.client.list_groups()
        return {group['name']: formatted_timestamp(group['created_at']) for group in groups}

    def export_group_listing(self, output_path: Path = Path('Groups Created At.txt')):
        """Write group listing to a file."""
        group_times = self.list_groups_summary()
        with open(output_path, 'w', encoding='utf8') as f:
            for name, timestamp in group_times.items():
                f.write(f"{name}: {timestamp}\n")
        logger.info(f"Group listing exported to {output_path}")

    def archive_group(self, group_id: str, output_dir: Path = Path('.')):
        """Archive all messages, counts, and names for a group."""
        group_data = self.client.get_group(group_id)
        group_name = group_data['name']
        
        messages_list = []
        message_count_dict = defaultdict(int)
        unique_names_dict = defaultdict(set)
        
        total_count = 0
        logger.info(f"Starting archive for group: {group_name} ({group_id})")
        
        for data in self.client.list_messages(group_id):
            user_id = data['user_id']
            name = data['name']
            
            # Historic message data
            messages_list.append([
                user_id,
                name,
                data['text'],
                list_attachments(data['attachments']),
                formatted_timestamp(data['created_at'])
            ])
            
            # Counts
            message_count_dict[user_id] += 1
            message_count_dict['Total'] += 1
            
            # Names
            unique_names_dict[user_id].add(name)
            
            total_count += 1
            if total_count % 1000 == 0:
                logger.info(f"Processed {total_count} messages...")

        # Write CSVs
        output_dir.mkdir(parents=True, exist_ok=True)
        self._write_csv(output_dir / 'historic_messages.csv', messages_list)
        
        # Message counts
        counts = [[uid, count] for uid, count in message_count_dict.items()]
        self._write_csv(output_dir / 'message_count.csv', counts)
        
        # Unique names
        names = [[uid] + sorted(list(n_set)) for uid, n_set in unique_names_dict.items()]
        self._write_csv(output_dir / 'unique_names.csv', names)
        
        logger.info(f"Archive complete for {group_name}. Processed {total_count} messages.")

    def _write_csv(self, path: Path, rows: List[List[Any]]):
        with open(path, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
