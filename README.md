# Job Application Tracker & ATS Analysis System

A professional, end-to-end **Job Application Tracking system** with a **real ATS-style resume analyzer**, built using Flask and pure HTML/CSS.

This project helps users track job applications, analyze resumes against job descriptions, and monitor application progress through a clean dashboard.

---

## � Documentation

**For detailed documentation, guides, and implementation details, see the [/docs](/docs) folder:**

- 🚀 **Getting Started:** [START_HERE.md](/docs/START_HERE.md)
- 📖 **Documentation Index:** [DOCUMENTATION_GUIDE.md](/docs/DOCUMENTATION_GUIDE.md)
- 💼 **Recruiter Talking Points:** [RECRUITER_TALKING_POINTS.md](/docs/RECRUITER_TALKING_POINTS.md)
- ⚙️ **Implementation Details:** [IMPLEMENTATION_DETAILS.md](/docs/IMPLEMENTATION_DETAILS.md)
- 🎨 **Design System:** [DESIGN_SYSTEM_OVERVIEW.md](/docs/DESIGN_SYSTEM_OVERVIEW.md)

---

## �🚀 Features

- Add and manage job applications (company, role, status)
- Job-specific ATS resume analysis
- Resume vs Job Description keyword matching
- ATS match percentage with missing keywords
- Application status tracking (Applied, Interview, Rejected)
- Clean, corporate HR-style UI
- Glassmorphism-based modern design
- Responsive design (desktop & mobile)

---

## 🧠 How the ATS Works

1. User adds a job with company name, role, and job description  
2. User uploads a resume and selects the job  
3. The system:
   - Extracts resume text
   - Extracts keywords from the job description
   - Matches resume keywords against the job description
4. Displays:
   - ATS match percentage
   - Matched keywords
   - Missing keywords
5. Dashboard shows ATS score and application status per job

This follows **real-world ATS logic** (job-based, not fixed skills).

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS (Pure CSS, no frameworks)
- **Backend:** Python (Flask)
- **Database:** SQLite
- **Design:** Corporate HR UI + Glassmorphism

---

## 📂 Project Structure

