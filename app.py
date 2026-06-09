import os
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, UserProfile, Job, LearningResource
from parser import extract_text_from_pdf, extract_skills
from recommender import get_recommendations

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize DB
    db.init_app(app)
    
    # Ensure Upload Folder Exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Load logged-in user before every request
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.session.get(User, user_id)
            
    # Helper to check file extension
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    # --- Core Routes ---
    
    @app.route('/')
    def index():
        if g.user:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth'))

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        if g.user:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'register':
                username = request.form.get('username', '').strip()
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                confirm_password = request.form.get('confirm_password', '')
                
                if not username or not email or not password:
                    flash('All fields are required for registration.', 'danger')
                    return render_template('auth.html', active_tab='register')
                    
                if password != confirm_password:
                    flash('Passwords do not match.', 'danger')
                    return render_template('auth.html', active_tab='register', username=username, email=email)
                    
                # Check if user already exists
                existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
                if existing_user:
                    flash('Username or email already exists.', 'danger')
                    return render_template('auth.html', active_tab='register', username=username, email=email)
                
                # Create user and profile
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.flush()  # Gets new_user.id
                
                new_profile = UserProfile(user_id=new_user.id)
                db.session.add(new_profile)
                db.session.commit()
                
                session.permanent = True
                session['user_id'] = new_user.id
                flash('Account created successfully! Welcome to your dashboard.', 'success')
                return redirect(url_for('dashboard'))
                
            elif action == 'login':
                username_or_email = request.form.get('username_or_email', '').strip()
                password = request.form.get('password', '')
                
                if not username_or_email or not password:
                    flash('Please enter both your credentials.', 'danger')
                    return render_template('auth.html', active_tab='login')
                    
                user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
                
                if user and user.check_password(password):
                    session.permanent = True
                    session['user_id'] = user.id
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username/email or password.', 'danger')
                    return render_template('auth.html', active_tab='login', username_or_email=username_or_email)
                    
        return render_template('auth.html', active_tab='login')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth'))

    @app.route('/dashboard')
    def dashboard():
        if not g.user:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('auth'))
            
        profile = UserProfile.query.filter_by(user_id=g.user.id).first()
        skills_list = [s.strip() for s in profile.skills.split(',')] if profile and profile.skills else []
        
        return render_template('dashboard.html', profile=profile, skills=skills_list)

    @app.route('/upload', methods=['POST'])
    def upload_resume():
        if not g.user:
            return jsonify({'error': 'Unauthorized'}), 401
            
        if 'resume' not in request.files:
            flash('No file part uploaded.', 'danger')
            return redirect(url_for('dashboard'))
            
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('dashboard'))
            
        if file and allowed_file(file.filename):
            # Save file
            filename = f"user_{g.user.id}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse skills and text from PDF
            try:
                extracted_text = extract_text_from_pdf(filepath)
                skills = extract_skills(extracted_text)
                
                # Update user profile
                profile = UserProfile.query.filter_by(user_id=g.user.id).first()
                if not profile:
                    profile = UserProfile(user_id=g.user.id)
                    db.session.add(profile)
                
                profile.resume_filename = file.filename
                profile.extracted_text = extracted_text
                profile.skills = ", ".join(skills)
                db.session.commit()
                
                flash(f'Resume uploaded and parsed successfully! Extracted {len(skills)} skills.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Failed to parse resume: {str(e)}', 'danger')
                
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid file format. Please upload a PDF file.', 'danger')
            return redirect(url_for('dashboard'))

    @app.route('/recommendations')
    def recommendations():
        if not g.user:
            flash('Please log in to view recommendations.', 'warning')
            return redirect(url_for('auth'))
            
        profile = UserProfile.query.filter_by(user_id=g.user.id).first()
        
        # If user hasn't uploaded a resume or added skills
        if not profile or (not profile.skills and not profile.extracted_text):
            flash('Please upload your resume to generate job recommendations.', 'info')
            return redirect(url_for('dashboard'))
            
        recs = get_recommendations(profile)
        
        return render_template('recommendations.html', recommendations=recs, skills_count=len(profile.skills.split(',')) if profile.skills else 0)

    # API to update skills manually from the frontend UI dashboard if needed
    @app.route('/api/update-skills', methods=['POST'])
    def update_skills():
        if not g.user:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            
        data = request.get_json() or {}
        new_skills = data.get('skills', [])
        
        try:
            profile = UserProfile.query.filter_by(user_id=g.user.id).first()
            if not profile:
                profile = UserProfile(user_id=g.user.id)
                db.session.add(profile)
                
            profile.skills = ", ".join([s.strip() for s in new_skills if s.strip()])
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    # Explicitly bind to 127.0.0.1 (localhost) on port 5000 to ensure address stability
    app.run(host='127.0.0.1', port=5000, debug=True)
