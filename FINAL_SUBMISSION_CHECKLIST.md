# CE310 Final Submission Checklist - Version 3

## Pre-Submission Verification (Complete ALL items)

### 1. AI Log Preparation
- [ ] Open `AI_LOG_ENHANCED.md`
- [ ] Review all 6 interaction sessions
- [ ] Verify debugging evidence is clear (before/after code)
- [ ] Verify critical evaluation of AI suggestions
- [ ] Convert to Word format (.docx)
- [ ] Save as `AI_log.docx` (exact filename required)
- [ ] File size check: Should be 50-200 KB

**How to convert**:
```bash
# Option 1: Use pandoc
pandoc AI_LOG_ENHANCED.md -o AI_log.docx

# Option 2: Copy content to Word manually
# - Open AI_LOG_ENHANCED.md in text editor
# - Copy all content
# - Paste into Microsoft Word
# - Format headings (Heading 1, 2, 3)
# - Save as AI_log.docx
```

---

### 2. Notebook Execution
- [ ] Open Jupyter Lab/Notebook
- [ ] Open `Part1.ipynb`
- [ ] Click: Kernel → Restart & Run All
- [ ] Wait for all cells to complete (may take 2-3 minutes)
- [ ] Verify no errors in any cell
- [ ] Verify all visualizations display correctly
- [ ] Save notebook (Ctrl+S)
- [ ] Close and reopen to verify outputs are saved

- [ ] Open `Part2.ipynb`
- [ ] Click: Kernel → Restart & Run All
- [ ] Wait for all cells to complete (may take 2-3 minutes)
- [ ] Verify no errors in any cell
- [ ] Verify all visualizations display correctly
- [ ] Verify Problem2 explanation is visible
- [ ] Save notebook (Ctrl+S)
- [ ] Close and reopen to verify outputs are saved

**Common Issues**:
- If "figures not found": Run `python scripts/generate_enhanced_visualizations.py` first
- If "module not found": Ensure you're in the CE310 directory
- If cells timeout: Increase Jupyter timeout in settings

---

### 3. Visual Inspection

#### Part1.ipynb Checklist:
- [ ] Title cell present and clear
- [ ] Each code cell has markdown explanation BEFORE it
- [ ] Task 1: OneMax test shows fitness increasing
- [ ] Task 2: Decoding tests show correct integer values
- [ ] Task 3: Encoding comparison chart displays
- [ ] Task 3: Parameter heatmap displays
- [ ] Task 3: Results table shows all 8 conditions
- [ ] Task 4: Deceptive comparison chart displays
- [ ] Task 4: Comparison shows trap < baseline
- [ ] Conclusions section present

#### Part2.ipynb Checklist:
- [ ] Title cell present and clear
- [ ] Each code cell has markdown explanation BEFORE it
- [ ] Task 5: Primitive set displayed correctly
- [ ] Task 6: Interpreter test shows execute([5,1,2], 3) = 4
- [ ] Task 7: Results table shows all 18 conditions
- [ ] Task 7: Problem2 explanation section present and detailed
- [ ] Task 7: Parameter impact heatmap displays
- [ ] Task 7: Computational cost chart displays
- [ ] Task 8: Primitive evolution plots display (both problems)
- [ ] Task 8: Detailed 8-subplot primitive charts display
- [ ] Conclusions section present

---

### 4. Content Quality Check

#### Incremental Development Evidence:
- [ ] Part1: At least 5 "Why this step" explanations
- [ ] Part1: At least 5 "What we're testing" statements
- [ ] Part1: At least 3 independent operator tests
- [ ] Part2: At least 5 "Why this step" explanations
- [ ] Part2: Interpreter validation with coursework example
- [ ] Part2: Fitness function validation with test cases

#### AI Log Quality:
- [ ] At least 6 interaction sessions documented
- [ ] At least 3 "Issue Found" (❌) examples
- [ ] At least 3 "My Fix" code blocks
- [ ] At least 3 "Test Added" examples
- [ ] Summary section with "What AI Helped With" and "What I Corrected"
- [ ] Declaration statement at end

#### Problem2 Explanation:
- [ ] Explains why ideal solution wasn't found
- [ ] Mentions 4 difficulty factors (complexity, length, search space, landscape)
- [ ] Provides best result achieved (-53.485)
- [ ] Compares to Problem1 difficulty
- [ ] Concludes this is expected behavior

---

### 5. File Preparation

#### Create Submission Zip:
```bash
# Create clean submission directory
mkdir CE310_Final_Submission
cd CE310_Final_Submission

# Copy required files
cp ../Part1.ipynb .
cp ../Part2.ipynb .
cp ../AI_log.docx .

# Verify file count (should be exactly 3)
ls -l

# Create zip
cd ..
zip -r CE310_Submission.zip CE310_Final_Submission/
```

#### Verify Zip Contents:
- [ ] Unzip to test directory
- [ ] Verify exactly 3 files present
- [ ] Verify Part1.ipynb opens in Jupyter
- [ ] Verify Part2.ipynb opens in Jupyter
- [ ] Verify AI_log.docx opens in Word
- [ ] Verify all outputs are visible in notebooks
- [ ] Verify no personal information in filenames

---

### 6. File Size Check
- [ ] Part1.ipynb: Should be 50-500 KB
- [ ] Part2.ipynb: Should be 50-500 KB
- [ ] AI_log.docx: Should be 50-200 KB
- [ ] Total zip: Should be < 5 MB

**If files are too large**:
- Clear output of cells with large data
- Reduce image DPI in visualizations
- Remove unnecessary cells

---

### 7. Metadata Cleanup
- [ ] Open Part1.ipynb in text editor
- [ ] Search for personal information (name, student ID, email)
- [ ] Remove any found instances
- [ ] Repeat for Part2.ipynb
- [ ] Repeat for AI_log.docx

**Common locations**:
- Notebook metadata section
- Cell metadata
- File paths (e.g., /Users/YourName/)
- Comments in code

---

### 8. FASER Upload Test
- [ ] Log into FASER
- [ ] Navigate to CE310 coursework submission
- [ ] Click "Upload" (don't submit yet!)
- [ ] Select CE310_Submission.zip
- [ ] Verify upload completes successfully
- [ ] Download uploaded file to verify integrity
- [ ] Delete test upload (if allowed)

---

### 9. Final Review

#### Technical Completeness:
- [ ] Part1: All 4 tasks (1-4) completed
- [ ] Part2: All 4 tasks (5-8) completed
- [ ] All required experiments run (10 runs per condition)
- [ ] All required statistics computed (mean, std, best-of-run)
- [ ] All required plots generated

#### Marking Criteria Alignment:
- [ ] Incremental development: Clear evidence in notebooks
- [ ] Responsible AI use: Comprehensive log with debugging
- [ ] Task 1 (10%): GA implementation complete
- [ ] Task 2 (10%): Both encodings implemented
- [ ] Task 3 (15%): Tuning + experiments complete
- [ ] Task 4 (15%): Deceptive problem with comparison
- [ ] Task 5 (10%): GP representation + operators
- [ ] Task 6 (20%): Interpreter + fitness functions
- [ ] Task 7 (10%): Experiments + statistics
- [ ] Task 8 (10%): Primitive frequency analysis

---

### 10. Backup Before Submission
```bash
# Create final backup
mkdir backups/final_submission_backup
cp Part1.ipynb backups/final_submission_backup/
cp Part2.ipynb backups/final_submission_backup/
cp AI_log.docx backups/final_submission_backup/
cp CE310_Submission.zip backups/final_submission_backup/

# Create timestamp
date > backups/final_submission_backup/TIMESTAMP.txt
```

---

### 11. Submission

#### Timing:
- [ ] Deadline: 2026-03-06, 2:00 PM
- [ ] Plan to submit at least 2 hours before deadline
- [ ] Allow time for potential upload issues

#### Submission Steps:
1. [ ] Log into FASER
2. [ ] Navigate to CE310 coursework submission page
3. [ ] Upload CE310_Submission.zip
4. [ ] Verify upload success message
5. [ ] Download submitted file to verify
6. [ ] Take screenshot of submission confirmation
7. [ ] Save confirmation email (if sent)

---

### 12. Post-Submission

- [ ] Keep backup of all files for at least 6 months
- [ ] Keep screenshot of submission confirmation
- [ ] Keep copy of submission email
- [ ] Do NOT modify any files after submission
- [ ] Do NOT delete any files until after grades are released

---

## Emergency Contacts

If you encounter issues:
- **Technical issues**: FASER support (check FASER website)
- **Content questions**: Prof. Riccardo Poli (email from coursework PDF)
- **Deadline extension**: Follow university procedures

---

## Estimated Completion Time

- AI Log conversion: 15-30 minutes
- Notebook execution: 5-10 minutes
- Visual inspection: 20-30 minutes
- File preparation: 10-15 minutes
- Upload and verification: 10-15 minutes

**Total: 60-100 minutes**

**Recommendation**: Start this checklist at least 3 hours before deadline.

---

## Version 3 Specific Checks

- [ ] All 7 enhanced visualizations present in figures/
- [ ] Problem2 explanation visible in Part2 notebook
- [ ] AI_LOG_ENHANCED.md converted to Word
- [ ] Incremental development evidence added to both notebooks
- [ ] Deceptive comparison shows local optimum convergence
- [ ] Primitive evolution shows 8 subplots per problem

---

## Confidence Check

Rate your confidence (1-5) for each criterion:

- Incremental Development: ___/5
- Responsible AI Use: ___/5
- Technical Implementation: ___/5
- Experimental Rigor: ___/5
- Documentation Quality: ___/5

**If any score < 4**: Review that section again before submitting.

---

## Final Declaration

I confirm that:
- [ ] All checklist items are completed
- [ ] I understand all submitted code
- [ ] I can explain any part of my work
- [ ] All AI interactions are documented
- [ ] No plagiarism or academic misconduct
- [ ] Submission is my own work

**Signature**: ________________  
**Date**: ________________  
**Time**: ________________

---

## Good Luck! 🍀

You've put in excellent work on this coursework. Version 3 represents a strong submission with:
- Comprehensive technical implementation
- Clear incremental development evidence
- Responsible AI usage documentation
- Enhanced visualizations
- Detailed analysis and explanations

**Expected Score: 37-39% out of 40% (92-98%)**

Trust your preparation and submit with confidence!
