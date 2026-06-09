import os
from app import create_app
from models import db, Job, LearningResource

def seed_database():
    print("Initializing Database Seeding...")
    
    # 1. Clear existing data
    db.drop_all()
    db.create_all()
    print("Database tables recreated successfully.")
    
    # 2. Sample Job Postings
    jobs = [
        Job(
            title="Junior Backend Developer",
            company="TechInnovate Solutions",
            location="Remote (US / Canada)",
            salary="$75,000 - $90,000",
            description="We are looking for a Junior Backend Developer to join our growing engineering team. You will assist in developing robust APIs, managing databases, and integrating third-party services. The ideal candidate has strong foundational knowledge of object-oriented programming, clean code writing, and backend architectures.",
            skills="Python, Flask, SQL, MySQL, Git, REST APIs"
        ),
        Job(
            title="Senior Frontend Engineer (React)",
            company="PixelPerfect Web",
            location="New York, NY (Hybrid)",
            salary="$130,000 - $160,000",
            description="PixelPerfect is seeking a Senior Frontend Engineer with deep expertise in React.js and modern state management. You will lead the development of our dashboard features, design slick interactive components, optimize page load times, and implement standard responsive designs using Tailwind CSS.",
            skills="JavaScript, TypeScript, React, HTML, CSS, Tailwind CSS, Git, Redux"
        ),
        Job(
            title="Full Stack Software Engineer",
            company="SaaSFlow Inc.",
            location="San Francisco, CA (Hybrid)",
            salary="$110,000 - $140,000",
            description="Join us in building the future of workspace collaboration software. As a Full Stack Engineer, you will handle both server-side logic and frontend user interfaces. You will work with Node.js/Express on the backend, React on the frontend, and run CI/CD deployment pipelines using Docker.",
            skills="JavaScript, React, Node.js, Express, PostgreSQL, SQL, Docker, Git, REST APIs"
        ),
        Job(
            title="Junior Data Scientist / Analyst",
            company="DataInsight Labs",
            location="Remote (Global)",
            salary="$80,000 - $105,000",
            description="We are hiring a passionate Junior Data Scientist to help us analyze customer behavior patterns. You will build and test predictive models, write scripts to extract and clean unstructured data, and build interactive dashboards to report metrics. Python expertise is essential.",
            skills="Python, SQL, Pandas, NumPy, Scikit-learn, Machine Learning, Tableau, Excel"
        ),
        Job(
            title="Machine Learning Engineer",
            company="CognitiveAI Corp",
            location="Seattle, WA (On-site)",
            salary="$140,000 - $180,000",
            description="CognitiveAI is designing cutting-edge LLMs and agentic AI systems. We are looking for an ML Engineer to train, fine-tune, and deploy models. You will design neural networks, implement NLP text parsing utilities, and scale deep learning algorithms in production using PyTorch and AWS.",
            skills="Python, Machine Learning, Deep Learning, PyTorch, TensorFlow, NLP, Docker, AWS, Git"
        ),
        Job(
            title="DevOps & Cloud Engineer",
            company="CloudScale Infrastructure",
            location="Remote (Europe)",
            salary="$115,000 - $135,000",
            description="We are looking for a DevOps Engineer to automate and scale our cloud deployments. You will manage kubernetes clusters, optimize AWS resources, set up secure CI/CD pipelines, and support our development team's deployment needs. Security and automation are core priorities.",
            skills="Linux, AWS, Docker, Kubernetes, Jenkins, Git, CI/CD, Terraform, Python"
        ),
        Job(
            title="Python Web Developer",
            company="PyCraft Software",
            location="Austin, TX (Hybrid)",
            salary="$95,000 - $115,000",
            description="PyCraft builds bespoke web applications for healthcare providers. We need a backend-focused Python engineer with experience using Django, designing Relational Databases, and deploying on AWS. You'll write unit tests and help architect new server-side modules.",
            skills="Python, Django, SQL, PostgreSQL, REST APIs, Git, Docker, Unit Testing"
        )
    ]
    
    # 3. Sample Learning Resources
    resources = [
        # Python
        LearningResource(
            skill_name="python",
            title="Python for Everybody Specialization",
            platform="Coursera (University of Michigan)",
            url="https://www.coursera.org/specializations/python"
        ),
        LearningResource(
            skill_name="python",
            title="Complete Python BootCamp: Go from Zero to Hero in Python",
            platform="Udemy",
            url="https://www.udemy.com/course/complete-python-bootcamp/"
        ),
        
        # Flask
        LearningResource(
            skill_name="flask",
            title="Flask Web Development Tutorial",
            platform="Corey Schafer (YouTube)",
            url="https://youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH"
        ),
        
        # Django
        LearningResource(
            skill_name="django",
            title="Django for Beginners: Build websites with Python",
            platform="Book / Website",
            url="https://djangoforbeginners.com/"
        ),
        
        # React
        LearningResource(
            skill_name="react",
            title="React - The Complete Guide (incl Hooks, React Router, Redux)",
            platform="Udemy",
            url="https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
        ),
        LearningResource(
            skill_name="react",
            title="React Official Documentation & Interactive Tutorials",
            platform="React.dev",
            url="https://react.dev/learn"
        ),
        
        # Node.js / Express
        LearningResource(
            skill_name="node.js",
            title="Node.js, Express, MongoDB & More: The Complete Bootcamp",
            platform="Udemy",
            url="https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/"
        ),
        
        # SQL / Databases
        LearningResource(
            skill_name="sql",
            title="SQL for Data Science",
            platform="Coursera (UC Davis)",
            url="https://www.coursera.org/learn/sql-for-data-science"
        ),
        LearningResource(
            skill_name="mysql",
            title="MySQL Tutorial for Beginners",
            platform="Programming with Mosh (YouTube)",
            url="https://youtu.be/7S_tz1z_5bA"
        ),
        LearningResource(
            skill_name="postgresql",
            title="Intro to PostgreSQL Database Course",
            platform="freeCodeCamp (YouTube)",
            url="https://youtu.be/qw5yEgPHHL8"
        ),
        
        # Docker / Kubernetes
        LearningResource(
            skill_name="docker",
            title="Docker and Kubernetes: The Complete Guide",
            platform="Udemy",
            url="https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/"
        ),
        LearningResource(
            skill_name="kubernetes",
            title="Kubernetes Tutorial for Beginners",
            platform="TechWorld with Nana (YouTube)",
            url="https://youtu.be/X48VuDVv0do"
        ),
        
        # Git / GitHub
        LearningResource(
            skill_name="git",
            title="Git & GitHub Crash Course for Beginners",
            platform="freeCodeCamp (YouTube)",
            url="https://youtu.be/RGOj5yH7evk"
        ),
        
        # Machine Learning
        LearningResource(
            skill_name="machine learning",
            title="Supervised Machine Learning: Regression and Classification",
            platform="Coursera (Andrew Ng / DeepLearning.AI)",
            url="https://www.coursera.org/learn/machine-learning"
        ),
        LearningResource(
            skill_name="scikit-learn",
            title="Machine Learning with PyTorch and Scikit-Learn (Book)",
            platform="Sebastian Raschka",
            url="https://sebastianraschka.com/books/"
        ),
        
        # PyTorch
        LearningResource(
            skill_name="pytorch",
            title="PyTorch for Deep Learning Bootcamp",
            platform="Daniel Bourke (YouTube / Git)",
            url="https://youtu.be/V_xro1bcAuA"
        ),
        
        # AWS
        LearningResource(
            skill_name="aws",
            title="AWS Certified Solutions Architect Associate",
            platform="Adrian Cantrill / Udemy",
            url="https://learn.cantrill.io/"
        )
    ]
    
    # 4. Add and Commit
    for job in jobs:
        db.session.add(job)
    for res in resources:
        db.session.add(res)
        
    db.session.commit()
    print(f"Successfully seeded {len(jobs)} jobs and {len(resources)} learning resources.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()
