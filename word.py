from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_modern_clean_template(output_path, user_data):
    doc = Document()

    # Name (Big Font, Centered)
    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = name.add_run(user_data.get("Full Name", ""))
    run.font.size = Pt(18)
    run.bold = True

    # Contact Info (Smaller Font, Centered)
    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = contact.add_run(
        f"{user_data.get('Address', '')} | {user_data.get('Phone', '')} | {user_data.get('Email', '')} | {user_data.get('LinkedIn', '')} | {user_data.get('GitHub', '')}"
    )
    run.font.size = Pt(10)
    font = run.font
    font.color.rgb = RGBColor(100, 100, 100)  # Light Gray

    # Add spacing
    doc.add_paragraph()

    # Professional Summary
    add_section(doc, "Professional Summary", user_data.get("Professional Summary", ""))

    # Experience
    add_section(doc, "Experience", user_data.get("Experience", ""))

    # Projects
    add_section(doc, "Projects", user_data.get("Projects", ""))

    # Skills
    add_section(doc, "Skills", user_data.get("Skills", ""))

    # Education
    add_section(doc, "Education", user_data.get("Education", ""))

    # Activities
    add_section(doc, "Activities", user_data.get("Activities", ""))

    # Save the template
    doc.save(output_path)

def add_section(doc, title, content):
    # Section Title
    heading = doc.add_paragraph()
    heading_run = heading.add_run(title)
    heading_run.bold = True
    heading_run.font.size = Pt(14)
    heading_run.font.underline = True

    # Section Content
    content_para = doc.add_paragraph()
    content_run = content_para.add_run(content)
    content_run.font.size = Pt(12)

# Usage Example
if __name__ == "__main__":
    # Sample user data dictionary
    user_data = {
        "Full Name": "John Doe",
        "Address": "123 Main Street, City, Country",
        "Phone": "+1234567890",
        "Email": "john@example.com",
        "LinkedIn": "linkedin.com/in/johndoe",
        "GitHub": "github.com/johndoe",
        "Professional Summary": "Experienced developer with a passion for coding.",
        "Experience": "Software Developer at XYZ Corp (2020-2023)",
        "Projects": "- Project A: Description\n- Project B: Description",
        "Skills": "Python, Java, SQL",
        "Education": "B.Tech in Computer Science, ABC University, 2020, 8.5 CGPA",
        "Activities": "Hackathons, Open-source contributions"
    }

    create_modern_clean_template("modern_clean_resume.docx", user_data)
    print("Modern clean resume created successfully!")


def generate_resume_from_form_data(user_data, output_path):
    """
    Transforms user data from ResumeForm format to the format expected by create_modern_clean_template,
    then calls create_modern_clean_template to generate the resume document.
    """
    transformed_data = {}

    transformed_data["Full Name"] = user_data.get("Full Name", "")
    transformed_data["Email"] = user_data.get("Email", "")
    transformed_data["LinkedIn"] = user_data.get("LinkedIn", "")
    transformed_data["GitHub"] = user_data.get("GitHub", "")
    transformed_data["Professional Summary"] = user_data.get("Professional Summary", "")

    # Transform projects array to string
    projects = user_data.get("Projects", [])
    if isinstance(projects, list):
        projects_str = "\n\n".join(
            [f"Title: {p.get('title', '')}\nDescription: {p.get('description', '')}\nTech Stack: {p.get('techStack', '')}\nLink: {p.get('link', '')}" for p in projects]
        )
    else:
        projects_str = ""
    transformed_data["Projects"] = projects_str

    # Transform experiences array to string
    experiences = user_data.get("Experiences", []) or user_data.get("Experience", [])
    if isinstance(experiences, list):
        experiences_str = "\n\n".join(
            [f"Company: {e.get('companyName', '')}\nJob Title: {e.get('jobTitle', '')}\nDuration: {e.get('duration', '')}\nDescription: {e.get('description', '')}" for e in experiences]
        )
    else:
        experiences_str = ""
    transformed_data["Experience"] = experiences_str

    # Transform certifications array to string
    certifications = user_data.get("Certifications", []) or user_data.get("Certification", [])
    if isinstance(certifications, list):
        certifications_str = "\n\n".join(
            [f"Title: {c.get('title', '')}\nIssuer: {c.get('issuer', '')}\nDate: {c.get('date', '')}" for c in certifications]
        )
    else:
        certifications_str = ""
    transformed_data["Certifications"] = certifications_str

    # Transform education array to string
    education = user_data.get("Education", [])
    if isinstance(education, list):
        education_str = "\n\n".join(
            [f"Degree: {edu.get('degree', '')}\nInstitution: {edu.get('institution', '')}\nDuration: {edu.get('duration', '')}" for edu in education]
        )
    else:
        education_str = ""
    transformed_data["Education"] = education_str

    # Combine technicalSkills and softSkills into Skills string
    technical_skills = user_data.get("TechnicalSkills", []) or user_data.get("technicalSkills", [])
    soft_skills = user_data.get("SoftSkills", []) or user_data.get("softSkills", [])
    skills_list = []
    if isinstance(technical_skills, list):
        skills_list.extend(technical_skills)
    if isinstance(soft_skills, list):
        skills_list.extend(soft_skills)
    transformed_data["Skills"] = ", ".join(skills_list)

    # Activities can be empty or added later
    transformed_data["Activities"] = ""

    create_modern_clean_template(output_path, transformed_data)
