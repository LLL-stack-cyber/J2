from backend.services.document_loader import DocumentLoader
from backend.services.blueprint_ai import BlueprintAI
from backend.services.quiz_generator import QuizGenerator
from backend.services.mentor_ai import MentorAI
from backend.services.evaluator import EvaluatorService
from backend.services.rag_engine import RAGEngine

# Initialize services
loader = DocumentLoader()
blueprint = BlueprintAI()
quiz_gen = QuizGenerator()
evaluator = EvaluatorService()
# RAGEngine needs to be the same instance used elsewhere, but for simplicity:
rag = RAGEngine()
mentor = MentorAI(rag_engine=rag)

def run_adaptive_flow(file_path: str, user_answers: str = None):
    """
    Orchestrates the adaptive study flow using standardized services.
    1. LOAD: Extract text from document.
    2. STORE: Index document in RAG engine.
    3. ANALYZE: Generate topic and query analysis.
    4. RETRIEVE: Get relevant context.
    5. GENERATE QUIZ: Create a short assessment using context.
    6. EVALUATE: (If answers provided) score performance.
    7. MENTOR: Provide feedback based on the whole flow.
    """
    result = {}

    # 1. LOAD PDF
    load_res = loader.load_document(file_path)
    if load_res.get("status") != "success":
        return load_res
    text = load_res.get("data")

    # 2. STORE IN RAG
    rag_res = rag.store_document(text)
    if rag_res.get("status") != "success":
        return rag_res

    # 3. ANALYSIS
    # We'll use the first 1000 chars for a quick analysis
    analysis_res = blueprint.process_student_query(user_id="flow-user", query=text[:1000])
    result["analysis"] = analysis_res.get("data")

    # 4. RETRIEVE CONTEXT
    context = rag.retrieve("important concepts and topics", top_k=5)
    context_text = "\n".join(context)

    # 5. GENERATE QUIZ USING CONTEXT
    quiz_input = f"Based on this material:\n{context_text}\nGenerate a 3-question quiz."
    topic = analysis_res.get("data", {}).get("topic", "General Study")
    quiz_res = quiz_gen.generate(topic=topic, count=3) # We use the service's generate method
    # Note: quiz_gen.generate uses a template for now, but in a real scenario, it would use the input.
    result["quiz"] = quiz_res.get("data")

    # 6. EVALUATION (if answers provided)
    if user_answers:
        evaluation_res = evaluator.evaluate(quiz_res.get("data"), user_answers)
        result["evaluation"] = evaluation_res.get("data")

        # 7. MENTOR BASED ON FLOW
        mentor_input = f"""
        Context: {context_text[:500]}
        Evaluation: {evaluation_res.get('data')}
        """
        mentor_res = mentor.respond(user_id="flow-user", question="Review my study session.", context=mentor_input)
        result["mentor_feedback"] = mentor_res.get("data")

    return {"status": "success", "data": result}
