import difflib
from typing import List, Tuple, Optional

class ParagraphAligner:
    """
    Aligns paragraph lists from old and new documents using LCS / SequenceMatcher.
    Prevents off-by-one misalignment when paragraphs are added or removed.
    """
    
    @staticmethod
    def align_paragraphs(old_texts: List[str], new_texts: List[str]) -> List[Tuple[str, Optional[int], Optional[int]]]:
        """
        Returns a list of tuples: (op_tag, old_idx, new_idx)
        op_tag can be:
          - 'equal': paragraph unchanged or updated, match old_idx to new_idx
          - 'insert': paragraph exists only in new document (old_idx is None)
          - 'delete': paragraph exists only in old document (new_idx is None)
          - 'replace': paragraph replaced
        """
        matcher = difflib.SequenceMatcher(None, old_texts, new_texts)
        aligned_pairs: List[Tuple[str, Optional[int], Optional[int]]] = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for old_i, new_j in zip(range(i1, i2), range(j1, j2)):
                    aligned_pairs.append(('equal', old_i, new_j))
            elif tag == 'insert':
                for new_j in range(j1, j2):
                    aligned_pairs.append(('insert', None, new_j))
            elif tag == 'delete':
                for old_i in range(i1, i2):
                    aligned_pairs.append(('delete', old_i, None))
            elif tag == 'replace':
                # Match old and new paragraphs by highest similarity ratio (> 0.4)
                old_indices = list(range(i1, i2))
                new_indices = list(range(j1, j2))
                
                matched_old = set()
                matched_new = set()

                for o_idx in old_indices:
                    best_match = None
                    best_ratio = 0.4  # minimum threshold to pair paragraphs
                    for n_idx in new_indices:
                        if n_idx in matched_new:
                            continue
                        ratio = difflib.SequenceMatcher(None, old_texts[o_idx], new_texts[n_idx]).ratio()
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_match = n_idx

                    if best_match is not None:
                        aligned_pairs.append(('replace', o_idx, best_match))
                        matched_old.add(o_idx)
                        matched_new.add(best_match)

                for o_idx in old_indices:
                    if o_idx not in matched_old:
                        aligned_pairs.append(('delete', o_idx, None))

                for n_idx in new_indices:
                    if n_idx not in matched_new:
                        aligned_pairs.append(('insert', None, n_idx))

                        
        return aligned_pairs
