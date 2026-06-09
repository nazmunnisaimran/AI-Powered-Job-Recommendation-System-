import re
from pypdf import PdfReader

# Extensive dictionary of technical skills to match in resumes
TECH_SKILLS = [
    # Languages
    'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'c', 'ruby', 'php', 
    'swift', 'go', 'golang', 'rust', 'kotlin', 'r', 'scala', 'perl', 'sql', 'nosql', 'html', 'css', 'sass',
    
    # Frontend Frameworks & Libraries
    'react', 'reactjs', 'angular', 'angularjs', 'vue', 'vuejs', 'nextjs', 'next.js', 'svelte', 'jquery', 
    'bootstrap', 'tailwind', 'tailwindcss', 'material-ui', 'mui', 'redux', 'webpack',
    
    # Backend Frameworks
    'django', 'flask', 'fastapi', 'node.js', 'nodejs', 'express', 'expressjs', 'spring boot', 'spring', 
    'laravel', 'asp.net', 'net core', 'rails', 'ruby on rails', 'nest.js', 'nestjs',
    
    # Databases & Caching
    'mysql', 'postgresql', 'postgres', 'sqlite', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 
    'mariadb', 'oracle', 'firebase', 'dynamodb',
    
    # Cloud & DevOps
    'aws', 'amazon web services', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 
    'git', 'github', 'gitlab', 'ansible', 'terraform', 'ci/cd', 'cicd', 'linux', 'unix', 'nginx', 'apache',
    
    # Data Science & Machine Learning
    'machine learning', 'deep learning', 'nlp', 'natural language processing', 'computer vision', 
    'data science', 'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'pytorch', 'keras', 
    'nltk', 'spacy', 'spark', 'hadoop', 'tableau', 'power bi', 'excel', 'data analysis', 'matplotlib', 'seaborn',
    
    # Other concepts & Tools
    'rest api', 'restful api', 'graphql', 'soap', 'microservices', 'agile', 'scrum', 'jira', 
    'object-oriented programming', 'oop', 'algorithms', 'data structures', 'system design', 
    'ui/ux', 'figma', 'adobe xd', 'testing', 'unit testing', 'jest', 'cypress', 'selenium', 'postman'
]

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a local PDF resume file using pypdf.
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def clean_text(text):
    """
    Normalizes text to lowercase and cleans up whitespace.
    """
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    # Replace multiple spaces/newlines with single spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills(text):
    """
    Extracts skills by matching normalized text against the TECH_SKILLS database.
    Handles special characters like c++, c#, .net, node.js, etc.
    """
    cleaned = clean_text(text)
    extracted = set()
    
    for skill in TECH_SKILLS:
        # Build a regex pattern that handles boundary checks, especially for symbols like +, #, .
        # Escape the skill name to prevent regex errors (e.g. c++ -> c\+\+)
        escaped_skill = re.escape(skill)
        
        # Determine boundary rules
        # If the skill starts/ends with alphanumeric, enforce word boundary \b.
        # Otherwise, don't enforce word boundary (e.g. for .net or c++)
        start_boundary = r'\b' if escaped_skill[0].isalnum() else ''
        end_boundary = r'\b' if escaped_skill[-1].isalnum() else ''
        
        # Special case adjustments
        # c++ needs to match c++ but not react+ (which is rare anyway)
        if skill == 'c++':
            pattern = r'\bc\+\+(?!\+)'
        elif skill == 'c#':
            pattern = r'\bc\#(?!\#)'
        elif skill == 'gcp' or skill == 'aws':
            pattern = r'\b' + escaped_skill + r'\b'
        else:
            pattern = start_boundary + escaped_skill + end_boundary
            
        # Match using regex
        if re.search(pattern, cleaned):
            # Normalize display name (e.g. nodejs and node.js match to "Node.js", reactjs to "React", etc.)
            display_name = normalize_skill_name(skill)
            extracted.add(display_name)
            
    return sorted(list(extracted))

def normalize_skill_name(skill):
    """
    Normalizes alternative spellings of skills to standard display names.
    """
    mapping = {
        'reactjs': 'React',
        'react': 'React',
        'angularjs': 'Angular',
        'angular': 'Angular',
        'vuejs': 'Vue.js',
        'vue': 'Vue.js',
        'nextjs': 'Next.js',
        'next.js': 'Next.js',
        'nodejs': 'Node.js',
        'node.js': 'Node.js',
        'expressjs': 'Express',
        'express': 'Express',
        'nestjs': 'Nest.js',
        'nest.js': 'Nest.js',
        'golang': 'Go',
        'go': 'Go',
        'tailwindcss': 'Tailwind CSS',
        'tailwind': 'Tailwind CSS',
        'material-ui': 'Material-UI',
        'mui': 'Material-UI',
        'gcp': 'GCP',
        'google cloud': 'GCP',
        'aws': 'AWS',
        'amazon web services': 'AWS',
        'amazon web services (aws)': 'AWS',
        'postgresql': 'PostgreSQL',
        'postgres': 'PostgreSQL',
        'scikit-learn': 'Scikit-learn',
        'sklearn': 'Scikit-learn',
        'natural language processing': 'NLP',
        'nlp': 'NLP',
        'ci/cd': 'CI/CD',
        'cicd': 'CI/CD',
        'rest api': 'REST APIs',
        'restful api': 'REST APIs',
        'git': 'Git',
        'github': 'Git',
        'gitlab': 'Git',
        'net core': '.NET Core',
        'asp.net': 'ASP.NET',
        'ruby on rails': 'Ruby on Rails',
        'rails': 'Ruby on Rails',
        'object-oriented programming': 'OOP',
        'oop': 'OOP',
        'data structures': 'Data Structures & Algorithms',
        'algorithms': 'Data Structures & Algorithms',
    }
    
    # Default is capitalized form of skill
    default = skill.title() if len(skill) > 3 else skill.upper()
    
    # Specific exceptions to uppercase:
    if skill in ['html', 'css', 'sql', 'nosql', 'xml', 'api', 'gcp', 'aws', 'nlp', 'oop', 'ui/ux']:
        return skill.upper()
    if skill == 'c#':
        return 'C#'
    if skill == 'c++':
        return 'C++'
    if skill == 'c':
        return 'C'
    if skill == 'r':
        return 'R'
    
    return mapping.get(skill.lower(), default)
