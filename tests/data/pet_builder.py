from typing import Any, Dict


class PetBuilder:
    def __init__(self):
        self._data: Dict[str, Any] = {
            "name": "DefaultName",
            "status": "available"
        }

    def with_name(self, name):
        self._data["name"] = name
        return self

    def with_status(self, status):
        self._data["status"] = status
        return self

    def without_name(self):
        self._data.pop("name", None)
        return self

    def with_photo_urls(self, urls):
        self._data["photoUrls"] = urls
        return self

    def without_photo_urls(self):
        self._data.pop("photoUrls", None)
        return self

    def with_category(self, category_id=None, name=None):
        self._data["category"] = {
            "id": category_id,
            "name": name
        }
        return self

    def without_category(self):
        self._data.pop("category", None)
        return self

    def with_tags(self, tags):
        self._data["tags"] = tags
        return self

    def with_single_tag(self, tag_id=None, name=None):
        self._data["tags"] = [
            {
                "id": tag_id,
                "name": name
            }
        ]
        return self

    def without_tags(self):
        self._data.pop("tags", None)
        return self

    def build(self):
        return self._data
