import requests
import os
from openai import AzureOpenAI, OpenAI
from flask import Flask, jsonify, request
# from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
load_dotenv()
def get_news_summary():
    global current_keyword
    prompt_response = ""
    links = []
    publisheddate = []
    subscription_key = os.getenv("subscription_key")
    current_keyword = os.getenv('keyword')
    apitype = "azure"
    link = "https://api.bing.microsoft.com/v7.0/search"
    try:
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {"q": current_keyword, "textDecorations": True, "textFormat": "Raw", "responseFilter": "News", "mkt": "en-IN"}
        response = requests.get(link, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        for newslink in search_results['news']['value']:
            links.append(newslink['url'])
            publisheddate.append(newslink['datePublished'])
    except Exception as e:
        print(f'Error in fetching news data from Bing Search API: {e}')
        exit()
    if apitype == "azure":
        client = AzureOpenAI(
            azure_endpoint = os.getenv("apibase"),
            api_version = os.getenv("apiversion"),
            api_key = os.getenv("apikey")
        )
        try:
            print("Scraping each link and generating Summary of the article with Azure Open AI")
            prompt_request = f"Act as a Webpage Scarper and scrape each link present in this list of links {links}.Generate a detailed and well-explained summary of the text present in each link in a JSON array with description, URL as key-value pairs. Only add text content from the article and do not add anything else on your own. Also, extract the published date in Day-Month-Year format from the list {publisheddate} and the publisher for each URL and add it to the JSON array."
            response = client.completions.create(
                model = "gpt-35-turbo",
                prompt = prompt_request,
                temperature = 0.7,
                max_tokens = 2000,
                top_p = 0.6
        )
            prompt_response = response.choices[0].text.strip()
            print("Response from Azure Open AI \n " + prompt_response)
        except Exception as e:
            print(f'Error in Text Content Scraping using Azure Open AI: {e}')
            exit()
        return prompt_response
    else:
        client = OpenAI(
            api_key = os.getenv("openapi_key")
        )
        try:
            print("Scraping each link and generating Summary of the article with Open AI")
            prompt_request = f"Act as a Webpage Scarper and scrape each link present in this list of links {links}.Generate a detailed and well-explained summary of the text present in each link in a JSON array with description, URL as key-value pairs. Only add text content from the article and do not add anything else on your own. Also, extract the published date in Day-Month-Year format from the list {publisheddate} and the publisher for each URL and add it to the JSON array."
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                {
                    "role": "user",
                    "content": prompt_request
                }
            ],
                temperature=0.5,
                max_tokens=2000,
                top_p=0.6
            )
            prompt_response = response.choices[0].text.strip()
            print("Response from Open AI \n " + prompt_response)
        except Exception as e:
            print(f'Error in Text Content Scraping using Open AI: {e}')
            exit()
        return prompt_response
getnews = get_news_summary()
print(getnews)
