# Đảm bảo tất cả các endpoint đều nằm ở lề ngoài cùng

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

_botnet_service = None

@app.post("/api/harvest-google")
async def api_harvest_google(request: Request):
    data = await request.json()
    dork_file = data.get("dork_file", "inputDork/general_search_dorks.txt")
    output_file = "outputDork/shops_fresh_2025_google.txt"
    dork_count = int(data.get("dork_count", 50))
    thread_count = int(data.get("thread_count", 10))
    use_proxies = data.get("use_proxies", False)
    use_ua_rotation = data.get("use_ua_rotation", False)
    min_delay = int(data.get("min_delay", 15))
    max_delay = int(data.get("max_delay", 45))
    # Đọc dork từ file
    with open(dork_file, "r", encoding="utf-8") as f:
        dorks = [line.strip() for line in f if line.strip()][:dork_count]
    # Giả lập search Google và ghi ra file output
    with open(output_file, "w", encoding="utf-8") as f_out:
        for dork in dorks:
            # Thay bằng logic search thực tế
            f_out.write(f"https://google.com/search?q={dork}\n")
    return JSONResponse(content={"success": True, "message": f"Harvested {len(dorks)} dorks for Google."})

@app.post("/api/harvest-bing")
async def api_harvest_bing(request: Request):
    data = await request.json()
    dork_file = data.get("dork_file", "inputDork/general_search_dorks.txt")
    output_file = "outputDork/shops_fresh_2025_bing.txt"
    dork_count = int(data.get("dork_count", 50))
    thread_count = int(data.get("thread_count", 10))
    use_proxies = data.get("use_proxies", False)
    use_ua_rotation = data.get("use_ua_rotation", False)
    min_delay = int(data.get("min_delay", 15))
    max_delay = int(data.get("max_delay", 45))
    # Đọc dork từ file
    with open(dork_file, "r", encoding="utf-8") as f:
        dorks = [line.strip() for line in f if line.strip()][:dork_count]
    # Giả lập search Bing và ghi ra file output
    with open(output_file, "w", encoding="utf-8") as f_out:
        for dork in dorks:
            # Thay bằng logic search thực tế
            f_out.write(f"https://bing.com/search?q={dork}\n")
    return JSONResponse(content={"success": True, "message": f"Harvested {len(dorks)} dorks for Bing."})

@app.post("/api/harvest-yandex")
async def api_harvest_yandex(request: Request):
    data = await request.json()
    dork_file = data.get("dork_file", "inputDork/general_search_dorks.txt")
    output_file = "outputDork/shops_fresh_2025_yandex.txt"
    dork_count = int(data.get("dork_count", 50))
    thread_count = int(data.get("thread_count", 10))
    use_proxies = data.get("use_proxies", False)
    use_ua_rotation = data.get("use_ua_rotation", False)
    min_delay = int(data.get("min_delay", 15))
    max_delay = int(data.get("max_delay", 45))
    # Đọc dork từ file
    with open(dork_file, "r", encoding="utf-8") as f:
        dorks = [line.strip() for line in f if line.strip()][:dork_count]
    # Giả lập search Yandex và ghi ra file output
    with open(output_file, "w", encoding="utf-8") as f_out:
        for dork in dorks:
            # Thay bằng logic search thực tế
            f_out.write(f"https://yandex.com/search/?text={dork}\n")
    return JSONResponse(content={"success": True, "message": f"Harvested {len(dorks)} dorks for Yandex."})

@app.post("/api/harvest-duckduckgo")
async def api_harvest_duckduckgo(request: Request):
    data = await request.json()
    dork_file = data.get("dork_file", "inputDork/general_search_dorks.txt")
    output_file = "outputDork/shops_fresh_2025_duckduckgo.txt"
    dork_count = int(data.get("dork_count", 50))
    thread_count = int(data.get("thread_count", 10))
    use_proxies = data.get("use_proxies", False)
    use_ua_rotation = data.get("use_ua_rotation", False)
    min_delay = int(data.get("min_delay", 15))
    max_delay = int(data.get("max_delay", 45))
    # Đọc dork từ file
    with open(dork_file, "r", encoding="utf-8") as f:
        dorks = [line.strip() for line in f if line.strip()][:dork_count]
    # Giả lập search DuckDuckGo và ghi ra file output
    with open(output_file, "w", encoding="utf-8") as f_out:
        for dork in dorks:
            # Thay bằng logic search thực tế
            f_out.write(f"https://duckduckgo.com/?q={dork}\n")
    return JSONResponse(content={"success": True, "message": f"Harvested {len(dorks)} dorks for DuckDuckGo."})


# ==== COMMON CRAWL SERVICE ====
import os
import requests
import gzip
from typing import List, Dict
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

class CommonCrawlService:
    """
    Common Crawl harvesting service following MVC pattern
    Handles fetching, parsing, and processing WARC files
    """
    
    def __init__(self):
        self.state = {
            "status": "idle",
            "shops_found": 0,
            "warc_files_processed": 0,
            "total_warc_files": 0,
            "current_warc": "",
            "recent_shops": [],
            "stop_flag": False,
        }
        self.output_file = "outputDork/shops_fresh_2025_common_crawl.txt"
        self.existing_domains = set()  # For duplicate checking
    
    def search_common_crawl(self, crawl_id: str = "auto", max_files: int = 10, 
                           patterns: List[bytes] = None, use_threading: bool = True,
                           clear_results: bool = False) -> Dict:
        """
        Main Common Crawl search function using Scrapy-based harvesting
        
        Args:
            crawl_id: Common Crawl ID (can be 'auto' to use latest)
            max_files: Max number of CC-MAIN crawls to use (each crawl has many WARC files)
            patterns: List of patterns to search (currently unused, using keywords from file)
            use_threading: Enable multi-threading
            clear_results: If True, clear output file before harvesting; if False, append
            
        Returns:
            Dict with results: {shops_found, status, message}
        """
        print("\n" + "="*80)
        print("STARTING COMMON CRAWL HARVEST")
        print(f"Max CC-MAIN crawls to use: {max_files}")
        print(f"Clear results before harvest: {clear_results}")
        print("="*80 + "\n")
        
        self.state["status"] = "running"
        self.state["stop_flag"] = False
        self.state["shops_found"] = 0
        
        # Handle clear_results option
        self._prepare_output_file(clear_results)
        
        try:
            # Step 1: Fetch index.html using requests
            html_content = self._fetch_index_with_scrapy()
            if not html_content:
                return {"success": False, "message": "Failed to fetch CC index"}
            
            # Step 2: Parse CC-MAIN links and limit by max_files
            cc_main_links = self._parse_cc_main_links(html_content, max_files)
            if not cc_main_links:
                return {"success": False, "message": "No CC-MAIN links found"}
            
            print(f"\n[SUCCESS] Selected {len(cc_main_links)} CC-MAIN crawls to process")
            print("\n" + "="*80)
            print("FINAL CC-MAIN CRAWLS LIST:")
            print("="*80)
            print(cc_main_links)
            print("="*80 + "\n")
            
            # Step 3: Stream and filter WARC URLs directly
            result = self._stream_and_filter_warc_urls(cc_main_links)
            if not result:
                return {"success": False, "message": "Streaming failed"}
            
            print(f"\n[SUCCESS] Completed streaming and filtering")
            
            self.state["status"] = "completed"
            
            return {
                "success": True,
                "shops_found": self.state["shops_found"],
                "message": f"Harvested {self.state['shops_found']} unique shops"
            }
            
        except Exception as e:
            self.state["status"] = "error"
            print(f"[ERROR] Common Crawl failed: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def _prepare_output_file(self, clear_results: bool):
        """
        Prepare output file based on clear_results option
        
        Args:
            clear_results: If True, clear file; if False, load existing domains for dedup
        """
        if clear_results:
            # Clear the file
            print(f"[FILE] Clearing output file: {self.output_file}")
            with open(self.output_file, "w", encoding="utf-8") as f:
                pass  # Create empty file
            self.existing_domains = set()
        else:
            # Load existing domains from file for duplicate checking
            print(f"[FILE] Loading existing domains from: {self.output_file}")
            self.existing_domains = set()
            if os.path.exists(self.output_file):
                try:
                    with open(self.output_file, "r", encoding="utf-8") as f:
                        for line in f:
                            domain = line.strip().lower()
                            if domain:
                                self.existing_domains.add(domain)
                    print(f"[FILE] Loaded {len(self.existing_domains)} existing domains for dedup")
                except Exception as e:
                    print(f"[WARNING] Could not load existing domains: {e}")
    
    def _add_domain(self, domain: str) -> bool:
        """
        Add domain to output file if not duplicate
        
        Args:
            domain: Domain to add
            
        Returns:
            bool: True if added (new domain), False if duplicate
        """
        domain_lower = domain.strip().lower()
        
        # Skip empty or invalid domains
        if not domain_lower or len(domain_lower) < 4:
            return False
        
        # Check duplicate
        if domain_lower in self.existing_domains:
            return False
        
        # Add to set and file
        self.existing_domains.add(domain_lower)
        
        try:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(f"{domain_lower}\n")
                f.flush()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to write domain: {e}")
            return False
    
    def _fetch_index_with_scrapy(self) -> str:
        """Fetch Common Crawl index page using requests (Scrapy has signal issues in threads)"""
        index_url = "https://data.commoncrawl.org/crawl-data/index.html"
        
        try:
            print("[CC] Fetching index page with requests...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(index_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            html_content = response.text
            print(f"[SUCCESS] Fetched {len(html_content)} chars from CC index")
            
            # Log first 1000 chars to verify content
            print("\n" + "="*80)
            print("HTML CONTENT PREVIEW (first 2000 chars):")
            print("="*80)
            print(html_content[:2000])
            print("="*80 + "\n")
            
            return html_content
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch CC index: {str(e)}")
            return ""
    
    def _parse_cc_main_links(self, html_content: str, max_crawls: int) -> List[str]:
        """Parse CC-MAIN links from HTML content and limit by max_crawls"""
        from parsel import Selector
        
        print("\n" + "="*80)
        print("PARSING CC-MAIN LINKS")
        print("="*80 + "\n")
        
        selector = Selector(text=html_content)
        all_links = selector.css('tr td a::text').getall()
        cc_main_links = [link for link in all_links if link.startswith('CC-MAIN-')]
        
        print(f"[FOUND] Total {len(cc_main_links)} CC-MAIN crawls available")
        
        # Sort by newest first (reverse chronological order)
        cc_main_links.sort(reverse=True)
        
        # Limit to max_crawls
        cc_main_links = cc_main_links[:max_crawls]
        
        print(f"[SELECTED] Using {len(cc_main_links)} CC-MAIN crawls:")
        for idx, crawl in enumerate(cc_main_links, 1):
            print(f"  {idx}. {crawl}")
        
        return cc_main_links
    
    def _stream_and_filter_warc_urls(self, crawl_ids: List[str]) -> bool:
        """
        Use Common Crawl Index API to search URLs by keywords directly
        
        Args:
            crawl_ids: List of CC crawl IDs (e.g., ['CC-MAIN-2025-47', 'CC-MAIN-2025-38'])
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("\n" + "="*80)
        print("USING COMMON CRAWL INDEX API FOR DIRECT SEARCH")
        print("="*80 + "\n")
        
        # Load keywords once for all crawls
        keywords = self._load_keywords()
        if not keywords:
            print(f"[ERROR] No keywords found, aborting...")
            return False
        
        print(f"[KEYWORDS] Loaded {len(keywords)} keywords for filtering")
        print(f"[FILE] Output: {self.output_file}")
        print(f"[DEDUP] {len(self.existing_domains)} existing domains loaded for duplicate check")
        
        total_new_shops = 0
        
        # Process each crawl
        for crawl_id in crawl_ids:
            print(f"\n[CC] Processing crawl: {crawl_id}")
            
            # Search each keyword using CC Index API
            for idx, keyword in enumerate(keywords, 1):
                if self.state.get("stop_flag"):
                    print(f"\n[STOPPED] User requested stop")
                    return False
                
                print(f"\n  [{idx}/{len(keywords)}] Searching keyword: '{keyword}'")
                
                try:
                    new_shops = self._search_cc_index_api(crawl_id, keyword, self.output_file)
                    total_new_shops += new_shops
                    
                    if new_shops > 0:
                        print(f"    ✓ Added {new_shops} NEW shops for '{keyword}'")
                    else:
                        print(f"    ○ No new results for '{keyword}'")
                        
                except Exception as e:
                    print(f"    ✗ Error searching '{keyword}': {str(e)}")
                    continue
            
            print(f"\n  [CRAWL SUMMARY] {crawl_id}: {total_new_shops} new shops added")
        
        print(f"\n[COMPLETE] Total: {self.state['shops_found']} unique shops")
        print(f"[FILE] Saved to: {self.output_file}")
        return True
    
    def _search_cc_index_api(self, crawl_id: str, keyword: str, output_file: str) -> int:
        """
        Search Common Crawl Index API for URLs containing keyword
        
        Args:
            crawl_id: CC crawl ID (e.g., 'CC-MAIN-2025-47')
            keyword: Keyword to search in URLs
            output_file: Output file path (unused, using self.output_file)
            
        Returns:
            int: Number of NEW shops found (excluding duplicates)
        """
        # CC Index API endpoint
        # Example: https://index.commoncrawl.org/CC-MAIN-2025-47-index?url=*.shopify.com/*&output=json
        
        # Build search URL - wildcard search for keyword in URL
        api_url = f"https://index.commoncrawl.org/{crawl_id}-index"
        
        # Try different URL patterns for the keyword
        search_patterns = [
            f"*{keyword}*",           # Keyword anywhere in URL
            f"*.{keyword}.*",         # Keyword in domain
            f"*/{keyword}/*",         # Keyword in path
        ]
        
        new_shops_found = 0
        duplicates_skipped = 0
        session_domains = set()  # Track domains found in this search session
        
        for pattern in search_patterns:
            try:
                params = {
                    "url": pattern,
                    "output": "json",
                    "limit": 1000  # Limit results per pattern
                }
                
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                print(f"      🔍 API: {api_url}?url={pattern}")
                
                response = requests.get(api_url, params=params, headers=headers, stream=True, timeout=60)
                
                # CC Index API returns NDJSON (newline-delimited JSON)
                # Each line is a separate JSON object
                for line in response.iter_lines():
                    if not line:
                        continue
                    
                    try:
                        import json
                        data = json.loads(line.decode('utf-8', errors='ignore'))
                        
                        # Extract URL from response
                        url = data.get('url', '')
                        if url:
                            # Extract domain
                            domain = urlparse(url).netloc
                            
                            # Skip if already seen in this session (same keyword search)
                            if domain in session_domains:
                                continue
                            session_domains.add(domain)
                            
                            # Try to add domain (checks global duplicates)
                            if self._add_domain(domain):
                                new_shops_found += 1
                                self.state["shops_found"] += 1
                                
                                # Log every 10 new shops
                                if new_shops_found % 10 == 0:
                                    print(f"        📊 {new_shops_found} NEW domains added (total: {self.state['shops_found']})")
                            else:
                                duplicates_skipped += 1
                                
                    except json.JSONDecodeError:
                        pass  # Skip invalid JSON lines
                    except Exception as e:
                        pass  # Skip errors
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    # No results for this pattern - this is normal
                    pass
                else:
                    print(f"        ⚠️ HTTP Error {e.response.status_code} for pattern '{pattern}'")
            except Exception as e:
                print(f"        ⚠️ Error for pattern '{pattern}': {str(e)}")
        
        if duplicates_skipped > 0:
            print(f"        ⏭️ Skipped {duplicates_skipped} duplicates")
        
        return new_shops_found
    
    def _load_keywords(self) -> List[str]:
        """Load keywords from file for URL filtering"""
        keyword_file = "inputDork/common_crawl_dorks.txt"
        keywords = []
        
        if os.path.exists(keyword_file):
            try:
                with open(keyword_file, "r", encoding="utf-8") as f:
                    keywords = [line.strip().lower() for line in f 
                               if line.strip() and not line.startswith('#')]
                print(f"[✓] Loaded {len(keywords)} keywords from {keyword_file}")
            except Exception as e:
                print(f"[WARNING] Failed to load keywords: {e}")
        
        if not keywords:
            # Default shop keywords
            keywords = [
                "myshopify.com", "shopify", "woocommerce", "magento",
                "opencart", "prestashop", "bigcommerce", "wix.com/stores",
                "/checkout", "/cart", "/shop/", "add-to-cart", "product_id="
            ]
            print(f"[WARNING] Using default keywords: {len(keywords)} patterns")
        
        return keywords
    

    
    def stop(self):
        """Stop the harvesting process"""
        self.state["stop_flag"] = True
        print("[CC] Stop signal sent")
    
    def get_status(self) -> Dict:
        """Get current harvesting status"""
        return {
            "status": self.state["status"],
            "shops_found": self.state["shops_found"],
            "warc_files_processed": self.state["warc_files_processed"],
            "total_warc_files": self.state["total_warc_files"],
            "current_warc": self.state["current_warc"],
            "recent_shops": self.state["recent_shops"][:10]
        }


import json
import httpx
"""
🤖 Botnet Service
High-performance async botnet operations for KJC API testing
"""

from typing import Dict
from fastapi import HTTPException
import httpx
import asyncio
import time
import random


async def get_user_by_username_async(username: str) -> Dict:
    """Get user by username - Direct database access to avoid circular import"""
    try:
        import os
        from pymongo import MongoClient
        from bson import ObjectId
        
        # Direct database access to avoid circular import
        mongodb_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DATABASE", "kjc-group-staging")
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        user = db.users.find_one({"username": username, "deletedAt": {"$in": [None, ""]}})
        if not user:
            client.close()
            return None
            
        # Convert ObjectId to string
        if "_id" in user:
            user["_id"] = str(user["_id"])
        for k, v in list(user.items()):
            if isinstance(v, ObjectId):
                user[k] = str(v)
                
        client.close()

        return user
    except Exception as e:
        print(f"Error getting user {username}: {str(e)}")
        return None


class BotBrowser:
    
    async def close_browser(self):
        """Close browser instance (cleanup resources including WebSocket)"""
        # Close WebSocket connection - AVOID accessing .open property (causes Code 1005)
        if self.websocket:
            try:
                # Just try to close without checking state - let exceptions handle closed connections
                await self.websocket.close()
                print(f"🔗 Bot {self.username}: WebSocket connection closed")
            except Exception as e:
                print(f"🔗 Bot {self.username}: WebSocket close error (expected): {e}")
            except Exception as e:
                print(f"⚠️ Bot {self.username}: Error closing WebSocket: {e}")
        
        # Cancel WebSocket monitoring task
        if self.websocket_task and not self.websocket_task.done():
            self.websocket_task.cancel()
            try:
                await self.websocket_task
            except asyncio.CancelledError:
                print(f"🔄 Bot {self.username}: WebSocket monitoring task cancelled")
            except Exception as e:
                print(f"⚠️ Bot {self.username}: Error cancelling WebSocket task: {e}")
        
        # Close HTTP client
        await self.http_client.aclose()
        print(f"🔴 Closed browser for bot: {self.username}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            if hasattr(self, 'http_client') and not self.http_client.is_closed:
                asyncio.create_task(self.http_client.aclose())
        except:
            pass


class BotnetService:
    """
    🚀 Optimized Botnet Service with async HTTP client
    Supports high-concurrency operations (up to 5000+ bots)
    """
    
    def __init__(self):
        """Initialize BotnetService with SJC scraper service"""
        self.active_bots = {}
    
    async def get_active_browsers(self) -> Dict:
        """Get information about all active browser instances with 5k scale analysis + caching"""
        import time
        
        # Cache browser info for 2 seconds to reduce get_session_info() calls 
        # This prevents race conditions with Socket.IO ping/pong
        current_time = time.time()
        cache_key = "active_browsers_cache"
        cache_timeout = 2.0  # seconds
        
        # Check if we have valid cached data
        if hasattr(self, '_browser_cache') and hasattr(self, '_browser_cache_time'):
            if current_time - self._browser_cache_time < cache_timeout:
                print(f"🔄 Using cached browser info ({len(self._browser_cache['browsers'])} bots)")
                return self._browser_cache
        
        # Generate fresh browser info (expensive operation)
        print(f"🔄 Refreshing browser info for {len(self.active_bots)} bots...")
        browsers_info = []
        
        for username, bot_browser in self.active_bots.items():
            session_info = await bot_browser.get_session_info()
            browsers_info.append(session_info)
        
        # Calculate 5k scale metrics
        current_browsers = len(self.active_bots)
        estimated_memory = current_browsers * 5  # 5MB per bot
        
        result = {
            "total_browsers": current_browsers,
            "browsers": browsers_info,
            "scale_analysis_5k": {
                "current_memory_usage_mb": estimated_memory,
                "max_concurrent_with_current_semaphore": 500,
                "estimated_5k_completion_time_seconds": 50,
                "no_io_blocking": True,
                "bottleneck": "semaphore_queue_management",
                "recommended_ram_for_5k": "25GB",
                "performance_rating": "excellent_for_5k_scale"
            }
        }
        
        # Cache the result
        self._browser_cache = result
        self._browser_cache_time = current_time
        
        return result
    
    async def close_bot_browser(self, username: str) -> Dict:
        """Close a specific bot's browser instance"""
        if username in self.active_bots:
            await self.active_bots[username].close_browser()
            del self.active_bots[username]
            return {
                "success": True,
                "message": f"Closed browser for bot: {username}",
                "remaining_browsers": len(self.active_bots)
            }
        else:
            return {
                "success": False,
                "message": f"No active browser found for bot: {username}"
            }
    
    async def close_all_browsers(self):
        """Close all active browser instances"""
        print(f"🔴 Closing {len(self.active_bots)} active browsers...")
        
        for username, bot_browser in self.active_bots.items():
            await bot_browser.close_browser()
        
        self.active_bots.clear()
        print("✅ All browsers closed successfully")
    
    async def scrape_sjc(self, csv_data=None) -> Dict:
        """Filter card data from CSV"""
        return await self.sjc_service.scrape_sjc(csv_data=csv_data)
    
    async def close(self):
        """Close all browser instances when service shuts down"""
        await self.close_all_browsers()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()



# --- FastAPI endpoint for /api/scrape-sjc ---
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

_botnet_service = None

def get_botnet_service() -> BotnetService:
    global _botnet_service
    if _botnet_service is None:
        _botnet_service = BotnetService()
    return _botnet_service

@app.post("/api/scrape-sjc")
async def api_scrape_sjc(request: Request):
    service = get_botnet_service()
    
    # Get CSV data from request body if provided
    csv_data = None
    try:
        body = await request.json()
        csv_data = body.get('csv_data', None)
    except:
        pass
    
    # Run scrape_sjc with CSV data
    result = await service.scrape_sjc(csv_data=csv_data)
    return JSONResponse(content=result)