import httpx
import logging
import re
from typing import Dict, Any, List, Optional
from .base_provider import BaseResourceProvider
from ...models.resource import ReuseDecision

logger = logging.getLogger(__name__)

class DikshaProvider(BaseResourceProvider):
    """
    DIKSHA Production Adapter for Sunbird API.
    Handles hierarchy resolution, stale ID mapping, and asset discovery.
    """

    SEARCH_URL = "https://diksha.gov.in/api/content/v1/search"
    READ_URL = "https://diksha.gov.in/api/content/v1/read"
    HIERARCHY_URL = "https://diksha.gov.in/action/content/v3/hierarchy"

    def __init__(self):
        from ...config.app_config import settings
        self.settings = settings
        self.session_token = None

    def get_source_id(self) -> str:
        return "DIKSHA"

    def extract_id_from_url(self, url: str) -> Optional[str]:
        """Extracts Sunbird 'do_id' from various DIKSHA URL formats."""
        import re
        patterns = [
            r"do_[0-9]+", # Direct ID
            r"/collection/(do_[0-9]+)",
            r"/content/(do_[0-9]+)",
            r"/course/(do_[0-9]+)",
            r"identifier=(do_[0-9]+)"
        ]
        for p in patterns:
            match = re.search(p, url)
            if match:
                return match.group(1) if "(" in p else match.group(0)
        return None

    async def _authenticate(self, class_level: str = "class_5"):
        # ... (authentication logic)
        self.session_token = "GUEST_SESSION"

    async def resolve_collection(self, collection_id: str) -> Dict[str, Any]:
        """Recursive hierarchy resolution using Sunbird Hierarchy API."""
        logger.info(f"Resolving DIKSHA collection hierarchy: {collection_id}")

        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-App-Id": "prod.diksha.portal"
        }

        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            try:
                # Use v3/hierarchy for authoritative unit/chapter mapping
                resp = await client.get(f"{self.HIERARCHY_URL}/{collection_id}", timeout=20.0)
                if resp.status_code == 200:
                    data = resp.json().get('result', {}).get('content', {})
                    return self._map_diksha_hierarchy(data)
                else:
                    # Fallback to read API if hierarchy fails
                    logger.warning(f"DIKSHA Hierarchy failed for {collection_id}: {resp.status_code}. Using fallback.")
                    url = f"{self.READ_URL}/{collection_id}?fields=children,name,publisher,organisation,license,board,gradeLevel,subject,medium,description,leafNodes"
                    resp = await client.get(url, timeout=20.0)
                    if resp.status_code == 200:
                        data = resp.json().get('result', {}).get('content', {})
                        return self._map_diksha_hierarchy_fallback(data, client)
            except Exception as e:
                logger.error(f"Hierarchy resolution failed for {collection_id}: {e}")

        return {"error": "Collection not found", "status": "FAILED"}

    def _map_diksha_hierarchy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maps full hierarchical Sunbird response including chapters/units."""
        collection_meta = self._map_diksha_collection_header(data)

        # Capture full structure
        units = []
        resources = []

        def traverse(node, parent_id, chapter_name=None):
            current_name = node.get('name', '')

            # Detect if this node is likely a Chapter (usually has "Chapter" or "Ch " in title)
            is_chapter = "chapter" in current_name.lower() or re.match(r"^\d+[- ]", current_name)
            new_chapter_name = current_name if is_chapter else chapter_name

            if node.get('mimeType') == 'application/vnd.ekstep.content-collection':
                # This is a Unit or Chapter collection
                units.append({
                    "id": node.get('identifier'),
                    "title": current_name,
                    "parent_id": parent_id,
                    "type": "UNIT",
                    "chapter_name": new_chapter_name
                })
                for child in node.get('children', []):
                    traverse(child, node.get('identifier'), new_chapter_name)
            else:
                # This is a leaf resource
                resources.append({
                    "id": node.get('identifier'),
                    "original_id": node.get('identifier'),
                    "parent_id": parent_id,
                    "title": current_name,
                    "type": self._map_mime_to_type(node.get('mimeType')),
                    "license": node.get('license'),
                    "url": f"https://diksha.gov.in/play/content/{node.get('identifier')}",
                    "downloadUrl": node.get('artifactUrl') or node.get('downloadUrl'),
                    "description": node.get('description', ''),
                    "board": node.get('board'),
                    "gradeLevel": node.get('gradeLevel', [None])[0] if node.get('gradeLevel') else None,
                    "subject": node.get('subject', [None])[0] if node.get('subject') else None,
                    "organisation": node.get('organisation', [None])[0] if node.get('organisation') else None,
                    "chapter_name": chapter_name # Propagate the detected chapter name
                })

        for child in data.get('children', []):
            traverse(child, data.get('identifier'))

        collection_meta['resources'] = resources
        collection_meta['units'] = units
        return collection_meta

    def _map_diksha_hierarchy_fallback(self, data: Dict[str, Any], client) -> Dict[str, Any]:
        # Implementation for when hierarchy API is unavailable
        # (Similar to previousTurn logic but improved to handle potential flat leafNodes)
        # For brevity, reusing the existing flat mapper if hierarchy fails
        collection_meta = self._map_diksha_collection_header(data)
        children = data.get('children', [])
        leaf_nodes = data.get('leafNodes', [])
        if children:
            collection_meta['resources'] = self._map_recursive_children(children, parent_id=data.get('identifier'))
        elif leaf_nodes:
            # We would need to fetch leaf nodes metadata, but without hierarchy we lose chapter mapping
            # This is why we prefer the hierarchy API.
            pass
        return collection_meta

    async def _fetch_leaf_nodes_bulk(self, client: httpx.AsyncClient, identifiers: List[str], parent_id: str) -> List[Dict[str, Any]]:
        """Fetches metadata for multiple leaf nodes using Search API in chunks."""
        all_resources = []
        chunk_size = 100 # Sunbird typical search limit

        for i in range(0, len(identifiers), chunk_size):
            chunk = identifiers[i:i + chunk_size]
            payload = {
                "request": {
                    "filters": {
                        "identifier": chunk,
                        "status": ["Live"]
                    },
                    "fields": ["name", "artifactUrl", "downloadUrl", "streamingUrl", "mimeType", "license", "description", "board", "gradeLevel", "subject", "organisation"],
                    "limit": chunk_size
                }
            }
            try:
                resp = await client.post(self.SEARCH_URL, json=payload, timeout=20.0)
                if resp.status_code == 200:
                    contents = resp.json().get('result', {}).get('content', [])
                    all_resources.extend([
                        {
                            "id": c.get('identifier'),
                            "original_id": c.get('identifier'),
                            "parent_id": parent_id,
                            "title": c.get('name'),
                            "type": self._map_mime_to_type(c.get('mimeType')),
                            "license": c.get('license'),
                            "url": f"https://diksha.gov.in/play/content/{c.get('identifier')}",
                            "downloadUrl": c.get('artifactUrl') or c.get('downloadUrl'),
                            "description": c.get('description', ''),
                            "board": c.get('board'),
                            "gradeLevel": c.get('gradeLevel', [None])[0] if c.get('gradeLevel') else None,
                            "subject": c.get('subject', [None])[0] if c.get('subject') else None,
                            "organisation": c.get('organisation', [None])[0] if c.get('organisation') else None
                        }
                        for c in contents
                    ])
            except Exception as e:
                logger.error(f"Leaf node bulk fetch chunk failed: {e}")

        return all_resources

    async def resolve_live_resource(self, resource_id: str) -> Dict[str, Any]:
        """Resolves potentially stale IDs using search."""
        payload = {
            "request": {
                "filters": {
                    "identifier": [resource_id],
                    "status": ["Live", "Unlisted"]
                }
            }
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(self.SEARCH_URL, json=payload)
            if resp.status_code == 200:
                content_list = resp.json().get('result', {}).get('content', [])
                if content_list:
                    return self._map_single_resource(content_list[0])

        return {"error": "Resource not found", "id": resource_id}

    async def resolve_asset(self, resource_id: str) -> Dict[str, Any]:
        meta = await self.resolve_live_resource(resource_id)
        if "error" in meta: return meta
        return {
            "resource_id": resource_id,
            "download_url": meta.get('downloadUrl'),
            "streaming_url": meta.get('streamingUrl'),
            "artifact_url": meta.get('artifactUrl'),
            "mime_type": meta.get('mimeType')
        }

    def _map_diksha_collection_header(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "collectionId": data.get('identifier'),
            "title": data.get('name'),
            "publisher": data.get('publisher'),
            "organization": data.get('organisation', [None])[0] if data.get('organisation') else None,
            "board": data.get('board'),
            "class": data.get('gradeLevel', [None])[0] if data.get('gradeLevel') else None,
            "subject": data.get('subject', [None])[0] if data.get('subject') else None,
            "medium": data.get('medium', [None])[0] if data.get('medium') else None,
            "description": data.get('description', '')
        }

    def _map_recursive_children(self, children: List[Dict[str, Any]], parent_id: str) -> List[Dict[str, Any]]:
        resources = []
        for child in children:
            if child.get('mimeType') == 'application/vnd.ekstep.content-collection':
                resources.extend(self._map_recursive_children(child.get('children', []), parent_id=child.get('identifier')))
            else:
                resources.append({
                    "id": child.get('identifier'),
                    "original_id": child.get('identifier'),
                    "parent_id": parent_id,
                    "title": child.get('name'),
                    "type": self._map_mime_to_type(child.get('mimeType')),
                    "license": child.get('license'),
                    "url": f"https://diksha.gov.in/play/content/{child.get('identifier')}",
                    "downloadUrl": child.get('artifactUrl') or child.get('downloadUrl'),
                    "mimeType": child.get('mimeType')
                })
        return resources

    def _map_single_resource(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": data.get('identifier'),
            "title": data.get('name'),
            "license": data.get('license'),
            "downloadUrl": data.get('artifactUrl') or data.get('downloadUrl'),
            "streamingUrl": data.get('streamingUrl'),
            "mimeType": data.get('mimeType'),
            "artifactUrl": data.get('artifactUrl'),
            "description": data.get('description'),
            "board": data.get('board'),
            "gradeLevel": data.get('gradeLevel', [None])[0] if data.get('gradeLevel') else None,
            "subject": data.get('subject', [None])[0] if data.get('subject') else None
        }

    def _map_mime_to_type(self, mime: str) -> str:
        if not mime: return "DOCUMENT"
        if "video" in mime: return "VIDEO"
        if "pdf" in mime: return "PDF"
        if "epub" in mime: return "EPUB"
        if "html" in mime: return "INTERACTIVE"
        if "audio" in mime: return "AUDIO"
        return "DOCUMENT"
