/**
 * RESUME MATCHER AI - FRONTEND SCRIPT (DESIGN ARENA EDITION)
 * Manages user interactions, sample data loading, FastAPI /match API integration,
 * dynamic score visualization, and skill breakdown rendering.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Element References
    const candidateNameInput = document.getElementById('candidateName');
    const resumeTextInput = document.getElementById('resumeText');
    const jobDescriptionInput = document.getElementById('jobDescription');
    
    const matchBtn = document.getElementById('matchBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnText = document.getElementById('btnText');
    
    const loadSampleDataBtn = document.getElementById('loadSampleDataBtn');
    const loadSampleWebBtn = document.getElementById('loadSampleWebBtn');
    const clearResumeBtn = document.getElementById('clearResumeBtn');
    const clearJobBtn = document.getElementById('clearJobBtn');
    
    const errorBanner = document.getElementById('errorBanner');
    const errorMessage = document.getElementById('errorMessage');
    
    const emptyState = document.getElementById('emptyState');
    const resultSection = document.getElementById('resultSection');
    const candidateDisplay = document.getElementById('candidateDisplay');
    const scoreValue = document.getElementById('scoreValue');
    const scoreRingProgress = document.getElementById('scoreRingProgress');
    const scoreCategory = document.getElementById('scoreCategory');
    const matchedSkillsList = document.getElementById('matchedSkillsList');
    const missingSkillsList = document.getElementById('missingSkillsList');
    const feedbackText = document.getElementById('feedbackText');

    // Pre-populate default sample values if empty
    if (!resumeTextInput.value.trim()) {
        resumeTextInput.value = "Python, SQL, Machine Learning, Pandas, NumPy, Scikit-learn, Git";
    }
    if (!jobDescriptionInput.value.trim()) {
        jobDescriptionInput.value = "Looking for a Data Scientist skilled in Python, SQL, Machine Learning, Pandas, AWS, and Docker.";
    }

    // Sample Data Loaders
    loadSampleDataBtn.addEventListener('click', () => {
        candidateNameInput.value = "Ajay Kumar";
        resumeTextInput.value = "Ajay Kumar\nData Scientist & AI Developer\n\nSkills:\nPython, SQL, Pandas, NumPy, Scikit-learn, Machine Learning, Deep Learning, BERT, NLP, Git, FastAPI";
        jobDescriptionInput.value = "Senior Data Scientist - AI Team\n\nRequirements:\nMust have strong proficiency in Python, SQL, Pandas, and Machine Learning.\nExperience with Deep Learning and BERT NLP models.\nExperience with Docker, AWS, and Git for deployment.";
        hideError();
    });

    loadSampleWebBtn.addEventListener('click', () => {
        candidateNameInput.value = "Priya Sharma";
        resumeTextInput.value = "Priya Sharma\nFull Stack Web Developer\n\nSkills:\nJavaScript, TypeScript, React, Node.js, Express, HTML, CSS, SQL, Git, Linux";
        jobDescriptionInput.value = "Full Stack Web Developer\n\nRequirements:\nStrong experience in JavaScript, React, Node.js, and SQL.\nHands-on experience with Docker, Kubernetes, and Cloud platforms like Azure.";
        hideError();
    });

    // Clear Button Action Handlers
    clearResumeBtn.addEventListener('click', () => {
        resumeTextInput.value = '';
        resumeTextInput.focus();
    });

    clearJobBtn.addEventListener('click', () => {
        jobDescriptionInput.value = '';
        jobDescriptionInput.focus();
    });

    // Match Button Click Event Listener
    matchBtn.addEventListener('click', async () => {
        const candidateName = candidateNameInput.value.trim();
        const resumeText = resumeTextInput.value.trim();
        const jobDescription = jobDescriptionInput.value.trim();

        // 1. Client-Side Input Validation
        if (!candidateName) {
            showError("Please enter the candidate's full name.");
            candidateNameInput.focus();
            return;
        }
        if (!resumeText) {
            showError("Please paste candidate resume text before analyzing.");
            resumeTextInput.focus();
            return;
        }
        if (!jobDescription) {
            showError("Please paste the target job description text.");
            jobDescriptionInput.focus();
            return;
        }

        // Reset previous error state
        hideError();

        // 2. Set Loading UI State
        setLoadingState(true);

        try {
            // 3. Perform Asynchronous API POST Call to /match
            const response = await fetch('/match', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    candidate_name: candidateName,
                    resume_text: resumeText,
                    job_description: jobDescription
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const detailMsg = errorData.detail || `Server error (Status ${response.status})`;
                throw new Error(detailMsg);
            }

            const data = await response.json();

            // 4. Render API Analysis Results
            renderResults(data);

        } catch (error) {
            console.error('Match Request Failed:', error);
            showError("Unable to connect to Resume Matcher API. Please ensure the FastAPI server is running.");
        } finally {
            // Restore Action Button State
            setLoadingState(false);
        }
    });

    /**
     * Toggles button loading state and spinner animation.
     */
    function setLoadingState(isLoading) {
        matchBtn.disabled = isLoading;
        if (isLoading) {
            btnSpinner.classList.remove('hidden');
            btnText.textContent = "Analyzing Resume...";
        } else {
            btnSpinner.classList.add('hidden');
            btnText.textContent = "Analyze Resume";
        }
    }

    /**
     * Displays error banner with specified text.
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorBanner.classList.remove('hidden');
    }

    /**
     * Hides error banner.
     */
    function hideError() {
        errorBanner.classList.add('hidden');
    }

    /**
     * Populates result dashboard with response data from /match API.
     */
    function renderResults(data) {
        // Candidate Name
        candidateDisplay.textContent = `Candidate: ${data.candidate_name || 'Candidate'}`;

        // Match Score Calculations
        const score = data.match_score || 0;
        const scoreFormatted = Number(score).toFixed(1);
        scoreValue.textContent = `${scoreFormatted}%`;

        // Update Score Category Label
        if (score >= 80) {
            scoreCategory.textContent = "High Match Score";
            scoreCategory.style.color = "#047857"; // Emerald Green
        } else if (score >= 50) {
            scoreCategory.textContent = "Moderate Match Score";
            scoreCategory.style.color = "#4f46e5"; // Indigo Blue
        } else {
            scoreCategory.textContent = "Low Match Score";
            scoreCategory.style.color = "#c2410c"; // Coral / Orange
        }

        // SVG Radial Progress Calculation (Circumference = 2 * PI * r = 2 * 3.14159 * 58 ≈ 364.42)
        const circumference = 364.42;
        const clampedScore = Math.min(100, Math.max(0, score));
        const offset = circumference - (circumference * (clampedScore / 100));
        scoreRingProgress.style.strokeDashoffset = offset;

        // Render Matched Skills
        matchedSkillsList.innerHTML = '';
        if (Array.isArray(data.matched_skills) && data.matched_skills.length > 0) {
            data.matched_skills.forEach(skill => {
                const chip = document.createElement('span');
                chip.className = 'skill-chip matched-chip';
                chip.innerHTML = `✓ ${escapeHtml(skill)}`;
                matchedSkillsList.appendChild(chip);
            });
        } else {
            matchedSkillsList.innerHTML = '<span class="empty-skill-msg">No matching technical skills detected.</span>';
        }

        // Render Missing Skills
        missingSkillsList.innerHTML = '';
        if (Array.isArray(data.missing_skills) && data.missing_skills.length > 0) {
            data.missing_skills.forEach(skill => {
                const chip = document.createElement('span');
                chip.className = 'skill-chip missing-chip';
                chip.innerHTML = `! ${escapeHtml(skill)}`;
                missingSkillsList.appendChild(chip);
            });
        } else {
            missingSkillsList.innerHTML = '<span class="empty-skill-msg">No missing skills identified! Candidate possesses all required competencies.</span>';
        }

        // Render AI Feedback
        feedbackText.textContent = data.feedback || "Resume analysis completed successfully.";

        // Hide Empty State Card & Show Results Dashboard
        emptyState.classList.add('hidden');
        resultSection.classList.remove('hidden');

        // Smooth Scroll to Results Dashboard
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Prevents XSS when rendering skill tokens.
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
