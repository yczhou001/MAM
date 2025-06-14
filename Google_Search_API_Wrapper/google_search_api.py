import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional
import logging
dotenv_path = '/your/path/to/example.env'
load_dotenv(dotenv_path)

class SearchResults:
    def __init__(self, results):
        self.results = results

    def __str__(self):
        output = ""
        for result in self.results:
            output += "---\n"
            output += f"Title: {result.get('title', 'Title not found')}\n"
            output += f"Link: {result.get('link', 'Link not found')}\n"
            if 'snippet' in result:
                output += f"Snippet: {result['snippet']}\n"
            if 'image' in result:
                output += f"Image: {result['image']}\n"
            output += "---\n"
        return output

class GoogleSearchAPI:
    def __init__(self):
        self.base_url = ""
        self.headers = {"Content-Type": "application/json"}

        self.api_key = os.getenv('api_key')
        if not self.api_key:
            raise ValueError("API key not found. Set the api_key environment variable.")
        self.cx = os.getenv('cx')
        if not self.cx:
            raise ValueError("CX (Search Engine ID) not found. Set the cx environment variable.")

    def response(self, method: str, query: str, max_results: int = 10) -> SearchResults:
        if not query:
            raise ValueError("Query not found. Please enter a query and try again.")
        
        query = query.replace(" ", "+")
        
        all_results = []
        total_fetched = 0
        start_index = 1

        while total_fetched < max_results:
            num_results = min(max_results - total_fetched, 10)  # API allows max 10 results at a time
            search_type_param = '&searchType=image' if method == 'image' else ''
            url = f"{self.base_url}?q={query}&key={self.api_key}&cx={self.cx}{search_type_param}&num={num_results}&start={start_index}"
            
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                search_results = response.json().get("items", [])
                all_results.extend(search_results)

                if "nextPage" in response.json()["queries"]:
                    start_index = response.json()["queries"]["nextPage"][0]["startIndex"]
                    total_fetched += len(search_results)
                else:
                    break
            except requests.exceptions.RequestException as e:
                logging.error(f"An error occurred: {e}")
                break

        formatted_results = [self.results(result, method) for result in all_results[:max_results]]
        return SearchResults(formatted_results)

    def results(self, result: Dict, search_type: str) -> Dict:
        if search_type == 'image':
            return {
                "title": self.field_search(result, "title"),
                "link": self.field_search(result, "image.contextLink"),
                "image": self.field_search(result, "link", "image.thumbnailLink")
            }
        else:
            return {
                "link": self.field_search(result, "link", "pagemap.metatags.0.og:url"),
                "title": self.field_search(result, "pagemap.metatags.0.og:title", "pagemap.metatags.0.twitter:title", "title", "pagemap.metatags.0.og:image:alt", "pagemap.metatags.0.twitter:image:alt"),
                "snippet": self.field_search(result, "pagemap.metatags.0.og:description", "pagemap.metatags.0.twitter:description", "snippet")
            }

    def field_search(self, result: Dict, *field_paths: str) -> str:
        for path in field_paths:
            try:
                value = result
                for key in path.split('.'):
                    if isinstance(value, dict):
                        value = value.get(key, {})
                    elif isinstance(value, list) and key.isdigit():
                        index = int(key)
                        if index < len(value):
                            value = value[index]
                        else:
                            break
                    else:
                        break
                if isinstance(value, str):
                    return value
            except Exception as e:
                logging.error(f"Error extracting {path}: {e}")
            
        return "Not found"
