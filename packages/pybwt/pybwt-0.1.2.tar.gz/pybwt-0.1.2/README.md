# PyBWT: A Burrows-Wheeler Transform Tool

PyBWT is a Python implementation of the **Burrows-Wheeler Transform (BWT)** for efficient text compression and pattern searching. It supports:
- **Constructing the BWT** of a given text.
- **Reversing the BWT** to recover an original text.
- **Efficient occurrence counting** using the FM-index (Backward Search).

## 📌 Features
✅ Compute the **Burrows-Wheeler Transform (BWT)** of a string.  
✅ **Invert the BWT** to recover the original text.  
✅ **Search for substrings** efficiently without reconstructing the original text.  
✅ Uses **suffix arrays** and **LF-mapping** for fast operations.  

---

## 🔧 Installation
Install the tool in a Python environment using the pip package-management system:
```bash
pip install pybwt
```

Import the tool into your file by
```bash
import pybwt
```
and start using!

---

## ⌨️ User Guide/Documentation
The tool is relatively simple at the moment and functions largely through the BWT_Container class.
For a simple example, please visit the project's git repo.
Additional documentation will be created shortly.