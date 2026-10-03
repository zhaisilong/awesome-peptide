"""Auditable metadata snapshots for reproducible paper-read rendering."""

from datetime import datetime, timezone
import json
from pathlib import Path
import warnings

from awepep import crossref, utils


class MetadataStore:
    def __init__(self, path, offline=False, refresh=False):
        if offline and refresh:
            raise ValueError("offline and refresh_metadata cannot be combined")
        self.path = Path(path)
        self.offline = offline
        self.refresh = refresh
        self.works = {}
        if self.path.exists():
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if payload.get("version") != 1 or not isinstance(
                payload.get("works"), dict
            ):
                raise ValueError(f"Invalid metadata snapshot: {self.path}")
            self.works = payload["works"]
        self.changed = False

    @staticmethod
    def validate(metadata):
        for field in ("title", "authors", "publications", "publish_date"):
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                raise ValueError(f"Metadata missing {field}")
        utils.date_bounds(metadata["publish_date"])
        return metadata

    def get(self, doi):
        doi = crossref.normalize_doi(doi)
        cached = self.works.get(doi)
        if cached and not self.refresh:
            return self.validate(cached["metadata"])
        if self.offline:
            raise RuntimeError(
                f"Offline metadata missing for {doi}; run awe-pep --refresh-metadata"
            )
        try:
            metadata = self.validate(crossref.metadata_for_doi(doi))
        except (RuntimeError, ValueError) as exc:
            if not cached:
                raise
            warnings.warn(
                f"Metadata refresh failed for {doi}; using existing snapshot: {exc}"
            )
            return self.validate(cached["metadata"])
        record = {
            "source": (
                "https://arxiv.org/abs/" + doi.removeprefix("10.48550/arxiv.")
                if doi.startswith("10.48550/arxiv.")
                else "https://api.crossref.org/works/" + doi
            ),
            "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "metadata": metadata,
        }
        if cached and cached.get("verified_publish_date"):
            record["verified_publish_date"] = cached["verified_publish_date"]
            metadata["publish_date"] = cached["verified_publish_date"]["date"]
        self.works[doi] = record
        self.changed = True
        return metadata

    def save(self):
        if not self.changed:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                {"version": 1, "works": self.works},
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)
        self.changed = False
