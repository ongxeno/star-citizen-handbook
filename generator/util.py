from pathlib import Path
from typing import Tuple
from constants import MAIN_CATEGORIES

def ensure_new_article_structure(article_path: Path) -> Tuple[Path, Path]:
    """
    If the article is directly under a main category, move it into a subfolder named after the file (without .md),
    rename to index.md, and return the new article path and output dir.
    Otherwise, return the original article path and its parent.
    """
    parent_folder = article_path.parent
    article_name = article_path.stem
    if parent_folder.name in MAIN_CATEGORIES and article_path.name != "index.md":
        new_folder = parent_folder / article_name
        new_folder.mkdir(parents=True, exist_ok=True)
        new_article_path = new_folder / "index.md"
        article_path.replace(new_article_path)
        print(f"Moved article to {new_article_path}")
        return new_article_path, new_folder
    else:
        return article_path, article_path.parent
