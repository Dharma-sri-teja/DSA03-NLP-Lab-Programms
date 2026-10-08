
import re

NAME_PATTERN = re.compile(r"^\s*Name\s*[:\-]\s*([A-Za-z.\s]+?)\s*$", re.MULTILINE | re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
MOBILE_PATTERN = re.compile(r"(?<!\d)(?:\+91[\s-]?|0)?([6-9]\d{9})(?!\d)")
SKILL_PATTERN = re.compile(r"\b(Python|Java|SQL|Machine\s+Learning|NLP)\b", re.IGNORECASE)
EXPERIENCE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b", re.IGNORECASE)
def extract_name(text):
    """Return candidate name from the 'Name:' line (fallback: first line)."""
    match = NAME_PATTERN.search(text)
    if match:
        return match.group(1).strip()
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    return first_line.strip() or "Not Found"


def extract_emails(text):
    return EMAIL_PATTERN.findall(text)


def extract_mobiles(text):
    return MOBILE_PATTERN.findall(text)


def extract_skills(text):
    """Return unique skills in a standard capitalisation."""
    found = {re.sub(r"\s+", " ", s).title() for s in SKILL_PATTERN.findall(text)}
    return sorted(s.upper() if s.lower() in ("sql", "nlp") else s for s in found)


def extract_experience(text):
    """Return the highest number of years mentioned in the resume."""
    years = [float(y) for y in EXPERIENCE_PATTERN.findall(text)]
    return max(years) if years else 0.0


def build_profile(text):
    """Create structured summary dictionary of one candidate."""
    emails = extract_emails(text)
    mobiles = extract_mobiles(text)
    return {
        "name": extract_name(text),
        "email": emails[0] if emails else "Not Found",
        "mobile": mobiles[0] if mobiles else "Not Found",
        "skills": extract_skills(text),
        "experience": extract_experience(text),
    }


def is_eligible(profile, min_exp=2):
    """Eligibility: minimum 2 years of experience AND Python skill."""
    return profile["experience"] >= min_exp and "Python" in profile["skills"]


def print_profile(profile, index):
    print(f"Candidate {index}")
    print("-" * 50)
    print(f"  Name       : {profile['name']}")
    print(f"  Email      : {profile['email']}")
    print(f"  Mobile     : {profile['mobile']}")
    print(f"  Skills     : {', '.join(profile['skills']) if profile['skills'] else 'None'}")
    print(f"  Experience : {profile['experience']:g} year(s)")
    print(f"  Eligible   : {'YES' if is_eligible(profile) else 'NO'}")
    print()


def section1_main():
    resumes = [
        """Name: Arjun Kumar
Email: arjun.kumar@gmail.com
Phone: +91 9876543210
Skills: Python, SQL, Machine Learning
Experience: 3 years as Data Analyst at TCS""",
        """Name: Priya Sharma
Email: priya_sharma@outlook.com
Mobile: 8123456789
Skills: Java, SQL, nlp
Experience: 4 years in backend development""",
        """Name: Rahul Verma
Email: rahul.verma@yahoo.in
Contact: 9000012345
Skills: python, Machine Learning, NLP
Experience: 1 year internship in AI""",
        """Name: Sneha Reddy
Email: sneha.reddy@company.co.in
Contact No: +91-7012345678
Skills: Python, Java, NLP, SQL
Experience: 2.5 years as ML Engineer""",
    ]

    print("=" * 50)
    print("     RESUME INFORMATION EXTRACTION SYSTEM")
    print("=" * 50, "\n")

    profiles = []
    for i, resume in enumerate(resumes, start=1):
        try:
            profile = build_profile(resume)
            profiles.append(profile)
            print_profile(profile, i)
        except Exception as error:  # basic error handling
            print(f"Error processing resume {i}: {error}")

    print("=" * 50)
    print("  SHORTLISTED CANDIDATES (>= 2 yrs & Python)")
    print("=" * 50)
    shortlisted = [p for p in profiles if is_eligible(p)]
    if shortlisted:
        for p in shortlisted:
            print(f"  * {p['name']:<15} | {p['experience']:g} yrs | {p['email']}")
    else:
        print("  No candidate satisfies the criteria.")
    print(f"\nTotal resumes: {len(profiles)} | Shortlisted: {len(shortlisted)}")


# ======================================================================
# SECTION 2: PRODUCT SEARCH SYSTEM
# ======================================================================

PRODUCTS = [
    "Apple iPhone 14", "Samsung Galaxy Phone", "Wireless Mouse",
    "Gaming Laptop", "Laptop Bag", "Bluetooth Headphones",
    "Headphone Stand", "Smart Watch", "Phone Case", "Mouse Pad",
    "USB Keyboard", "Mechanical Keyboard", "Laptop Stand",
]


def build_pattern(keyword, mode):
    """Create a regex pattern according to the search type."""
    key = re.escape(keyword)
    patterns = {
        "exact":   rf"^{key}$",              # whole product name equals keyword
        "word":    rf"\b{key}\b",            # keyword as a complete word
        "prefix":  rf"\b{key}\w*",           # a word starting with keyword
        "suffix":  rf"\w*{key}\b",           # a word ending with keyword
        "partial": rf"{key}",                # keyword anywhere
    }
    return re.compile(patterns[mode], re.IGNORECASE)   # case-insensitive


def search(products, keyword, mode):
    pattern = build_pattern(keyword, mode)
    return [p for p in products if pattern.search(p)]


def run_search(products, keyword, mode, title, report):
    results = search(products, keyword, mode)
    print(f"[{title}]  keyword = '{keyword}'")
    if results:
        for r in results:
            print(f"   - {r}")
    else:
        print("   No matching products found.")
    print(f"   Matches: {len(results)}\n")
    report.append((title, keyword, len(results)))


def section2_main():
    print("=" * 55)
    print("           PRODUCT SEARCH SYSTEM (REGEX)")
    print("=" * 55)
    print("Product Catalogue:")
    for i, p in enumerate(PRODUCTS, start=1):
        print(f"  {i:>2}. {p}")
    print()

    report = []
    run_search(PRODUCTS, "Gaming Laptop", "exact",   "1. Exact Keyword Search", report)
    run_search(PRODUCTS, "Head",          "prefix",  "2. Prefix Search", report)
    run_search(PRODUCTS, "board",         "suffix",  "3. Suffix Search", report)
    run_search(PRODUCTS, "top",           "partial", "4. Partial Keyword Search", report)
    run_search(PRODUCTS, "LAPTOP",        "word",    "5. Case-Insensitive Search", report)
    run_search(PRODUCTS, "tablet",        "partial", "6. Search With No Result", report)

    print("=" * 55)
    print("              SEARCH SUMMARY REPORT")
    print("=" * 55)
    print(f"{'Search Type':<30}{'Keyword':<16}{'Matches':>8}")
    print("-" * 55)
    for title, keyword, count in report:
        print(f"{title:<30}{keyword:<16}{count:>8}")
    print("-" * 55)
    print(f"{'Total matching products':<46}{sum(c for _, _, c in report):>9}")


# ======================================================================
# SECTION 3: UNIVERSITY REGISTRATION VALIDATION SYSTEM
# ======================================================================

# ---------- Validation rules (regex) ----------
RULES = {
    "Register Number": (re.compile(r"^19\d{7}$"),
                        "9 digits starting with 19 (e.g. 192425269)"),
    "Email":           (re.compile(r"^[A-Za-z0-9._]+@(?:saveetha\.com|simats\.edu\.in)$"),
                        "must end with @saveetha.com or @simats.edu.in"),
    "Course Code":     (re.compile(r"^[A-Z]{3}\d{2,4}$"),
                        "3 capital letters + 2-4 digits (e.g. DSA03, ITA0405)"),
    "Semester":        (re.compile(r"^(?:Sem(?:ester)?\s*)?[1-8]$", re.IGNORECASE),
                        "number 1-8 (e.g. 4 or Semester 4)"),
    "Mobile Number":   (re.compile(r"^(?:\+91[\s-]?)?[6-9]\d{9}$"),
                        "10 digits starting with 6-9, optional +91"),
}


def validate_field(field, value):
    pattern, hint = RULES[field]
    if pattern.fullmatch(value.strip()):
        return True, f"VALID   - {field}: {value}"
    return False, f"INVALID - {field}: '{value}' ({hint})"


def validate_student(student):
    """Validate all fields of one student and print the registration report."""
    print(f"Student: {student.get('Name', 'Unknown')}")
    print("-" * 60)
    all_valid = True
    for field in RULES:
        try:
            ok, message = validate_field(field, student.get(field, ""))
        except Exception as error:
            ok, message = False, f"ERROR   - {field}: {error}"
        print("  " + message)
        all_valid &= ok
    status = "REGISTRATION SUCCESSFUL" if all_valid else "REGISTRATION FAILED"
    print(f"\n  >>> FINAL STATUS: {status}\n")
    return all_valid


def section3_main():
    students = [
        {"Name": "M.Dharma Sri Teja", "Register Number": "192425269",
         "Email": "192425269.sse@saveetha.com", "Course Code": "DSA03",
         "Semester": "4", "Mobile Number": "+91 9876543210"},
        {"Name": "Test Case 2 (all invalid)", "Register Number": "29242526",
         "Email": "student@gmail.com", "Course Code": "dsa3",
         "Semester": "9", "Mobile Number": "5123456789"},
        {"Name": "Test Case 3 (one invalid)", "Register Number": "192425270",
         "Email": "ravi.k@simats.edu.in", "Course Code": "ITA0405",
         "Semester": "Semester 6", "Mobile Number": "98765432"},
    ]

    print("=" * 60)
    print("     UNIVERSITY REGISTRATION VALIDATION SYSTEM")
    print("=" * 60, "\n")
    results = [validate_student(s) for s in students]
    print("=" * 60)
    print(f"Total: {len(results)} | Successful: {sum(results)} | Failed: {len(results) - sum(results)}")


# ======================================================================
# RUN ALL SECTIONS
# ======================================================================


if __name__ == "__main__":
    section1_main()
    print("\n\n")
    section2_main()
    print("\n\n")
    section3_main()
