"""
Job Tracker Application with ATS System
========================================
This Flask app helps users track job applications and analyze resume ATS match
for each specific job posting.

Features:
- Add jobs with company name, role, job description, and status
- Upload resume and analyze ATS match against specific job descriptions
- Dashboard shows all jobs with their ATS scores
- Job-specific keyword extraction and matching (no predefined skills list)
"""

from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os
from datetime import datetime
from PyPDF2 import PdfReader
import re

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def get_db():
    """Get database connection with row factory for easier data access"""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """
    Initialize the database with the required tables.
    Called once on first run.
    
    Table: jobs
    - id: Unique job identifier
    - company: Company name
    - role: Job position/title
    - job_description: Full job posting text (for keyword extraction)
    - status: Applied, Interview, or Rejected
    - ats_score: ATS match percentage (0-100), NULL if not analyzed yet
    - date_added: Timestamp when job was added
    - date_applied: Date when application was submitted
    - interview_date: Optional date of scheduled interview
    - notes: Optional notes or comments about the application
    """
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            job_description TEXT,
            status TEXT DEFAULT 'Applied',
            ats_score INTEGER,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_applied TEXT,
            interview_date TEXT,
            notes TEXT
        )
    """)
    
    # Add new columns to existing table if they don't exist (backward compatibility)
    try:
        cur.execute("ALTER TABLE jobs ADD COLUMN date_applied TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cur.execute("ALTER TABLE jobs ADD COLUMN interview_date TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cur.execute("ALTER TABLE jobs ADD COLUMN notes TEXT")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()


# Initialize database on startup
init_db()

# ============================================================
# KEYWORD EXTRACTION & ATS MATCHING LOGIC
# ============================================================

def extract_keywords(text, min_length=3):
    """
    Extract meaningful keywords from text using simple frequency analysis.
    
    Strategy:
    1. Convert to lowercase and remove special characters
    2. Split into words
    3. Filter out common words (stop words)
    4. Keep words of length >= min_length
    5. Return sorted by frequency
    
    Args:
        text (str): Text to extract keywords from
        min_length (int): Minimum word length to consider (default 3)
    
    Returns:
        list: Keywords sorted by frequency (most common first)
    """
    
    # Common English words to ignore
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'as', 'is', 'are', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'your',
        'our', 'their', 'what', 'which', 'who', 'when', 'where', 'why', 'how',
        'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
        'any', 'much', 'many', 'only', 'own', 'same', 'so', 'than', 'too',
        'very', 'just', 'such', 'no', 'not', 'nor', 'also', 'if', 'because',
        'if', 'as', 'while', 'although', 'after', 'before', 'during', 'through',
        'between', 'within', 'without', 'job', 'position', 'role', 'experience'
    }
    
    # Convert to lowercase and remove special characters
    text = text.lower()
    # Replace common punctuation with spaces
    text = re.sub(r'[^a-z0-9\s\+\#\.]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter words: remove stop words, keep meaningful ones
    keywords = [
        word for word in words 
        if len(word) >= min_length and word not in stop_words
    ]
    
    # Count frequency and return sorted by count
    from collections import Counter
    word_freq = Counter(keywords)
    
    # Return top keywords (limit to 50 to avoid noise)
    top_keywords = [word for word, count in word_freq.most_common(50)]
    
    return top_keywords


def calculate_ats_score(resume_text, job_description):
    """
    Calculate ATS match score between resume and job description.
    
    Algorithm:
    1. Extract keywords from job description (what the job wants)
    2. Extract keywords from resume (what the candidate has)
    3. Count matches between them
    4. Return percentage: (matches / job keywords) * 100
    
    Args:
        resume_text (str): Full text extracted from resume PDF
        job_description (str): Full job posting text
    
    Returns:
        tuple: (match_percentage, matched_keywords, missing_keywords)
        - match_percentage: 0-100 score
        - matched_keywords: List of keywords found in both
        - missing_keywords: Keywords in job description but not resume
    """
    
    if not resume_text or not job_description:
        return 0, [], []
    
    # Extract keywords from both texts
    job_keywords = set(extract_keywords(job_description))
    resume_keywords = set(extract_keywords(resume_text))
    
    # Find matches and misses
    matched = list(job_keywords & resume_keywords)  # Intersection
    missing = list(job_keywords - resume_keywords)  # In job but not resume
    
    # Calculate percentage
    total_job_keywords = len(job_keywords)
    if total_job_keywords == 0:
        match_percentage = 0
    else:
        match_percentage = int((len(matched) / total_job_keywords) * 100)
    
    # Sort for consistent display
    matched.sort()
    missing.sort()
    
    return match_percentage, matched, missing


def get_resume_improvement_suggestions(match_score, missing_keywords_count, missing_keywords):
    """
    Generate actionable improvement suggestions based on ATS analysis.
    
    Args:
        match_score (int): ATS match percentage (0-100)
        missing_keywords_count (int): Number of missing keywords
        missing_keywords (list): List of actual missing keywords
    
    Returns:
        dict: {
            'score_level': 'excellent'|'good'|'needs_improvement',
            'main_message': str,
            'priority_actions': [list of actionable suggestions],
            'quick_wins': [list of easy improvements]
        }
    """
    
    suggestions = {
        'excellent': {
            'score_level': 'excellent',
            'main_message': 'Your resume is a strong match for this position!',
            'priority_actions': [
                'Your resume covers most key requirements—apply with confidence',
                'Consider highlighting achievements that align with job requirements'
            ],
            'quick_wins': [
                'Quantify your accomplishments where possible',
                'Ensure your skills section is visible and up-to-date'
            ]
        },
        'good': {
            'score_level': 'good',
            'main_message': 'Your resume is a good match with room for improvement.',
            'priority_actions': [
                f'Add the {missing_keywords_count} missing keywords to your resume',
                'Update your experience descriptions to include industry-specific terms',
                'Create a dedicated skills section highlighting technical abilities'
            ],
            'quick_wins': [
                'Use keywords from the job description in your resume',
                'Tailor your professional summary for this specific role',
                'Add quantifiable results to your job descriptions'
            ]
        },
        'needs_improvement': {
            'score_level': 'needs_improvement',
            'main_message': 'Your resume needs updates to better match this position.',
            'priority_actions': [
                f'Add {missing_keywords_count} missing keywords to your resume',
                'Reorganize your resume to highlight relevant experience first',
                'Expand your skills section with technical and soft skills',
                'Consider this role may not be the best fit with your current background'
            ],
            'quick_wins': [
                f'Start by adding these top keywords: {", ".join(missing_keywords[:5]) if missing_keywords else "industry skills"}',
                'Reorder your experience to lead with most relevant roles',
                'Add metrics and achievements to your job descriptions',
                'Use the same terminology as the job posting'
            ]
        }
    }
    
    if match_score >= 80:
        return suggestions['excellent']
    elif match_score >= 60:
        return suggestions['good']
    else:
        return suggestions['needs_improvement']


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    """Home page - shows overview and navigation"""
    return render_template("index.html")


@app.route("/add-job", methods=["GET", "POST"])
def add_job():
    """
    Add Job Route
    
    GET: Display form for adding a new job
    POST: Save job with company name, role, description, status, and optional dates
    
    Important: Job description is stored for ATS analysis later.
    """
    if request.method == "POST":
        # Get form data
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        job_description = request.form.get("job_description", "").strip()
        status = request.form.get("status", "Applied")
        date_applied = request.form.get("date_applied", "").strip()
        interview_date = request.form.get("interview_date", "").strip()
        notes = request.form.get("notes", "").strip()
        
        # Validate required fields
        errors = []
        if not company:
            errors.append("Company name is required")
        if not role:
            errors.append("Job role is required")
        if not job_description:
            errors.append("Job description is required for ATS analysis")
        
        if errors:
            return render_template("add_job.html", errors=errors)
        
        # Save to database
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO jobs (company, role, job_description, status, date_applied, interview_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company, role, job_description, status, date_applied if date_applied else None, 
              interview_date if interview_date else None, notes if notes else None))
        
        conn.commit()
        conn.close()
        
        # Redirect to dashboard to see the new job
        return redirect("/dashboard")
    
    # GET request - show the form
    return render_template("add_job.html")


@app.route("/dashboard")
def dashboard():
    """
    Dashboard Route
    
    Shows:
    - Summary cards: Total, Applied, Interview, Rejected counts
    - Table with all jobs:
      - Company name
      - Job role
      - Application status
      - ATS match percentage (if analyzed)
    """
    conn = get_db()
    cur = conn.cursor()
    
    # Get all jobs from database
    cur.execute("SELECT * FROM jobs ORDER BY date_added DESC")
    jobs = cur.fetchall()
    
    # Get count statistics
    cur.execute("SELECT COUNT(*) FROM jobs")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM jobs WHERE status='Applied'")
    applied = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM jobs WHERE status='Interview'")
    interview = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM jobs WHERE status='Rejected'")
    rejected = cur.fetchone()[0]
    
    conn.close()
    
    return render_template(
        "dashboard.html",
        jobs=jobs,
        total=total,
        applied=applied,
        interview=interview,
        rejected=rejected
    )


@app.route("/edit-job", methods=["GET", "POST"])
def edit_job():
    """
    Edit Job Route
    
    GET: Display form pre-filled with job details
    POST: Update job with new information (status, dates, notes, etc.)
    
    Does NOT require resume re-upload; uses existing ATS score
    """
    job_id = request.args.get("job_id") or request.form.get("job_id")
    
    if not job_id:
        return redirect("/dashboard")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cur.fetchone()
    conn.close()
    
    if not job:
        return redirect("/dashboard")
    
    if request.method == "POST":
        # Get form data
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        job_description = request.form.get("job_description", "").strip()
        status = request.form.get("status", "Applied")
        date_applied = request.form.get("date_applied", "").strip()
        interview_date = request.form.get("interview_date", "").strip()
        notes = request.form.get("notes", "").strip()
        
        # Validate required fields
        errors = []
        if not company:
            errors.append("Company name is required")
        if not role:
            errors.append("Job role is required")
        
        if errors:
            return render_template("edit_job.html", job=job, errors=errors)
        
        # Update database
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE jobs 
            SET company=?, role=?, job_description=?, status=?, date_applied=?, interview_date=?, notes=?
            WHERE id=?
        """, (company, role, job_description, status, 
              date_applied if date_applied else None, 
              interview_date if interview_date else None, 
              notes if notes else None, 
              job_id))
        
        conn.commit()
        conn.close()
        
        return redirect("/dashboard")
    
    # GET request - show the form with pre-filled data
    return render_template("edit_job.html", job=job)


@app.route("/export-results/<int:job_id>")
def export_results(job_id):
    """
    Export ATS analysis results as a professional text report.
    
    Generates a summary including:
    - Job and company details
    - ATS match score with interpretation
    - Matched keywords
    - Missing keywords
    - Actionable improvement suggestions
    """
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cur.fetchone()
    conn.close()
    
    if not job:
        return "Job not found", 404
    
    # Check if ATS analysis was done
    if job['ats_score'] is None:
        return "This job has not been analyzed yet. Please upload a resume first.", 400
    
    # Re-generate improvement suggestions for the report
    improvement_suggestions = get_resume_improvement_suggestions(
        job['ats_score'],
        0,  # Will be calculated from matched/missing
        []
    )
    
    # Build professional report text
    report = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    ATS COMPATIBILITY ANALYSIS REPORT                       ║
╚════════════════════════════════════════════════════════════════════════════╝

POSITION DETAILS
─────────────────────────────────────────────────────────────────────────────
Company:                {job['company']}
Position:               {job['role']}
Date Applied:          {job['date_applied'] if job['date_applied'] else 'Not specified'}
Application Status:    {job['status']}

ATS MATCH SCORE
─────────────────────────────────────────────────────────────────────────────
Score:                 {job['ats_score']}%

Score Interpretation:
  • 80-100%:  EXCELLENT MATCH - Strong candidate, high priority application
  • 60-79%:   GOOD MATCH - Competitive candidate, consider targeted updates
  • Below 60%: NEEDS IMPROVEMENT - Critical gaps to address

Current Status:        {improvement_suggestions['main_message']}

RECOMMENDED ACTIONS
─────────────────────────────────────────────────────────────────────────────
Priority Actions:
"""
    
    for i, action in enumerate(improvement_suggestions['priority_actions'], 1):
        report += f"  {i}. {action}\n"
    
    report += "\nQuick Wins:\n"
    for i, win in enumerate(improvement_suggestions['quick_wins'], 1):
        report += f"  {i}. {win}\n"
    
    report += """
─────────────────────────────────────────────────────────────────────────────
Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

This report was generated by the Job Tracker Application.
For the best results, ensure your resume is:
  ✓ ATS-friendly with standard formatting
  ✓ Tailored to specific job requirements
  ✓ Using industry keywords and terminology
  ✓ Highlighting measurable achievements
"""
    
    # Return as downloadable text file
    from flask import make_response
    response = make_response(report)
    response.headers["Content-Disposition"] = f"attachment; filename=ATS_Analysis_{job['company']}.txt"
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():
    """
    Resume Upload & ATS Analysis Route
    
    GET: Show form to upload resume and select job to analyze
    POST: 
      1. Extract resume PDF text
      2. Get selected job's description
      3. Calculate ATS score
      4. Show matched and missing keywords
      5. Generate improvement suggestions
      6. Save score to database
    
    Workflow:
    - User selects which job to analyze against
    - Uploads resume PDF
    - System compares resume keywords with job keywords
    - ATS score is saved to that job's record
    - Improvement suggestions are provided
    """
    
    # Get all jobs for the dropdown
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, company, role, job_description FROM jobs ORDER BY date_added DESC")
    all_jobs = cur.fetchall()
    conn.close()
    
    # Default values
    resume_text = ""
    matched_keywords = []
    missing_keywords = []
    match_percent = 0
    selected_job = None
    analyzed_job_id = None
    improvement_suggestions = None
    
    if request.method == "POST":
        # Get uploaded file and selected job
        file = request.files.get("resume")
        job_id = request.form.get("job_id")
        
        # Validate inputs
        errors = []
        
        if not file or file.filename == "":
            errors.append("No file selected. Please choose a PDF file to upload.")
        elif not file.filename.endswith(".pdf"):
            errors.append("Invalid file type. Please upload a PDF file only.")
        
        if not job_id:
            errors.append("Please select a job to analyze.")
        
        if errors:
            return render_template(
                "resume.html",
                all_jobs=all_jobs,
                errors=errors
            )
        
        try:
            # Get the selected job's description first
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, company, role, job_description FROM jobs WHERE id = ?",
                (job_id,)
            )
            job = cur.fetchone()
            conn.close()
            
            if not job:
                errors.append("Selected job not found. Please choose a different job.")
                return render_template(
                    "resume.html",
                    all_jobs=all_jobs,
                    errors=errors
                )
            
            if not job['job_description'] or job['job_description'].strip() == "":
                errors.append("Job description is missing. Please edit the job and add a description.")
                return render_template(
                    "resume.html",
                    all_jobs=all_jobs,
                    errors=errors
                )
            
            selected_job = dict(job)
            analyzed_job_id = job_id
            
            # Save and extract PDF text
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            
            try:
                reader = PdfReader(filepath)
                if len(reader.pages) == 0:
                    errors.append("PDF file is empty. Please upload a valid resume PDF.")
                    return render_template(
                        "resume.html",
                        all_jobs=all_jobs,
                        errors=errors
                    )
                
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text
                
                if not resume_text or resume_text.strip() == "":
                    errors.append("Could not extract text from PDF. Please ensure your resume PDF contains readable text.")
                    return render_template(
                        "resume.html",
                        all_jobs=all_jobs,
                        errors=errors
                    )
            
            except Exception as pdf_error:
                errors.append(f"Error reading PDF file: {str(pdf_error)}")
                return render_template(
                    "resume.html",
                    all_jobs=all_jobs,
                    errors=errors
                )
            
            # Calculate ATS score
            match_percent, matched_keywords, missing_keywords = calculate_ats_score(
                resume_text,
                job['job_description']
            )
            
            # Generate improvement suggestions
            improvement_suggestions = get_resume_improvement_suggestions(
                match_percent,
                len(missing_keywords),
                missing_keywords
            )
            
            # Save ATS score to database
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "UPDATE jobs SET ats_score = ? WHERE id = ?",
                (match_percent, job_id)
            )
            conn.commit()
            conn.close()
            
        except Exception as e:
            errors.append(f"An unexpected error occurred: {str(e)}")
            return render_template(
                "resume.html",
                all_jobs=all_jobs,
                errors=errors
            )
    
    return render_template(
        "resume.html",
        all_jobs=all_jobs,
        resume_text=resume_text,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        match_percent=match_percent,
        selected_job=selected_job,
        analyzed_job_id=analyzed_job_id,
        improvement_suggestions=improvement_suggestions
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template("error.html", error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template("error.html", error="Server error"), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
