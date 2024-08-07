from odoo import models, fields, api, _
from datetime import date
import logging
import os
import json
import ast
from odoo.exceptions import ValidationError, UserError
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from dotenv import load_dotenv

_logger = logging.getLogger(__name__)

load_dotenv()


class OpenAIModelFee(BaseModel):
    title: str = Field(..., description="Title")
    body: str = Field(..., description="body")
    img: str = Field(..., alias="img", description="Article Img")
    link: str = Field(..., alias="link", description="a.article-link")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    monitor_partner = fields.Boolean(string="Monitor Omni News")

    def _scrape_partner_news(self):
        crawler = WebCrawler()
        crawler.warmup()

        # Define the URL
        url = 'https://omni.se/senaste'

        def run_crawler_with_retries(news_url, crawl_instruction, retries=5):
            attempt = 0
            while attempt < retries:
                result = crawler.run(
                    url=news_url,
                    word_count_threshold=1,
                    extraction_strategy=LLMExtractionStrategy(
                        provider="openai/gpt-4o",
                        api_token=os.getenv('OPENAI_API_KEY'),
                        schema=OpenAIModelFee.schema(),
                        extraction_type="model_json_schema",
                        instruction=crawl_instruction
                    ),
                    bypass_cache=True,
                )

                if news := result.extracted_content:
                    message = ""
                    for new_content in json.loads(news):
                        message += f"<strong>{new_content.get('title')}</strong>"
                        message += (f"<p>{new_content.get('summary')}<br/>{new_content.get('url')}"
                                    f"<br/>{new_content.get('img')}</p>")
                    partner.message_post(body=message)
                    return news
                attempt += 1
                logging.warning(f"Retrying... Attempt {attempt}/{retries}")
            return None

        for partner in self.env['res.partner'].search([('monitor_partner', '=', True)], limit=1):
            instruction = f"""
                Crawl the website and extract news articles that mention {partner.name}. Ensure that the articles
                are relevant to the context of {partner.name} and exclude any unrelated banners, ads, or general
                content.
                Each extracted article should be in the following JSON format:
                {{
                    "title": "Title of the article",
                    "url": "URL of the article",
                    "summary": "Brief summary of the article",
                    "img": "URL of the article image"
                }}.
            """

            # Run the crawler with retries
            extracted_content = run_crawler_with_retries(url, instruction)

            if extracted_content:
                logging.info(extracted_content)
            else:
                logging.error(f"Failed to extract content for {partner.name} after multiple attempts")


