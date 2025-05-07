from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class ArxivSearchResult:
    """Represents a processed search result from ArXiv."""
    title: str
    published_date: str  # Store as string e.g., "YYYY-MM-DD"
    summary: str
    arxiv_id: str # e.g., "1703.06870v1"
    authors: List[str] = field(default_factory=list)
    pdf_url: Optional[str] = None
    full_text: Optional[str] = None
    processing_error: Optional[str] = None # To capture any errors during PDF download/parsing for this item

    def __str__(self) -> str:
        """Returns a string representation of the ArxivSearchResult object."""
        authors_str = ", ".join(self.authors) if self.authors else "N/A"
        text_preview = (self.full_text[:200] + "..." if self.full_text and len(self.full_text) > 200 else self.full_text) or "N/A"
        
        lines = [
            f"Title: {self.title}",
            f"Authors: {authors_str}",
            f"Published: {self.published_date}",
            f"ArXiv ID: {self.arxiv_id}",
            f"PDF URL: {self.pdf_url or 'N/A'}",
            f"Summary: {self.summary}",
            f"Full Text Preview: {text_preview}",
        ]
        if self.processing_error:
            lines.append(f"Processing Error: {self.processing_error}")
        return "\n".join(lines)