/* ==========================================================================
   CareerMatch AI - Dynamic Frontend Interactions
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('open');
            const icon = menuToggle.querySelector('i');
            if (navMenu.classList.contains('open')) {
                icon.className = 'fa-solid fa-xmark';
            } else {
                icon.className = 'fa-solid fa-bars';
            }
        });
    }

    // 2. Drag & Drop PDF Resume Upload Box
    const dropzone = document.getElementById('dropzone');
    const resumeInput = document.getElementById('resumeInput');
    const filePreview = document.getElementById('filePreview');
    const selectedFileName = document.getElementById('selectedFileName');
    const clearFileBtn = document.getElementById('clearFileBtn');
    const btnSubmitUpload = document.getElementById('btnSubmitUpload');
    const uploadForm = document.getElementById('uploadForm');

    if (dropzone && resumeInput) {
        // Highlight drop zone when dragging files over
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.remove('dragover');
            }, false);
        });

        // Handle file drop
        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                resumeInput.files = files;
                updateFilePreview(files[0]);
            }
        });

        // Handle manual file selection
        resumeInput.addEventListener('change', (e) => {
            if (resumeInput.files.length > 0) {
                updateFilePreview(resumeInput.files[0]);
            }
        });

        // Clear file selection
        if (clearFileBtn) {
            clearFileBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                resumeInput.value = '';
                filePreview.style.display = 'none';
                dropzone.querySelector('.dropzone-content').style.display = 'block';
                if (btnSubmitUpload) btnSubmitUpload.disabled = true;
            });
        }

        // Form submit spinner
        if (uploadForm) {
            uploadForm.addEventListener('submit', () => {
                if (btnSubmitUpload) {
                    btnSubmitUpload.disabled = true;
                    const spinner = btnSubmitUpload.querySelector('.spinner');
                    const textSpan = btnSubmitUpload.querySelector('span');
                    if (spinner) spinner.style.display = 'inline-block';
                    if (textSpan) textSpan.innerText = 'Extracting Skills...';
                }
            });
        }
    }

    function updateFilePreview(file) {
        if (file.type !== 'application/pdf') {
            alert('Only PDF files are supported.');
            resumeInput.value = '';
            return;
        }
        selectedFileName.innerText = file.name;
        dropzone.querySelector('.dropzone-content').style.display = 'none';
        filePreview.style.display = 'flex';
        if (btnSubmitUpload) btnSubmitUpload.disabled = false;
    }

    // 3. Manual Skills Tag Management
    const skillsContainer = document.getElementById('skillsContainer');
    const newSkillInput = document.getElementById('newSkillInput');
    const btnAddSkill = document.getElementById('btnAddSkill');
    const saveSkillsBar = document.getElementById('saveSkillsBar');
    const btnSaveSkills = document.getElementById('btnSaveSkills');

    // Keep track of skill changes
    let originalSkills = [];
    if (skillsContainer) {
        const pills = skillsContainer.querySelectorAll('.skill-pill');
        pills.forEach(pill => {
            originalSkills.push(pill.dataset.skill.trim());
        });
    }

    function getCurrentlyDisplayedSkills() {
        const skills = [];
        if (skillsContainer) {
            const pills = skillsContainer.querySelectorAll('.skill-pill');
            pills.forEach(pill => {
                skills.push(pill.dataset.skill.trim());
            });
        }
        return skills;
    }

    function checkSkillChanges() {
        if (!saveSkillsBar) return;
        const current = getCurrentlyDisplayedSkills();
        const hasChanges = (current.length !== originalSkills.length) || 
                            current.some((val, idx) => val.toLowerCase() !== originalSkills[idx].toLowerCase());
        
        if (hasChanges) {
            saveSkillsBar.style.display = 'flex';
        } else {
            saveSkillsBar.style.display = 'none';
        }
    }

    if (btnAddSkill && newSkillInput) {
        // Trigger add skill on button click
        btnAddSkill.addEventListener('click', () => {
            addCustomSkill();
        });

        // Trigger add skill on Enter key
        newSkillInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addCustomSkill();
            }
        });
    }

    function addCustomSkill() {
        const rawName = newSkillInput.value.trim();
        if (!rawName) return;
        
        // Clean name (e.g. capitalize first letters or match normalizations)
        const name = normalizeSkillString(rawName);
        
        const currentSkills = getCurrentlyDisplayedSkills();
        if (currentSkills.map(s => s.toLowerCase()).includes(name.toLowerCase())) {
            newSkillInput.value = '';
            return; // Already exists
        }

        // Remove placeholder if present
        const placeholder = document.getElementById('noSkillsPlaceholder');
        if (placeholder) {
            placeholder.remove();
        }

        // Create skill pill DOM element
        const pill = document.createElement('div');
        pill.className = 'skill-pill fade-in';
        pill.dataset.skill = name;
        pill.innerHTML = `
            <span>${name}</span>
            <button type="button" class="skill-remove-btn" onclick="removeSkill('${name}')">&times;</button>
        `;
        
        skillsContainer.appendChild(pill);
        newSkillInput.value = '';
        checkSkillChanges();
    }

    // Expose removeSkill to window since it is defined inline in HTML templates
    window.removeSkill = function(skillName) {
        const currentPills = skillsContainer.querySelectorAll('.skill-pill');
        currentPills.forEach(pill => {
            if (pill.dataset.skill.toLowerCase() === skillName.toLowerCase()) {
                pill.remove();
            }
        });

        // If no pills left, render placeholder
        const remaining = getCurrentlyDisplayedSkills();
        if (remaining.length === 0 && !document.getElementById('noSkillsPlaceholder')) {
            skillsContainer.innerHTML = `
                <div class="no-skills" id="noSkillsPlaceholder">
                    <i class="fa-solid fa-tags placeholder-icon"></i>
                    <h3>No skills parsed yet</h3>
                    <p>Upload a PDF resume to populate your skills inventory, or add skills manually below.</p>
                </div>
            `;
        }
        checkSkillChanges();
    };

    // Save manually configured skills
    if (btnSaveSkills) {
        btnSaveSkills.addEventListener('click', () => {
            const skills = getCurrentlyDisplayedSkills();
            btnSaveSkills.disabled = true;
            const textSpan = btnSaveSkills.querySelector('span');
            textSpan.innerText = 'Saving...';

            fetch('/api/update-skills', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ skills: skills })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    originalSkills = [...skills];
                    saveSkillsBar.style.display = 'none';
                    // Optional flash alert style
                    window.location.reload(); // Reload to refresh backend session context and sync recommendations
                } else {
                    alert('Error saving skills: ' + data.error);
                }
            })
            .catch(err => {
                console.error(err);
                alert('Connection error. Failed to save skills.');
            })
            .finally(() => {
                btnSaveSkills.disabled = false;
                textSpan.innerText = 'Save Changes';
            });
        });
    }

    function normalizeSkillString(skill) {
        // Special standard tech mappings
        const low = skill.toLowerCase();
        if (low === 'html' || low === 'css' || low === 'sql' || low === 'aws' || low === 'gcp' || low === 'nlp' || low === 'oop') {
            return skill.toUpperCase();
        }
        if (low === 'c++') return 'C++';
        if (low === 'c#') return 'C#';
        if (low === 'javascript') return 'JavaScript';
        if (low === 'typescript') return 'TypeScript';
        if (low === 'node.js' || low === 'nodejs') return 'Node.js';
        if (low === 'react' || low === 'reactjs') return 'React';
        
        // Capitalize words
        return skill.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }
});

// 4. Recommendation Pages: Toggle job card selection details
function selectJobCard(cardElement) {
    // 1. Remove active state from all job cards
    const cards = document.querySelectorAll('.job-card');
    cards.forEach(c => c.classList.remove('active'));

    // 2. Set clicked card as active
    cardElement.classList.add('active');

    // 3. Hide all detail contents
    const details = document.querySelectorAll('.job-detail-content');
    details.forEach(d => d.style.display = 'none');

    // 4. Show corresponding detail content
    const jobId = cardElement.dataset.jobId;
    const detailPanel = document.getElementById(`job-detail-${jobId}`);
    if (detailPanel) {
        detailPanel.style.display = 'block';
    }
}

// 5. Recommendations detailed panel tabs toggler
function switchDetailTab(buttonElement, targetPaneId) {
    const parentContainer = buttonElement.closest('.job-detail-content');
    
    // Deactivate all tab buttons in this details container
    const buttons = parentContainer.querySelectorAll('.detail-tab-btn');
    buttons.forEach(b => b.classList.remove('active'));

    // Deactivate all tab panes in this details container
    const panes = parentContainer.querySelectorAll('.detail-tab-pane');
    panes.forEach(p => p.style.display = 'none');

    // Activate selected button and pane
    buttonElement.classList.add('active');
    const targetPane = document.getElementById(targetPaneId);
    if (targetPane) {
        targetPane.style.display = 'block';
    }
}

// 6. Auth Tab Switcher (Login / Register cards)
function switchAuthTab(tab) {
    const loginTabBtn = document.getElementById('loginTabBtn');
    const registerTabBtn = document.getElementById('registerTabBtn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (tab === 'login') {
        loginTabBtn.classList.add('active');
        registerTabBtn.classList.remove('active');
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    } else if (tab === 'register') {
        registerTabBtn.classList.add('active');
        loginTabBtn.classList.remove('active');
        registerForm.classList.add('active');
        loginForm.classList.remove('active');
    }
}
