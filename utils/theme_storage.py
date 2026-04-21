from abc import ABC, abstractmethod
from typing import Optional
import json
import os
import re
import sqlite3


# ── Abstract Base ──────────────────────────────────────────────────────────────

class ThemeStorage(ABC):
    """Abstract base class for theme storage backends."""

    @abstractmethod
    def save_theme(self, name: str, data: dict) -> bool:
        pass

    @abstractmethod
    def load_theme(self, name: str) -> Optional[dict]:
        pass

    @abstractmethod
    def list_themes(self) -> list[str]:
        pass

    @abstractmethod
    def delete_theme(self, name: str) -> bool:
        pass


# ── Local File Backend ─────────────────────────────────────────────────────────

class LocalFileStorage(ThemeStorage):
    """Local JSON file backend — dev fallback."""

    def __init__(self, themes_dir: str = "themes/custom_db"):
        self.themes_dir = themes_dir
        os.makedirs(themes_dir, exist_ok=True)

    def _path(self, name: str) -> str:
        safe = "".join(c for c in name if c.isalnum() or c in ("-", "_"))
        return os.path.join(self.themes_dir, f"{safe}.json")

    def save_theme(self, name: str, data: dict) -> bool:
        try:
            with open(self._path(name), "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def load_theme(self, name: str) -> Optional[dict]:
        path = self._path(name)
        if not os.path.exists(path):
            return None
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None

    def list_themes(self) -> list[str]:
        if not os.path.exists(self.themes_dir):
            return []
        return [f.replace(".json", "") for f in os.listdir(self.themes_dir) if f.endswith(".json")]

    def delete_theme(self, name: str) -> bool:
        path = self._path(name)
        if not os.path.exists(path):
            return False
        try:
            os.remove(path)
            return True
        except Exception:
            return False


# ── SQLite Backend ─────────────────────────────────────────────────────────────

class SQLiteThemeStorage(ThemeStorage):
    """SQLite backend — works locally and on Streamlit Cloud (/tmp)."""

    def __init__(self, db_path: str = None):
            if db_path is None:
                import tempfile
                db_path = os.path.join(tempfile.gettempdir(), "gitcanvas_themes.db")
            self.db_path = db_path
            self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS themes (
                    name TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_theme(self, name: str, data: dict) -> bool:
        try:
            with self._connect() as conn:
                conn.execute("""
                    INSERT INTO themes (name, data) VALUES (?, ?)
                    ON CONFLICT(name) DO UPDATE SET data = excluded.data
                """, (name, json.dumps(data)))
                conn.commit()
            return True
        except Exception:
            return False

    def load_theme(self, name: str) -> Optional[dict]:
        try:
            with self._connect() as conn:
                row = conn.execute("SELECT data FROM themes WHERE name = ?", (name,)).fetchone()
            return json.loads(row[0]) if row else None
        except Exception:
            return None

    def list_themes(self) -> list[str]:
        try:
            with self._connect() as conn:
                rows = conn.execute("SELECT name FROM themes ORDER BY name").fetchall()
            return [row[0] for row in rows]
        except Exception:
            return []

    def delete_theme(self, name: str) -> bool:
        try:
            with self._connect() as conn:
                cursor = conn.execute("DELETE FROM themes WHERE name = ?", (name,))
                conn.commit()
            return cursor.rowcount > 0
        except Exception:
            return False


# ── Firebase Backend ───────────────────────────────────────────────────────────

class FirebaseThemeStorage(ThemeStorage):
    """
    Firebase Firestore backend — for production cloud persistence.
    Requires FIREBASE_CREDENTIALS env var (JSON string of service account).
    Falls back gracefully if credentials not set.
    """

    def __init__(self):
        self._db = None
        self._collection = "custom_themes"
        self._init_firebase()

    def _init_firebase(self):
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore

            creds_json = os.environ.get("FIREBASE_CREDENTIALS")
            if not creds_json:
                return

            if not firebase_admin._apps:
                cred = credentials.Certificate(json.loads(creds_json))
                firebase_admin.initialize_app(cred)

            self._db = firestore.client()
        except Exception:
            self._db = None  # Graceful fallback

    def _is_available(self) -> bool:
        return self._db is not None

    def save_theme(self, name: str, data: dict) -> bool:
        if not self._is_available():
            return False
        try:
            self._db.collection(self._collection).document(name).set(data)
            return True
        except Exception:
            return False

    def load_theme(self, name: str) -> Optional[dict]:
        if not self._is_available():
            return None
        try:
            doc = self._db.collection(self._collection).document(name).get()
            return doc.to_dict() if doc.exists else None
        except Exception:
            return None

    def list_themes(self) -> list[str]:
        if not self._is_available():
            return []
        try:
            docs = self._db.collection(self._collection).stream()
            return [doc.id for doc in docs]
        except Exception:
            return []

    def delete_theme(self, name: str) -> bool:
        if not self._is_available():
            return False
        try:
            self._db.collection(self._collection).document(name).delete()
            return True
        except Exception:
            return False


# ── Auto-select Backend ────────────────────────────────────────────────────────

def get_storage_backend() -> ThemeStorage:
    """
    Auto-selects storage backend based on environment:
    - FIREBASE_CREDENTIALS set → FirebaseThemeStorage
    - Otherwise              → SQLiteThemeStorage (default for Streamlit Cloud)
    """
    if os.environ.get("FIREBASE_CREDENTIALS"):
        backend = FirebaseThemeStorage()
        if backend._is_available():
            return backend

    # Use SQLite by default — survives Streamlit Cloud restarts better than local files
    return SQLiteThemeStorage()