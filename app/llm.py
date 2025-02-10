import os
import glob
import subprocess
import argparse
import tempfile
import tiktoken
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process a GitHub repo with repo-to-text and upload it to Gemini.")
    parser.add_argument("repo_url", help="GitHub repository URL to process")
    parser.add_argument("--question", default="What's this software about? Tell me the compatible disciplines.", help="Question to ask Gemini")
    args = parser.parse_args()

    # Clone the GitHub repository into a temporary folder
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Cloning {args.repo_url} into {temp_dir}...")
        subprocess.run(["git", "clone", args.repo_url, temp_dir], check=True)

        # Run the repo-to-text command in the repository directory
        subprocess.run(["repo-to-text"], cwd=temp_dir, check=True)

        # Retrieve all .txt files generated in the repository directory
        txt_files = glob.glob(os.path.join(temp_dir, "*.txt"))

        # Combine contents of all text files into a single string
        combined_text = ""
        for file in txt_files:
            with open(file, "r", encoding="utf-8") as f:
                combined_text += f.read() + "\n"
                
        # Limit combined_text to 950000 tokens
        limiter_encoding = tiktoken.get_encoding("cl100k_base")
        tokens = limiter_encoding.encode(combined_text)
        
        print(f"Original amount of tokens: {len(tokens)}")
        # This is the limit for Gemini
        if len(tokens) > 950000:
            tokens = tokens[:800000]
            combined_text = limiter_encoding.decode(tokens)
                
        # Save the combined text to a new file
        combined_file_path = os.path.join(temp_dir, "combined_repo.txt")
        with open(combined_file_path, "w", encoding="utf-8") as f:
            f.write(combined_text)

        # Upload the combined file to Gemini
        my_file = client.files.upload(file=combined_file_path)


        response = client.models.count_tokens(
            model='gemini-2.0-flash',
            contents=[args.question, my_file],
        )

        real_tokens = int(response.total_tokens)

        if real_tokens < 990000:
            # Generate the content response using Gemini
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[args.question, my_file]
            )

            print(response.text)

            # Count tokens in the combined document and the output
            encoding = tiktoken.get_encoding("cl100k_base")
            doc_token_count = len(encoding.encode(combined_text))
            output_token_count = len(encoding.encode(response.text))
            print(f"Document token count: {doc_token_count}")
            print(f"Output token count: {output_token_count}")
        else:
            print(f"The input is too long to be processed by Gemini. {real_tokens}")

        # Delete the uploaded file from Gemini
        delete_response = client.files.delete(name=my_file.name)
        print(delete_response)





if __name__ == "__main__":
    main()