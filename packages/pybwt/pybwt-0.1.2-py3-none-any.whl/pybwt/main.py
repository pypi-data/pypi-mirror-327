import bisect
from collections import defaultdict
from .bwt_utils import construct_BWT

class BWT_Container:
    def __init__(self, input, is_bwt=False):
        """
        Initialize a BWT_Container.
        
        s[str]: Original string or precomputed BWT
        is_bwt[bool]: If True, 's' is already a BWT and needs decoding
        """
        if is_bwt:
            self.bwt = input
            self.original_text = None
            self.first_occurrence, self.occ_counts = self._precompute_bwt_data()
        else:
            self.original_text = input
            self.bwt = None

    def get_BWT(self):
        if self.bwt is None:
            raise ValueError("BWT has not been computed yet.")
        return self.bwt
    
    def decode_BWT(self):
        """Invert (decode) the BWT string using cached precomputed data"""
        if self.original_text is not None:
            return self.original_text
        if self.bwt is None:
            raise ValueError("BWT has not been computed yet.")
        decoded = self._invert_BWT(self.bwt, use_cached=True)
        self.original_text = decoded
        return decoded
    
    def encode_BWT(self):
        if self.bwt is not None:
            return self.bwt
        if self.original_text is None:
            raise ValueError("Original text has not been set.")
        encoded = construct_BWT(self.original_text)
        self.bwt = encoded
        self.first_occurrence, self.occ_counts = self._precompute_bwt_data()
        return encoded

    def _invert_BWT(self, bwt, use_cached=False):
        """
        Invert (decode) the BWT string, assuming a single '$' sentinel exists.
        
        bwt[str]: BWT string to invert
        use_cached[bool]: If True, use precomputed first_occurrence & occ_counts
        """
        if not isinstance(bwt, str):
            raise ValueError("The input to this function must be a string. \
                             If attempting to invert a BWT_Container object, use the \
                             'decode_BWT' method instead.")

        n = len(bwt)

        if use_cached:
            first_occurrence, occ_counts = self.first_occurrence, self.occ_counts
        else:
            first_occurrence, occ_counts = BWT_Container._precompute_bwt_data_static(bwt)

        LF = [0] * n
        occ_tracker = defaultdict(int)
        for i, c in enumerate(bwt):
            LF[i] = first_occurrence[c] + occ_tracker[c]
            occ_tracker[c] += 1

        sentinel_index = bwt.index('$')

        i = sentinel_index
        original_reversed = []
        for _ in range(n - 1):
            i = LF[i]
            original_reversed.append(bwt[i])

        return "".join(reversed(original_reversed))

    def _precompute_bwt_data(self):
        return self._precompute_bwt_data_static(self.bwt)

    @staticmethod
    def _precompute_bwt_data_static(bwt):
        """
        Static version of _precompute_bwt_data()
        """
        freq = defaultdict(int)
        for c in bwt:
            freq[c] += 1

        first_occurrence = BWT_Container._compute_first_occurrence(freq)

        occ_counts = defaultdict(list)
        for i, c in enumerate(bwt):
            occ_counts[c].append(i)

        return first_occurrence, occ_counts

    @staticmethod
    def _compute_first_occurrence(freq):
        """
        Compute first occurrence array (C array) from character frequency dictionary.
        """
        sorted_chars = sorted(freq.keys())
        first_occurrence = {}
        total = 0
        for c in sorted_chars:
            first_occurrence[c] = total
            total += freq[c]
        return first_occurrence

    def _rank_of(self, i, c):
        """
        Compute how many times character 'c' appears in bwt[0..i].
        Uses binary search over occ_counts[c].
        """
        if c not in self.occ_counts:
            return 0
        return bisect.bisect_right(self.occ_counts[c], i)

    def count_occurrences(self, pattern):
        """
        Counts the occurrences of the string 'pattern' in the BWT's original string using backward search.
        """
        if self.bwt is None:
            raise ValueError("BWT has not been computed yet.")
        
        top = 0
        bottom = len(self.bwt) - 1

        for i in range(len(pattern) - 1, -1, -1):
            c = pattern[i]
            if c not in self.first_occurrence:
                return 0, None

            top_rank = self._rank_of(top - 1, c)
            bottom_rank = self._rank_of(bottom, c)

            count = bottom_rank - top_rank
            if count == 0:
                return 0, None

            top = self.first_occurrence[c] + top_rank
            bottom = self.first_occurrence[c] + bottom_rank - 1

        return bottom - top + 1

    def __str__(self):
        return ("BWT_Container object: BWT = {}".format(self.bwt) if self.bwt else "") + \
               ("\nOriginal text = {}".format(self.original_text) if self.original_text else "")
