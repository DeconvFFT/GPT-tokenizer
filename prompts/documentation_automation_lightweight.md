You are an expert technical writer + software architect. 
Your job is to turn this Python codebase into a fully documented project 
with Sphinx + ReadTheDocs.

Scope
-----
- Language: Python only
- Audience: engineers & data scientists
- Docstring style: NumPy
- Build system: Sphinx (with napoleon, autosummary, myst-parser, viewcode, intersphinx)
- Hosting: ReadTheDocs with .readthedocs.yml v2
- CI/CD: GitHub Actions, fail on warnings (-W)

What to do
----------
1. Add or refine docstrings for all public classes/functions:
   - NumPy style with proper section formatting
   - Full type hints (parameters, returns, raises)
   - At least 1 runnable doctest-style example
   - Link to related functions in "See Also"
   - Include "Notes" and "References" sections where relevant

2. Generate Sphinx docs scaffold:
   - docs/conf.py (extensions: autodoc, autosummary, napoleon, myst_parser, viewcode, intersphinx, doctest, coverage, todo)
   - docs/index.rst with simplified, working navigation structure
   - docs/getting-started.md with installation + quickstart (using MyST Markdown)
   - docs/api/modules.rst for auto-generated API reference
   - .readthedocs.yml (v2, Python 3.11+, with required sphinx.configuration key)
   - docs/requirements.txt (sphinx, furo, myst-parser)
   - docs/Makefile with build commands

3. Generate GitHub Action `.github/workflows/docs.yml`:
   - Install dependencies + package
   - Run `sphinx-build -W -b html docs _build/html`
   - Upload built docs as artifact
   - Run doctests with `sphinx-build -b doctest`

4. Package configuration:
   - setup.py with proper metadata and extras_require
   - requirements-dev.txt with all development dependencies
   - pyproject.toml compatibility (if exists)

Constraints
-----------
- No theme or import fallbacks; assume clean Python package.
- No over-engineered monitoring scripts.
- Keep examples simple, realistic, and runnable.
- If API contracts are ambiguous, insert `# TODO(doc): clarify`.
- Output changes as diffs or full file content ready to commit.
- Avoid complex toctree structures that reference non-existent files.

Critical Learnings & Requirements
--------------------------------
1. **ReadTheDocs v2 Configuration**:
   - MUST include `sphinx.configuration: docs/conf.py` key
   - Python version under `build.tools.python`, not `python.version`
   - Use `requirements` under `python.install` for dependencies

2. **Sphinx Configuration**:
   - Avoid `sphinx_autodoc_typehints` extension (causes parsing errors)
   - Use built-in `sphinx.ext.typehints` instead
   - Set `html_static_path = ['_static']` but don't require the directory
   - Configure `napoleon_numpy_docstring = True` for NumPy style

3. **Documentation Structure**:
   - Start simple: only include files that actually exist
   - Use MyST Markdown for .md files (enables cross-references)
   - Keep toctree minimal and working
   - Avoid broken cross-references between non-existent files

4. **Docstring Formatting**:
   - Ensure proper spacing between sections
   - Use consistent underline lengths for titles
   - Include working doctest examples
   - Handle control characters and special cases properly

5. **Build Process**:
   - Test locally with `sphinx-build -b html` before CI
   - Use `-W` flag in CI but test without it locally first
   - Ensure all dependencies are in requirements files
   - Handle package installation properly in CI

6. **Common Pitfalls**:
   - Title underlines must match title length exactly
   - Don't reference non-existent documentation files
   - Avoid complex extension configurations initially
   - Test build process step by step

Deliverables
------------
- Updated source files with complete docstrings
- `docs/` folder scaffold (minimal, working structure)
- `.readthedocs.yml` config (v2 compliant)
- GitHub Action workflow
- setup.py and requirements files
- Local build verification

Quality Checklist
-----------------
- [ ] Documentation builds locally without errors
- [ ] All docstrings follow NumPy style consistently
- [ ] Examples are runnable and realistic
- [ ] Navigation structure is simple and functional
- [ ] ReadTheDocs configuration is v2 compliant
- [ ] CI/CD workflow builds successfully
- [ ] No broken cross-references or missing files
- [ ] Package installs and imports correctly
