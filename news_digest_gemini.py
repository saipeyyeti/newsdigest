import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from gnews import GNews
from datetime import datetime

class NewsDigestGenerator:
    def __init__(self, gemini_api_key):
        """Initialize with Gemini API key."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.3
        )
        self.gnews = GNews(language='en', max_results=10)
        
    def search_news(self, keywords):
        """Search Google News for given keywords."""
        if isinstance(keywords, list):
            query = ' OR '.join(keywords)
        else:
            query = keywords
            
        articles = self.gnews.get_news(query)
        return articles
    
    def generate_digest(self, keywords):
        """Generate bite-sized news digest."""
        # Search for news
        articles = self.search_news(keywords)
        
        if not articles:
            return "No news articles found for the given keywords."
        
        # Format articles for LLM
        news_text = "\n\n".join([
            f"Title: {article['title']}\n"
            f"Description: {article['description']}\n"
            f"Publisher: {article['publisher']['title']}\n"
            f"Date: {article['published date']}"
            for article in articles[:5]  # Limit to top 5
        ])
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a professional news editor creating concise, engaging news digests."),
            ("user", """Based on the following news articles about {keywords}, create a bite-sized news digest summary.

News Articles:
{news_text}

Requirements:
- Keep it under 150 words
- Highlight the most important developments
- Use clear, engaging language
- Focus on facts and key takeaways
- Start with the most significant news

Digest:""")
        ])
        
        # Generate summary
        chain = prompt | self.llm
        response = chain.invoke({
            "keywords": ', '.join(keywords) if isinstance(keywords, list) else keywords,
            "news_text": news_text
        })
        
        return response.content
    
    def print_digest(self, keywords):
        """Print formatted news digest."""
        print(f"\n{'='*60}")
        print(f"NEWS DIGEST: {', '.join(keywords) if isinstance(keywords, list) else keywords}")
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        digest = self.generate_digest(keywords)
        print(digest)
        print(f"\n{'='*60}\n")


# Example usage
if __name__ == "__main__":
    import sys
    
    # Set your Gemini API key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
    
    # Get keywords from command line arguments
    if len(sys.argv) > 1:
        keywords = sys.argv[1:]
    else:
        print("Usage: python script.py <keyword1> <keyword2> ...")
        print("Example: python script.py 'artificial intelligence' 'machine learning'")
        sys.exit(1)
    
    # Initialize generator
    generator = NewsDigestGenerator(GEMINI_API_KEY)
    
    # Generate and print digest
    generator.print_digest(keywords)