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
        # Load the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        
        # 1. Prepare Input
        # Format the diff for the model. A simple prompt helps guide the model.
        input_prompt = f"Review the following code change for potential bugs or improvements: {diff_text}"
        
        input_ids = tokenizer.encode(input_prompt, 
                                     return_tensors="pt", 
                                     max_length=512, 
                                     truncation=True)
        
        # 2. Generate Output (the review comment)
        output_ids = model.generate(
            input_ids,
            max_length=MAX_LENGTH,
            num_beams=5, # Use beam search for higher quality
            temperature=0.7,
            no_repeat_ngram_size=2 # Helps prevent repetitive text
        )
        
        # 3. Decode and Clean the result
        comment = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        
        # Simple cleanup (models sometimes add extra, unwanted text)
        if comment.startswith("Review:"):
            comment = comment.replace("Review:", "", 1).strip()
            
        return comment

    except Exception as e:
        return f"ERROR: Could not generate review. Exception: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python review_code.py <path_to_diff_file_or_diff_string>")
        sys.exit(1)

    # In a real DevOps setup, the CI system would pipe the diff content here.
    diff_content = sys.argv[1]
    
    # Simple example diff: fixing a typo
    example_diff = """
--- a/src/utils.py
+++ b/src/utils.py
@@ -1,4 +1,4 @@
 def log_message(msg):
-    # Important: Ensure message is logged corectly
+    # Important: Ensure message is logged correctly
     print(f"LOG: {msg}")
"""
    
    # Use the example diff for testing, or assume input from command line
    print(f"Processing diff:\n{example_diff}\n")
    
    review = generate_review_comment(example_diff)
    
    print("--- Generated AI Review Comment ---")
    print(review)
    print("-----------------------------------")