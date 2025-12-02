"""
Test script to verify Scrapy can fetch and display HTML from Common Crawl index
"""
import scrapy
from scrapy.crawler import CrawlerProcess

def test_scrapy_fetch():
    print("\n" + "="*80)
    print("STARTING SCRAPY HTML FETCH TEST")
    print("="*80 + "\n")
    
    index_url = "https://data.commoncrawl.org/crawl-data/index.html"
    html_result = {}

    class CrawlIndexSpider(scrapy.Spider):
        name = "crawl_index_test"
        start_urls = [index_url]
        
        def parse(self, response):
            html_result['content'] = response.text
            html_result['status'] = response.status
            html_result['url'] = response.url
            print(f"\n[SCRAPY] Response Status: {response.status}")
            print(f"[SCRAPY] Response URL: {response.url}")
            print(f"[SCRAPY] HTML Length: {len(response.text)} characters\n")

    # Configure Scrapy with minimal logging
    process = CrawlerProcess(settings={
        "LOG_ENABLED": True,
        "LOG_LEVEL": "INFO",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    
    process.crawl(CrawlIndexSpider)
    print("\n[TEST] Starting Scrapy crawler...")
    process.start()
    
    # Print results
    print("\n" + "="*80)
    print("SCRAPY FETCH RESULTS")
    print("="*80)
    
    if html_result.get('content'):
        html_content = html_result['content']
        print(f"\n[SUCCESS] Fetched HTML successfully!")
        print(f"[INFO] Status Code: {html_result.get('status')}")
        print(f"[INFO] URL: {html_result.get('url')}")
        print(f"[INFO] Content Length: {len(html_content)} characters")
        
        print("\n" + "="*80)
        print("HTML CONTENT PREVIEW (First 2000 characters)")
        print("="*80 + "\n")
        print(html_content[:2000])
        
        print("\n" + "="*80)
        print("HTML CONTENT PREVIEW (Last 1000 characters)")
        print("="*80 + "\n")
        print(html_content[-1000:])
        
        # Test parsing for CC-MAIN links
        print("\n" + "="*80)
        print("PARSING TEST - Looking for CC-MAIN links")
        print("="*80 + "\n")
        
        from parsel import Selector
        selector = Selector(text=html_content)
        
        # Try different CSS selectors
        print("[TEST] Trying selector: 'tr td a::text'")
        all_links = selector.css('tr td a::text').getall()
        print(f"[RESULT] Found {len(all_links)} links in <tr><td><a> tags")
        
        cc_main_links = [link for link in all_links if link.startswith('CC-MAIN-')]
        print(f"[RESULT] Found {len(cc_main_links)} CC-MAIN links")
        
        if cc_main_links:
            print("\n[SUCCESS] Sample CC-MAIN links found:")
            for i, link in enumerate(cc_main_links[:10], 1):
                print(f"  {i}. {link}")
        else:
            print("\n[WARNING] No CC-MAIN links found!")
            print("\n[DEBUG] All links found:")
            for i, link in enumerate(all_links[:20], 1):
                print(f"  {i}. {link}")
    else:
        print("\n[ERROR] Failed to fetch HTML content!")
    
    print("\n" + "="*80)
    print("TEST COMPLETED")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_scrapy_fetch()
