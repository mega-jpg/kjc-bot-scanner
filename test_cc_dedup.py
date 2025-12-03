"""Test Common Crawl with clear_results and deduplication"""
from botnet_service import CommonCrawlService

# Test 1: Clear mode
print("=" * 60)
print("TEST 1: CLEAR MODE")
print("=" * 60)
service = CommonCrawlService()
result = service.search_common_crawl(max_files=1, clear_results=True)
print(f"\n✓ Result: {result['shops_found']} shops found")

# Test 2: Append mode (should skip duplicates)
print("\n" + "=" * 60)
print("TEST 2: APPEND MODE (checking duplicates)")
print("=" * 60)
service2 = CommonCrawlService()
result2 = service2.search_common_crawl(max_files=1, clear_results=False)
print(f"\n✓ Result: {result2['shops_found']} NEW shops (after dedup)")

# Show final file stats
print("\n" + "=" * 60)
print("FINAL STATS")
print("=" * 60)
with open("outputDork/shops_fresh_2025_common_crawl.txt", "r") as f:
    lines = f.readlines()
    unique = set(line.strip().lower() for line in lines if line.strip())
    print(f"Total lines in file: {len(lines)}")
    print(f"Unique domains: {len(unique)}")
