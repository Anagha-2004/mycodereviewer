# review_code.py
import sys
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# --- Configuration ---
# Use a model specialized in code tasks (e.g., CodeReviewer, CodeT5)
MODEL_NAME = "microsoft/codereviewer" 
MAX_LENGTH = 150 # Max length for the generated comment

def generate_review_comment(diff_text: str):
    """Loads a transformer model and generates a review comment."""
    try:
        # Load the model and tokenizer (This happens only once per job run)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        
        # 1. Prepare Input
        input_prompt = f"Review the following code change for potential bugs or improvements: {diff_text}"
        
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
        # Return a clean error message, which will be the review comment
        return f"ERROR: Could not generate review. Exception: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # In the CI environment, sys.argv[1] should be the diff content
        print("ERROR: Missing diff content argument.")
        sys.exit(1)

    diff_content = sys.argv[1]
    
    review = generate_review_comment(diff_content)
    
    # ⚠️ CRITICAL: Print ONLY the review comment to standard output
    print(review)