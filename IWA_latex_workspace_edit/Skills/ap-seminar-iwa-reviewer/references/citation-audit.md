# Citation and Source Audit Guide

Use this guide when reviewing the student's citation table, Works Cited, References, or bibliography.

## Basic matching process

1. Extract all in-text citations or footnotes from the essay.
2. Extract every bibliography/reference entry.
3. Match in-text labels to bibliography labels.
4. Mark three categories:
   - Used and listed.
   - Cited in text but missing from bibliography.
   - Listed in bibliography but not clearly used in the essay.
5. Check whether stimulus materials are cited and listed.
6. Check whether quoted/paraphrased claims have attribution.

## Essential elements to check

Most entries should include enough information to identify the source:

- Author or organization.
- Title.
- Publication/container, journal, publisher, agency, website, or platform.
- Date or publication year.
- URL, DOI, database, page range, or access detail when relevant.

AP Seminar does not require MLA, APA, or Chicago specifically, but the style must be consistent and complete enough for tracking.

## Common Row 6 problems

- In-text citations use article titles while Works Cited is organized by author, making links hard to track.
- Works Cited has URLs only, with no author/title/date.
- Bibliography exists, but paragraphs use vague attribution such as "studies say" with no citation.
- Sources are listed in inconsistent styles with no organizational principle.
- Stimulus sources are cited in the essay but missing from Works Cited.
- The paper quotes statistics without page numbers, source names, or enough attribution.

## Common Row 5 source-quality issues

- Too many journalistic or advocacy sources for a research question that needs scholarly evidence.
- Overreliance on generic websites, dictionaries, encyclopedias, or blog posts.
- Scholarly sources exist but are used only for broad claims that do not support the argument's specific reasoning.
- Old sources are used for fast-changing topics without explaining why older evidence remains valid.
- Credibility is asserted by saying "this is credible because..." rather than integrated through source context, credentials, publication type, method, or relevance.

## Helpful source categories

- Strong academic: peer-reviewed journal article, scholarly book, academic press, credentialed researcher with field-relevant publication.
- Strong institutional: government report, reputable NGO/IGO report, official statistical dataset, major professional organization.
- Useful but needs support: high-quality journalism, expert interview, reputable magazine, think tank report.
- Weak unless justified: blog, generic website, encyclopedia/dictionary, commercial content, unsourced infographic, social media post.

## Script helper

If the essay text is saved locally, run:

```bash
python scripts/citation_audit.py essay.txt
```

Use the output to speed up matching, then manually verify. The script cannot judge source credibility or catch every citation style.
