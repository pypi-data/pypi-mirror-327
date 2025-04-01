"""
viindex.py

Provides a VideoIndexer class that manages a SQLite database for storing and
querying video metadata, as well as convenience functions.
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional


class VideoIndexer:
    """Manages the SQLite database for storing and querying video metadata."""

    def __init__(self, db_path: str = "viindex.db") -> None:
        """
        Initializes the VideoIndexer with the specified database path. If the
        database or table does not exist, it is created automatically.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # For dict-like cursor results
        self._setup_database()

    def _setup_database(self) -> None:
        """
        Creates the 'videos' table if it does not already exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_path TEXT NOT NULL,
            metadata TEXT
        );
        """
        with self.connection:
            self.connection.execute(query)

    def index_video(self, video_path: str, metadata: Dict[str, Any]) -> int:
        """
        Inserts a new video record into the database with its path and metadata.

        Args:
            video_path (str): File path or URL of the video.
            metadata (Dict[str, Any]): Key-value pairs of metadata.

        Returns:
            int: The auto-incremented ID of the newly inserted video.
        """
        query = """
        INSERT INTO videos (video_path, metadata)
        VALUES (?, ?);
        """
        metadata_str = json.dumps(metadata)
        cursor = self.connection.cursor()
        cursor.execute(query, (video_path, metadata_str))
        self.connection.commit()

        inserted_id = cursor.lastrowid
        return inserted_id

    def remove_video(self, video_id: int) -> None:
        """
        Removes a video record from the database by its ID.

        Args:
            video_id (int): The unique ID of the video to remove.
        """
        query = "DELETE FROM videos WHERE id = ?;"
        with self.connection:
            self.connection.execute(query, (video_id,))

    def search_videos(self, query_str: str) -> List[Dict[str, Any]]:
        """
        Searches the database for videos matching the query string. The search
        looks for matches in the 'video_path' or in the stringified 'metadata'.

        Args:
            query_str (str): A keyword to look for in the path or metadata.

        Returns:
            List[Dict[str, Any]]: A list of matching video records.
        """
        query = """
        SELECT id, video_path, metadata
        FROM videos
        WHERE video_path LIKE ?
           OR metadata LIKE ?
        """
        like_pattern = f"%{query_str}%"
        cursor = self.connection.cursor()
        cursor.execute(query, (like_pattern, like_pattern))
        rows = cursor.fetchall()

        results = []
        for row in rows:
            # Convert 'metadata' from JSON string to dict
            metadata = json.loads(row["metadata"]) if row["metadata"] else {}
            results.append(
                {
                    "id": row["id"],
                    "video_path": row["video_path"],
                    "metadata": metadata,
                }
            )
        return results

    def get_video_by_id(self, video_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single video's record from the database by its unique ID.

        Args:
            video_id (int): The unique ID of the video to retrieve.

        Returns:
            Optional[Dict[str, Any]]: A dictionary of the video's information
            if found, else None.
        """
        query = """
        SELECT id, video_path, metadata
        FROM videos
        WHERE id = ?
        LIMIT 1
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (video_id,))
        row = cursor.fetchone()

        if not row:
            return None

        metadata = json.loads(row["metadata"]) if row["metadata"] else {}
        return {
            "id": row["id"],
            "video_path": row["video_path"],
            "metadata": metadata,
        }

    def update_video_metadata(
        self, video_id: int, new_metadata: Dict[str, Any]
    ) -> bool:
        """
        Updates the metadata for an existing video record.

        Args:
            video_id (int): Unique ID of the video to update.
            new_metadata (Dict[str, Any]): Updated key-value pairs of metadata.

        Returns:
            bool: True if the record was updated, False if not found or no update occurred.
        """
        query = """
        UPDATE videos
        SET metadata = ?
        WHERE id = ?;
        """
        metadata_str = json.dumps(new_metadata)
        cursor = self.connection.cursor()
        cursor.execute(query, (metadata_str, video_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None


def create_indexer(db_path: str = "viindex.db") -> VideoIndexer:
    """
    Creates and returns a VideoIndexer instance with the given database path.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        VideoIndexer: An instance of the VideoIndexer class.
    """
    return VideoIndexer(db_path=db_path)
