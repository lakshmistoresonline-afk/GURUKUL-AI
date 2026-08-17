from abc import ABC, abstractmethod
import re
from typing import Dict, Any, List, Optional
from ...models.resource import VerifiedResource, ReuseDecision

class BaseResourceProvider(ABC):
    """
    Abstract base class for production-scale authoritative educational resource providers.
    """

    @abstractmethod
    def get_source_id(self) -> str:
        """Return the unique identifier for this source (e.g. 'DIKSHA')."""
        pass

    @abstractmethod
    async def resolve_collection(self, collection_id: str) -> Dict[str, Any]:
        """Fetch and analyze metadata for a collection of resources, handling nesting."""
        pass

    @abstractmethod
    async def resolve_live_resource(self, resource_id: str) -> Dict[str, Any]:
        """Resolve a potentially stale ID to a live ID and fetch current metadata."""
        pass

    @abstractmethod
    async def resolve_asset(self, resource_id: str) -> Dict[str, Any]:
        """Obtain verified download/streaming URLs for an asset."""
        pass

    def determine_reuse_eligibility(self, metadata: Dict[str, Any]) -> ReuseDecision:
        """
        Logic-first license processing.
        Determines if a resource can be imported based on its license.
        """
        raw_license = str(metadata.get('license', '')).lower().strip()

        # Normalize: remove dashes, spaces, and dots
        norm = re.sub(r'[^a-z0-9]', '', raw_license)

        # Common open licenses
        open_patterns = ['ccby', 'ccbysa', 'creativecommonsattribution', 'publicdomain', 'governmentopenlicense']

        # Restricted patterns
        restricted_patterns = ['ccbync', 'ccbynd', 'copyrighted', 'allrightsreserved']

        if any(p in norm for p in open_patterns):
            if 'nc' in norm:
                return ReuseDecision.NEEDS_REVIEW
            return ReuseDecision.IMPORT_ALLOWED

        if any(p in norm for p in restricted_patterns) or 'copyright' in raw_license:
            return ReuseDecision.LINK_ONLY

        return ReuseDecision.UNKNOWN
