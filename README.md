# News Digest

A Langchain & LLM based news digest tool that generates bite-sized news summaries based on user-provided keywords.

## Description

This script uses the GNews API to fetch news articles based on specified keywords and then leverages Google's Gemini LLM via Langchain to generate a concise and engaging news digest.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/news-digest.git
   cd news-digest
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key:**
   Create a `.env` file in the root directory of the project and add your Gemini API key as follows:
   ```
   GEMINI_API_KEY="your-api-key-here"
   ```

## Usage

Run the script from the command line, providing one or more keywords as arguments:

```bash
python news_digest_gemini.py <keyword1> <keyword2> ...
```

### Example

```bash
python news_digest_gemini.py "artificial intelligence" "machine learning"
```
