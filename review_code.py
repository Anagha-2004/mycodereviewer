import sys
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# --- Configuration ---
MODEL_NAME = "microsoft/codereviewer" 
MAX_LENGTH = 150 

def generate_review_comment(diff_text: str):
    """Loads a transformer model and generates a review comment."""
    try:
        # Load the model and tokenizer (from cache if available)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        
        # 1. Prepare Input - Strong, directive prompt for better bug detection
        input_prompt = f"Critique this code change. Specifically check for logical errors, security risks (like division by zero), and ensure variables are used correctly. Code diff: {diff_text}"
        
        input_ids = tokenizer.encode(input_prompt, 
                                     return_tensors="pt", 
                                     max_length=512, 
                                     truncation=True)
        
        # 2. Generate Output (the review comment)
        output_ids = model.generate(
            input_ids,
            max_length=MAX_LENGTH,
            num_beams=5,
            temperature=0.7,
            no_repeat_ngram_size=2
        )
        
        # 3. Decode and Clean the result
        comment = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        
        if comment.startswith("Review:"):
            comment = comment.replace("Review:", "", 1).strip()
            
        return comment

    except Exception as e:
        # Return a clean error message if the model fails
        return f"ERROR: Could not generate review due to model failure. Exception: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # This error is usually caught by the GitHub Action workflow
        print("ERROR: Missing diff content argument.")
        sys.exit(1)

    diff_content = sys.argv[1]
    review = generate_review_comment(diff_content)
    
    # ⚠️ FINAL LOGIC: Check for critical keywords to set the header ⚠️
    critical_keywords = ["bug", "error", "risk", "security", "fail", "incorrect", "issue", "vulnerability", "zero"]
    
    # Check if the generated review contains any critical keywords (case-insensitive)
    is_critical = any(keyword in review.lower() for keyword in critical_keywords)
    
    # Format the final output with a strong header based on content
    if is_critical:
        final_output = "🚨 **CRITICAL AI REVIEW ALERT:** 🚨\n\n" + review
    else:
        final_output = "✅ **AI Code Reviewer Suggestion (No Major Issues Found):**\n\n" + review
        
    # Print ONLY the final classified output to standard output
    print(final_output)