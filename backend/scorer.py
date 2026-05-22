def calculate_score(semantic_score, skill_match_percent, sections):
    # Section completeness score
    total_sections = len(sections)
    present_sections = sum(1 for v in sections.values() if v == "present")
    completeness_score = round(present_sections / total_sections * 100, 1)

    # Weighted final ATS score
    final_score = (
        semantic_score      * 0.40 +
        skill_match_percent * 0.35 +
        completeness_score  * 0.25
    )

    # Grade
    if final_score >= 80:
        grade = "Excellent"
    elif final_score >= 65:
        grade = "Good"
    elif final_score >= 50:
        grade = "Average"
    else:
        grade = "Needs Work"

    return {
        "semantic_score":     round(semantic_score, 1),
        "skill_match":        round(skill_match_percent, 1),
        "completeness":       completeness_score,
        "final_score":        round(final_score, 1),
        "grade":              grade
    }