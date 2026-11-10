import json 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models.models import Article


# creating the app instance
app = FastAPI()

# CORS origins configuration is needed to allow frontend requests to be made the server
# creating list of origins to allow CORS requests
list = ["http://localhost/:5000",
        "http://localhost/:8000",
        "https://localhost/:5000"]

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# load json articles from the file
with open('data/articles.json', 'r') as f:
    articles = [Article(**article) for article in json.load(f)]

@app.get("/articles", response_model=List[Article])
async def get_articles():
    return articles

@app.get("/articles/{id}", response_model=Article)
async def get_article(id: int):
    for article in articles:
        if article.id == id:
            return article
    raise HTTPException(status_code=404, detail="Article not found")

@app.get("/articles{title}", response_model=List[Article])
def get_articles_by_title(title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Error: Title is required")
    
    matching_articles = [article for article in articles if title.lower() in article.title.lower()]
    
    if not matching_articles:
        raise HTTPException(status_code=404, detail="No articles found with that title")
    
    return matching_articles

@app.delete("/articles")
async def delete_article(id: Optional [int] = None, title: Optional[str] = None):
    if not id and not title:
        raise HTTPException(status_code=400, detail="Error: Either id or title is required to delete an article")
    
    for article in articles:
        if article.id == id:
            articles.remove(article)
            return {"message": "Article deleted successfully"}
        elif article.title == title:
            articles.remove(article)
            return {"message": "Article deleted successfully"}
        
    raise HTTPException(status_code=404, detail="Article not found")

@app.get("/")
async def root():
    return {"message": "FastAPI spike"}
