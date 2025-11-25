import tiktoken

def split_ebook_into_chunks(file_path, chunk_size=1000, encoding_name="cl100k_base"):
    """
    Split an ebook text file into chunks of approximately chunk_size tokens.

    Args:
        file_path: Path to the text file
        chunk_size: Target number of tokens per chunk (default: 1000)
        encoding_name: Tokenizer encoding to use (default: cl100k_base for GPT-4)

    Returns:
        List of text chunks
    """
    # Initialize tokenizer
    encoding = tiktoken.get_encoding(encoding_name)

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Tokenize the entire text
    tokens = encoding.encode(text)

    # Split into chunks
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

def save_chunks(chunks, output_prefix="chunk"):
    """Save chunks to separate files."""
    for i, chunk in enumerate(chunks, 1):
        output_file = f"{output_prefix}_{i:04d}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        print(f"Saved {output_file} ({len(chunk)} characters)")

# Usage
if __name__ == "__main__":
    input_file = "1.txt"  # Change to your file path

    # Split the ebook
    chunks = split_ebook_into_chunks(input_file, chunk_size=1000)

    print(f"Split into {len(chunks)} chunks")

    # Save chunks to separate files
    save_chunks(chunks, output_prefix="ebook_chunk")

    # Or work with chunks in memory
    # for i, chunk in enumerate(chunks, 1):
    #     print(f"Chunk {i}: {len(chunk)} characters")
