
"""
AI Competency-Based Classroom Evaluator
CBSE Science | Classes VI–X
Aligned to: CBSE CBE Learning Framework | NEP 2020 | PARAKH Guidelines

Competency sources:
- CBSE Learning Standards Framework - Science (Azim Premji University)
- CBSE Scientific Literacy Framework (CBSE + SAS + ACER/PISA)
"""

import streamlit as st
import json
import datetime
import pandas as pd

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CBSE AI Competency Evaluator",
    page_icon="🎓",
    layout="wide"
)

# ── CBSE COMPETENCY FRAMEWORK ─────────────────────────────────────────────────
# Source: CBSE Learning Standards Framework - Science (Azim Premji University)
# Subject-specific cognitive levels based on Revised Bloom's Taxonomy

BLOOM_LEVELS = {
    "L1 - Remember & Understand": {
        "description": "Recall facts, define terms, describe concepts",
        "keywords": ["define", "identify", "describe", "list", "state", "recall"],
        "cbse_weight": "20%"
    },
    "L2 - Apply": {
        "description": "Use knowledge in new situations, solve problems",
        "keywords": ["calculate", "solve", "use", "apply", "demonstrate", "show"],
        "cbse_weight": "40%"
    },
    "L3 - Analyse": {
        "description": "Break information into parts, find patterns, make inferences",
        "keywords": ["compare", "differentiate", "examine", "relate", "infer"],
        "cbse_weight": "25%"
    },
    "L4 - Evaluate & Create": {
        "description": "Judge, justify, design, propose solutions",
        "keywords": ["justify", "evaluate", "design", "propose", "argue", "assess"],
        "cbse_weight": "15%"
    }
}

# Source: CBSE Scientific Literacy Framework (PISA 2018 competencies)
# Developed by CBSE + Sri Aurobindo Society + ACER
SCIENCE_COMPETENCIES = {
    "C1": {
        "name": "Explain Phenomena Scientifically",
        "description": "Recognise, offer and evaluate explanations for natural phenomena using scientific knowledge",
        "what_to_look_for": "Does the student use scientific concepts to explain? Do they go beyond just naming facts?"
    },
    "C2": {
        "name": "Interpret Data and Evidence Scientifically",
        "description": "Analyse and evaluate data, claims and arguments using scientific reasoning",
        "what_to_look_for": "Does the student correctly read and interpret data? Do they draw valid conclusions?"
    },
    "C3": {
        "name": "Evaluate and Design Scientific Enquiry",
        "description": "Describe and appraise scientific investigations and propose ways to address questions scientifically",
        "what_to_look_for": "Does the student understand how scientific investigations work? Can they suggest improvements?"
    }
}

# Class-wise content domains from CBSE Science syllabus
CLASS_CONTENT = {
    "VI": {
        "topics": ["Food: Where Does It Come From?", "Components of Food", "Fibre to Fabric",
                   "Sorting Materials into Groups", "Separation of Substances", "Changes Around Us",
                   "Getting to Know Plants", "Body Movements", "The Living Organisms and Their Surroundings",
                   "Motion and Measurement of Distances", "Light, Shadows and Reflections",
                   "Electricity and Circuits", "Fun with Magnets", "Water", "Air Around Us", "Garbage In, Garbage Out"],
        "bloom_focus": "L1 and L2 — basic recall and simple application",
        "pisa_focus": "C1 — explaining simple natural phenomena"
    },
    "VII": {
        "topics": ["Nutrition in Plants", "Nutrition in Animals", "Fibre to Fabric", "Heat",
                   "Acids, Bases and Salts", "Physical and Chemical Changes", "Weather, Climate and Adaptations",
                   "Winds, Storms and Cyclones", "Soil", "Respiration in Organisms", "Transportation in Animals and Plants",
                   "Reproduction in Plants", "Motion and Time", "Electric Current and Its Effects",
                   "Light", "Water: A Precious Resource", "Forests: Our Lifeline", "Wastewater Story"],
        "bloom_focus": "L1, L2, early L3 — application and beginning of analysis",
        "pisa_focus": "C1 and C2 — explaining phenomena and beginning to interpret data"
    },
    "VIII": {
        "topics": ["Crop Production and Management", "Microorganisms", "Synthetic Fibres and Plastics",
                   "Materials: Metals and Non-Metals", "Coal and Petroleum", "Combustion and Flame",
                   "Conservation of Plants and Animals", "Cell — Structure and Functions",
                   "Reproduction in Animals", "Reaching the Age of Adolescence",
                   "Force and Pressure", "Friction", "Sound", "Chemical Effects of Electric Current",
                   "Some Natural Phenomena", "Light", "Stars and the Solar System", "Pollution of Air and Water"],
        "bloom_focus": "L2 and L3 — application and analysis",
        "pisa_focus": "C1, C2 — explaining and interpreting"
    },
    "IX": {
        "topics": ["Matter in Our Surroundings", "Is Matter Around Us Pure?", "Atoms and Molecules",
                   "Structure of the Atom", "The Fundamental Unit of Life", "Tissues",
                   "Diversity in Living Organisms", "Motion", "Force and Laws of Motion", "Gravitation",
                   "Work and Energy", "Sound", "Why Do We Fall Ill?", "Natural Resources",
                   "Improvement in Food Resources"],
        "bloom_focus": "L2, L3, early L4 — analysis and evaluation begins",
        "pisa_focus": "C1, C2, C3 — all three competencies introduced"
    },
    "X": {
        "topics": ["Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-Metals",
                   "Carbon and Its Compounds", "Life Processes", "Control and Coordination",
                   "How do Organisms Reproduce?", "Heredity", "Light — Reflection and Refraction",
                   "Human Eye and Colourful World", "Electricity", "Magnetic Effects of Electric Current",
                   "Our Environment"],
        "bloom_focus": "L2, L3, L4 — full range including evaluation and justification",
        "pisa_focus": "C1, C2, C3 — all three at higher proficiency levels"
    }
}

# ── DEMO EVALUATIONS ──────────────────────────────────────────────────────────
DEMO_RESPONSES = {
    "basic": {
        "bloom_level_achieved": "L1 - Remember & Understand",
        "bloom_level_expected": "L2 - Apply",
        "pisa_competency": "C1 - Explain Phenomena Scientifically",
        "cbse_competency_score": 2,
        "evidence_from_answer": "Student correctly named photosynthesis and mentioned sunlight, but did not explain the process or why it matters.",
        "learning_gaps": [
            "Cannot describe the step-by-step process of photosynthesis",
            "Does not connect raw materials (CO2, water) to the products (glucose, oxygen)",
            "Missing application — cannot explain why plants make their own food"
        ],
        "strengths": [
            "Correctly identified photosynthesis as the answer",
            "Mentioned sunlight as a requirement"
        ],
        "improvement_suggestions": [
            "Learn the word equation: CO2 + water + sunlight → glucose + oxygen",
            "Practice explaining what happens inside the chloroplast in your own words",
            "Try answering: Why can't animals make their own food like plants do?"
        ],
        "teacher_note": "Student is at recall level. Needs guided questioning to move toward understanding and application.",
        "next_question_suggestion": "What would happen to a plant if it was kept in complete darkness for two weeks? Explain using the process of photosynthesis."
    }
}

# ── AI EVALUATION FUNCTION ────────────────────────────────────────────────────
def build_cbse_prompt(question, student_answer, class_level, topic, marks):
    """
    Build a structured prompt using official CBSE CBE competency framework.
    Sources: CBSE Learning Standards (Azim Premji), Scientific Literacy Framework (ACER/PISA)
    """

    class_data = CLASS_CONTENT[class_level]
    bloom_focus = class_data["bloom_focus"]
    pisa_focus = class_data["pisa_focus"]

    bloom_desc = "\n".join([
        f"  {level}: {data['description']} (CBSE weight: {data['cbse_weight']})"
        for level, data in BLOOM_LEVELS.items()
    ])

    comp_desc = "\n".join([
        f"  {cid} - {data['name']}: {data['description']}"
        for cid, data in SCIENCE_COMPETENCIES.items()
    ])

    prompt = f"""You are a CBSE Science teacher and assessment specialist evaluating a Class {class_level} student's answer.

## EVALUATION FRAMEWORK
You must evaluate using the official CBSE Competency-Based Education (CBE) framework aligned to:
- CBSE Learning Standards Framework - Science (Azim Premji University / CBSE)
- CBSE Scientific Literacy Competencies (CBSE + ACER + PISA 2018)
- NEP 2020 mandate for higher-order thinking assessment

## BLOOM'S COGNITIVE LEVELS (Revised Bloom's Taxonomy - CBSE adapted)
{bloom_desc}

For Class {class_level}, the expected cognitive range is: {bloom_focus}

## CBSE SCIENTIFIC LITERACY COMPETENCIES (PISA-aligned)
{comp_desc}

For Class {class_level}, primary competency focus is: {pisa_focus}

## QUESTION TO EVALUATE
Topic: {topic}
Class: {class_level}
Marks: {marks}
Question: {question}

## STUDENT'S ANSWER
{student_answer}

## YOUR TASK
Evaluate this answer and return ONLY a valid JSON object with exactly this structure:

{{
  "bloom_level_achieved": "exact level label from L1/L2/L3/L4",
  "bloom_level_expected": "what level is expected for Class {class_level} for this question type",
  "pisa_competency": "which of C1/C2/C3 is primarily being tested",
  "cbse_competency_score": <integer 1-5 where 5=full competency demonstrated>,
  "evidence_from_answer": "specific phrases or sentences from the student's answer that show what they understand",
  "learning_gaps": ["gap 1", "gap 2", "gap 3"],
  "strengths": ["strength 1", "strength 2"],
  "improvement_suggestions": ["specific suggestion 1", "specific suggestion 2", "specific suggestion 3"],
  "teacher_note": "one sentence for the teacher about this student's current level",
  "next_question_suggestion": "a follow-up question to push the student toward the expected Bloom's level"
}}

Return ONLY the JSON. No preamble, no explanation outside the JSON."""

    return prompt


def evaluate_with_ai(question, student_answer, class_level, topic, marks, api_key):
    """Call OpenAI API with CBSE-aligned prompt"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = build_cbse_prompt(question, student_answer, class_level, topic, marks)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw), None

    except ImportError:
        return None, "OpenAI library not installed. Run: pip install openai"
    except json.JSONDecodeError as e:
        return None, f"Could not parse AI response as JSON: {e}"
    except Exception as e:
        return None, f"API error: {str(e)}"


# ── DISPLAY FUNCTIONS ─────────────────────────────────────────────────────────
def display_evaluation(result, class_level, marks):
    """Display the evaluation result in a clean, teacher-friendly format"""

    bloom_colors = {
        "L1 - Remember & Understand": "🔵",
        "L2 - Apply": "🟡",
        "L3 - Analyse": "🟠",
        "L4 - Evaluate & Create": "🔴"
    }

    score = result.get("cbse_competency_score", 0)
    score_color = "🟢" if score >= 4 else "🟡" if score >= 3 else "🔴"

    # ── TOP METRICS ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Competency Score", f"{score}/5 {score_color}")
    with col2:
        achieved = result.get("bloom_level_achieved", "")
        st.metric("Bloom's Level Achieved", f"{bloom_colors.get(achieved, '⚪')} {achieved[:2]}")
    with col3:
        expected = result.get("bloom_level_expected", "")
        st.metric("Expected for Class", f"{bloom_colors.get(expected, '⚪')} {expected[:2]}")
    with col4:
        pisa = result.get("pisa_competency", "")
        st.metric("CBSE Competency", pisa[:2] if pisa else "—")

    st.divider()

    # ── BLOOM'S LADDER VISUAL ──
    st.subheader("📊 Bloom's Taxonomy Level")
    levels = list(BLOOM_LEVELS.keys())
    for lvl in levels:
        icon = "✅" if lvl == result.get("bloom_level_achieved") else (
               "🎯" if lvl == result.get("bloom_level_expected") else "⬜")
        label = ""
        if lvl == result.get("bloom_level_achieved") and lvl == result.get("bloom_level_expected"):
            label = " ← **Achieved & Expected**"
        elif lvl == result.get("bloom_level_achieved"):
            label = " ← **Student is here**"
        elif lvl == result.get("bloom_level_expected"):
            label = " ← **Target for this class**"
        st.markdown(f"{icon} {lvl}{label}")

    st.divider()

    # ── EVIDENCE ──
    st.subheader("🔍 Evidence from Answer")
    st.info(result.get("evidence_from_answer", "No evidence extracted."))

    # ── STRENGTHS & GAPS ──
    col_s, col_g = st.columns(2)
    with col_s:
        st.subheader("✅ Strengths")
        for s in result.get("strengths", []):
            st.success(f"• {s}")

    with col_g:
        st.subheader("⚠️ Learning Gaps")
        for g in result.get("learning_gaps", []):
            st.warning(f"• {g}")

    st.divider()

    # ── IMPROVEMENT SUGGESTIONS ──
    st.subheader("💡 Improvement Suggestions")
    for i, suggestion in enumerate(result.get("improvement_suggestions", []), 1):
        st.markdown(f"**{i}.** {suggestion}")

    # ── TEACHER NOTE ──
    st.divider()
    col_t, col_n = st.columns([1, 1])
    with col_t:
        st.subheader("📝 Teacher Note")
        st.markdown(f"*{result.get('teacher_note', '')}*")
    with col_n:
        st.subheader("➡️ Suggested Next Question")
        st.markdown(f"> {result.get('next_question_suggestion', '')}")

    # ── CBSE COMPETENCY REFERENCE ──
    with st.expander("📚 CBSE Competency Framework Reference"):
        pisa_key = result.get("pisa_competency", "")[:2]
        if pisa_key in SCIENCE_COMPETENCIES:
            comp = SCIENCE_COMPETENCIES[pisa_key]
            st.markdown(f"**{comp['name']}**")
            st.markdown(comp['description'])
            st.markdown(f"*What to look for: {comp['what_to_look_for']}*")
        st.markdown("---")
        st.markdown("**Sources:** CBSE Learning Standards Framework - Science (Azim Premji University) | "
                    "CBSE Scientific Literacy Framework (CBSE + SAS + ACER/PISA 2018) | NEP 2020")


# ── MAIN APP ──────────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown("## 🎓 AI Competency-Based Classroom Evaluator")
    st.markdown("**CBSE Science | Classes VI–X** | Aligned to NEP 2020 · CBSE CBE Framework · PARAKH Guidelines")
    st.divider()

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        mode = st.radio("Mode", ["🎮 Demo Mode", "🤖 AI Mode (OpenAI)"])
        api_key = ""
        if "AI Mode" in mode:
            api_key = st.text_input("OpenAI API Key", type="password")
            st.caption("Your key is never stored.")

        st.divider()
        st.markdown("### 📋 CBSE Framework")
        st.markdown("**Cognitive Levels (Bloom's)**")
        for level, data in BLOOM_LEVELS.items():
            st.caption(f"**{level[:2]}** — {data['description'][:40]}...")

        st.divider()
        st.markdown("**Scientific Literacy Competencies**")
        for cid, comp in SCIENCE_COMPETENCIES.items():
            st.caption(f"**{cid}** — {comp['name']}")

        st.divider()
        st.markdown("**Sources**")
        st.caption("CBSE Learning Standards - Science (Azim Premji University)")
        st.caption("Scientific Literacy Framework (CBSE + ACER/PISA)")
        st.caption("PARAKH Assessment Guidelines (NCERT)")
        st.caption("NEP 2020 | NCFSE 2023")

    # Main form
    st.markdown("### 📝 Enter Evaluation Details")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        class_level = st.selectbox(
            "Class", ["VI", "VII", "VIII", "IX", "X"],
            help="CBSE class determines expected Bloom's level and competency focus"
        )
    with col2:
        class_topics = CLASS_CONTENT[class_level]["topics"]
        topic = st.selectbox("Topic / Chapter", class_topics)
    with col3:
        marks = st.selectbox("Marks", [1, 2, 3, 4, 5], index=2,
                              help="Marks allocated to this question")

    # Show expected levels for selected class
    with st.expander(f"📊 Expected Competency Level for Class {class_level}"):
        cd = CLASS_CONTENT[class_level]
        st.info(f"**Bloom's focus:** {cd['bloom_focus']}")
        st.info(f"**PISA competency focus:** {cd['pisa_focus']}")

    question = st.text_area(
        "Question",
        placeholder="E.g. Explain the process of photosynthesis and why it is important for all living organisms.",
        height=80
    )

    student_answer = st.text_area(
        "Student's Answer",
        placeholder="Paste or type the student's answer here...",
        height=150
    )

    evaluate_btn = st.button("🔍 Evaluate Answer", type="primary", use_container_width=True)

    # Evaluation
    if evaluate_btn:
        if not question.strip() or not student_answer.strip():
            st.error("Please enter both the question and student answer.")
            return

        with st.spinner("Evaluating against CBSE CBE framework..."):

            if "Demo" in mode:
                result = DEMO_RESPONSES["basic"]
                st.success("✅ Demo evaluation complete (using sample data)")
            else:
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar.")
                    return
                result, error = evaluate_with_ai(question, student_answer, class_level, topic, marks, api_key)
                if error:
                    st.error(f"Error: {error}")
                    return
                st.success("✅ AI evaluation complete")

        st.divider()
        st.markdown(f"### 📊 Evaluation Result — Class {class_level} | {topic}")
        display_evaluation(result, class_level, marks)

        # Save to history
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "class": class_level,
            "topic": topic,
            "marks": marks,
            "question": question[:60] + "...",
            "bloom_achieved": result.get("bloom_level_achieved", ""),
            "bloom_expected": result.get("bloom_level_expected", ""),
            "score": result.get("cbse_competency_score", 0),
            "pisa_competency": result.get("pisa_competency", "")
        })

        # Download button
        st.divider()
        download_data = json.dumps({
            "metadata": {
                "class": class_level,
                "topic": topic,
                "marks": marks,
                "question": question,
                "student_answer": student_answer,
                "evaluated_at": datetime.datetime.now().isoformat(),
                "framework": "CBSE CBE | NEP 2020 | PARAKH"
            },
            "evaluation": result
        }, indent=2, ensure_ascii=False)

        st.download_button(
            "⬇️ Download Evaluation Report (JSON)",
            data=download_data,
            file_name=f"cbse_eval_class{class_level}_{topic[:20].replace(' ', '_')}.json",
            mime="application/json"
        )

    # History tab
    st.divider()
    if "history" in st.session_state and st.session_state.history:
        with st.expander(f"📋 Evaluation History ({len(st.session_state.history)} evaluations this session)"):
            df = pd.DataFrame(st.session_state.history)
            df.columns = ["Time", "Class", "Topic", "Marks", "Question", "Bloom Achieved", "Bloom Expected", "Score /5", "PISA Competency"]
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "⬇️ Download History as CSV",
                data=csv,
                file_name="cbse_evaluation_history.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()
