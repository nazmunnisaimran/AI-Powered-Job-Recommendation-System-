import math
import re
from models import Job, LearningResource

def parse_skills_list(skills_str):
    """
    Splits a comma-separated skills string into a clean, lowercased set.
    """
    if not skills_str:
        return set()
    return {s.strip().lower() for s in skills_str.split(',') if s.strip()}

# --- Pure Python TF-IDF and Cosine Similarity Implementation ---

def tokenize(text):
    """
    Cleans, lowercases, tokenizes and removes simple stop words.
    """
    if not text:
        return []
    # Lowercase and find all words of length 2 or more
    words = re.findall(r'\b[a-z]{2,}\b', text.lower())
    
    # Common English stop words
    STOP_WORDS = {
        'the', 'and', 'a', 'of', 'to', 'is', 'in', 'that', 'this', 'it', 'for', 'on', 'with', 'as', 'by', 'an', 
        'be', 'at', 'or', 'are', 'from', 'your', 'our', 'we', 'you', 'i', 'my', 'me', 'he', 'she', 'they', 'them',
        'will', 'can', 'should', 'would', 'have', 'has', 'had', 'do', 'does', 'did', 'but', 'not', 'about', 'which',
        'there', 'their', 'then', 'than', 'so', 'who', 'its', 'into', 'only', 'more', 'about', 'other', 'all'
    }
    return [w for w in words if w not in STOP_WORDS]

def compute_tfidf_vectors(documents):
    """
    Computes TF-IDF vector dicts for a list of document texts.
    Returns: list of dicts mapping {word: tfidf_value}
    """
    if not documents:
        return []
        
    tokenized_docs = [tokenize(doc) for doc in documents]
    num_docs = len(documents)
    
    # 1. Document Frequency (DF)
    df = {}
    for doc in tokenized_docs:
        unique_words = set(doc)
        for w in unique_words:
            df[w] = df.get(w, 0) + 1
            
    # 2. Inverse Document Frequency (IDF)
    idf = {}
    for w, count in df.items():
        # Using standard smoothed IDF formula: log((1 + N) / (1 + df)) + 1
        idf[w] = math.log((1 + num_docs) / (1 + count)) + 1
        
    # 3. Term Frequency - Inverse Document Frequency (TF-IDF)
    vectors = []
    for doc in tokenized_docs:
        if not doc:
            vectors.append({})
            continue
            
        tf = {}
        for w in doc:
            tf[w] = tf.get(w, 0) + 1
            
        doc_len = len(doc)
        doc_vector = {}
        for w, count in tf.items():
            # Normalized TF: term count / total terms in doc
            normalized_tf = count / doc_len
            doc_vector[w] = normalized_tf * idf[w]
            
        vectors.append(doc_vector)
        
    return vectors

def calculate_cosine_similarity(vec1, vec2):
    """
    Calculates cosine similarity between two vector dicts: vec1 and vec2.
    """
    if not vec1 or not vec2:
        return 0.0
        
    # Dot product
    dot_product = 0.0
    for word, val in vec1.items():
        if word in vec2:
            dot_product += val * vec2[word]
            
    # Vector magnitudes (norms)
    norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
        
    return dot_product / (norm1 * norm2)

# --- Recommendation Core Engine ---

def get_recommendations(user_profile):
    """
    Computes job recommendations for a user profile using:
    1. Cosine similarity of resume text with job descriptions (pure Python).
    2. Overlap ratio of user skills and required job skills.
    
    Returns a list of dictionaries with job details, match percentage, skill gap, and course recommendations.
    """
    # 1. Fetch all jobs from the database
    jobs = Job.query.all()
    if not jobs:
        return []
    
    # 2. Get user skills
    user_skills_set = parse_skills_list(user_profile.skills)
    user_text = user_profile.extracted_text or ""
    
    # Fallback to user skills list as text if resume text is empty
    if not user_text and user_profile.skills:
        user_text = " ".join(user_skills_set)
    
    # 3. Calculate text similarity using our pure Python TF-IDF and Cosine Similarity
    job_descriptions = [job.description for job in jobs]
    all_texts = [user_text] + job_descriptions
    
    try:
        tfidf_vectors = compute_tfidf_vectors(all_texts)
        user_vector = tfidf_vectors[0]
        job_vectors = tfidf_vectors[1:]
        
        # Calculate similarity against each job
        similarities = [calculate_cosine_similarity(user_vector, job_vec) for job_vec in job_vectors]
    except Exception as e:
        print(f"Error calculating TF-IDF similarity: {e}")
        similarities = [0.0] * len(jobs)
        
    # 4. Process each job and build final list
    recommendations = []
    for idx, job in enumerate(jobs):
        job_skills_set = parse_skills_list(job.skills)
        
        # Calculate Skill Match Score
        if job_skills_set:
            matching_skills = user_skills_set.intersection(job_skills_set)
            skill_match_ratio = len(matching_skills) / len(job_skills_set)
        else:
            matching_skills = set()
            skill_match_ratio = 1.0  # No skills required, so 100% match on skills
            
        # Get TF-IDF cosine similarity score
        text_sim_score = float(similarities[idx]) if idx < len(similarities) else 0.0
        
        # Combine both scores: 60% skill match (hard requirement) + 40% description similarity (contextual)
        # Limit text similarity impact if user has absolutely zero matching skills but description matches generic words
        if len(job_skills_set) > 0 and len(matching_skills) == 0:
            combined_score = text_sim_score * 0.2  # penalize severely if no required skills match
        else:
            combined_score = (0.6 * skill_match_ratio) + (0.4 * text_sim_score)
            
        # Match percentage (0% to 100%)
        match_percentage = round(min(combined_score * 100, 100.0), 1)
        
        # Ensure match percentage is non-negative and realistic
        if match_percentage < 0:
            match_percentage = 0.0
            
        # Identify Skill Gaps
        missing_skills = sorted(list(job_skills_set - user_skills_set))
        
        # Capitalize display names of required and missing skills for UI
        display_required_skills = [s.strip() for s in job.skills.split(',') if s.strip()]
        display_missing_skills = []
        for missing in missing_skills:
            # Match the case from the original job's skill list if possible
            matched_name = None
            for req in display_required_skills:
                if req.lower() == missing.lower():
                    matched_name = req
                    break
            display_missing_skills.append(matched_name or missing.title())
            
        # Find Learning Recommendations for missing skills
        learning_paths = []
        if missing_skills:
            # Query courses from DB that match any of the missing skills
            resources = LearningResource.query.filter(
                LearningResource.skill_name.in_([s.lower() for s in missing_skills])
            ).all()
            
            # Group resources by skill
            skill_to_courses = {}
            for res in resources:
                s_name = res.skill_name.lower()
                if s_name not in skill_to_courses:
                    skill_to_courses[s_name] = []
                skill_to_courses[s_name].append({
                    'title': res.title,
                    'platform': res.platform,
                    'url': res.url
                })
                
            # Build structured learning paths list
            for s_name in missing_skills:
                # Find display name for skill
                disp_name = None
                for req in display_required_skills:
                    if req.lower() == s_name:
                        disp_name = req
                        break
                disp_name = disp_name or s_name.title()
                
                learning_paths.append({
                    'skill': disp_name,
                    'courses': skill_to_courses.get(s_name, [
                        # Fallback course recommendation if not in DB
                        {
                            'title': f"Learn {disp_name} on YouTube",
                            'platform': 'YouTube Search',
                            'url': f"https://www.youtube.com/results?search_query=learn+{disp_name}+tutorial"
                        },
                        {
                            'title': f"Learn {disp_name} on Coursera",
                            'platform': 'Coursera',
                            'url': f"https://www.coursera.org/courses?query={disp_name}"
                        }
                    ])
                })
                
        recommendations.append({
            'job_id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'salary': job.salary,
            'description': job.description,
            'required_skills': display_required_skills,
            'match_percentage': match_percentage,
            'missing_skills': display_missing_skills,
            'learning_paths': learning_paths
        })
        
    # Sort recommendations by match percentage descending
    recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    return recommendations
