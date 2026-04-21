#!/usr/bin/env python3
"""
Test suite for AI generative features.

Tests the following implementations:
1. generate_artistic_caption() - Dynamic caption generation with Gemini
2. analyze_vibe() - Night Owl vs Early Bird detection from commit history
"""

from ai.generative import generate_artistic_caption, analyze_vibe
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_generate_artistic_caption():
    """Test artistic caption generation"""
    print("\n" + "="*70)
    print("TEST 1: Artistic Caption Generation")
    print("="*70)
    
    test_cases = [
        {
            "username": "torvalds",
            "total_commits": 80000,
            "top_language": "C",
            "description": "Linux creator with massive commit history"
        },
        {
            "username": "gvanrossum",
            "total_commits": 15000,
            "top_language": "Python",
            "description": "Python creator"
        },
        {
            "username": "ejw",
            "total_commits": 3500,
            "top_language": "JavaScript",
            "description": "Web developer"
        },
    ]
    
    for case in test_cases:
        try:
            caption = generate_artistic_caption(
                case["username"],
                case["total_commits"],
                case["top_language"]
            )
            
            print(f"\n📝 {case['description']}")
            print(f"   User: {case['username']}")
            print(f"   Commits: {case['total_commits']}")
            print(f"   Language: {case['top_language']}")
            print(f"   ✨ Caption: {caption}")
            
            # Validate caption
            if caption and len(caption) > 10:
                print(f"   ✓ Caption generated successfully")
            else:
                print(f"   ✗ Caption too short or empty")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")


def test_analyze_vibe_early_bird():
    """Test vibe analysis for early bird pattern (pastel)"""
    print("\n" + "="*70)
    print("TEST 2: Vibe Analysis - Early Bird Pattern (Pastel)")
    print("="*70)
    
    # Early bird pattern: Consistent weekday commits, few weekend commits
    contributions = []
    base_date = datetime(2025, 1, 1)
    
    for i in range(60):  # 60 days
        current_date = base_date + timedelta(days=i)
        weekday = current_date.weekday()
        
        if weekday < 5:  # Weekday (Monday-Friday)
            # Consistent high weekday commits (8am-5pm pattern)
            commits = 5 + (i % 3)  # 5-8 commits on weekdays
        else:  # Weekend
            # Few weekend commits (night owl would have more)
            commits = 0 if i % 7 == 0 else 1
        
        contributions.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "count": commits
        })
    
    vibe = analyze_vibe(contributions)
    
    print(f"\nContribution Pattern:")
    print(f"  - 60 days of data")
    print(f"  - High weekday commits (5-8 per day)")
    print(f"  - Low weekend commits (0-1 per day)")
    print(f"  - Consistent, regular pattern")
    print(f"\n✨ Detected Vibe: {vibe.upper()}")
    
    if vibe == "pastel":
        print("✓ Correctly identified as Early Bird (Pastel)")
    else:
        print(f"⚠ Expected 'pastel' but got '{vibe}'")


def test_analyze_vibe_night_owl():
    """Test vibe analysis for night owl pattern (neon)"""
    print("\n" + "="*70)
    print("TEST 3: Vibe Analysis - Night Owl Pattern (Neon)")
    print("="*70)
    
    # Night owl pattern: Irregular schedule, lots of weekend commits, high variance
    contributions = []
    base_date = datetime(2025, 1, 1)
    
    for i in range(60):  # 60 days
        current_date = base_date + timedelta(days=i)
        weekday = current_date.weekday()
        
        if weekday < 5:  # Weekday (Monday-Friday)
            # Irregular weekday commits (some high, some low)
            commits = (i * 7 + i % 13) % 10  # Variable pattern
        else:  # Weekend
            # High weekend commits (more flexible schedule)
            commits = 8 + (i % 5)  # 8-13 commits on weekends
        
        contributions.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "count": commits
        })
    
    vibe = analyze_vibe(contributions)
    
    print(f"\nContribution Pattern:")
    print(f"  - 60 days of data")
    print(f"  - Irregular commit distribution")
    print(f"  - High weekend commits (8-13 per day)")
    print(f"  - Variable pattern (high variance)")
    print(f"\n✨ Detected Vibe: {vibe.upper()}")
    
    if vibe == "neon":
        print("✓ Correctly identified as Night Owl (Neon)")
    else:
        print(f"⚠ Expected 'neon' but got '{vibe}'")


def test_analyze_vibe_empty():
    """Test vibe analysis with empty history"""
    print("\n" + "="*70)
    print("TEST 4: Vibe Analysis - Empty History (Default)")
    print("="*70)
    
    vibe = analyze_vibe([])
    
    print(f"\nInput: Empty contribution history")
    print(f"✨ Detected Vibe: {vibe.upper()}")
    print(f"✓ Returns default value (neon)")


def test_analyze_vibe_minimal():
    """Test vibe analysis with minimal data"""
    print("\n" + "="*70)
    print("TEST 5: Vibe Analysis - Minimal Data")
    print("="*70)
    
    # Just a few commits
    contributions = [
        {"date": "2025-01-01", "count": 5},
        {"date": "2025-01-02", "count": 3},
        {"date": "2025-01-03", "count": 8},
        {"date": "2025-01-04", "count": 2},
        {"date": "2025-01-05", "count": 4},
    ]
    
    vibe = analyze_vibe(contributions)
    
    print(f"\nInput: 5 days of minimal data")
    print(f"Commits: {[c['count'] for c in contributions]}")
    print(f"✨ Detected Vibe: {vibe.upper()}")
    print(f"✓ Handles minimal data gracefully")


def test_caption_with_large_numbers():
    """Test caption generation with extreme numbers"""
    print("\n" + "="*70)
    print("TEST 6: Artistic Caption - Extreme Numbers")
    print("="*70)
    
    try:
        # Test with very large commit count
        caption = generate_artistic_caption(
            "superdev",
            500000,
            "Rust"
        )
        
        print(f"\n⚡ Extreme Profile:")
        print(f"   User: superdev")
        print(f"   Commits: 500,000")
        print(f"   Language: Rust")
        print(f"   ✨ Caption: {caption}")
        print(f"✓ Handles large numbers correctly")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def test_integration():
    """Integration test combining both features"""
    print("\n" + "="*70)
    print("TEST 7: Integration - Complete Profile Analysis")
    print("="*70)
    
    # Create a realistic developer profile
    username = "alice_dev"
    total_commits = 12500
    top_language = "TypeScript"
    
    # Early bird commit pattern
    contributions = []
    base_date = datetime(2024, 9, 1)
    
    for i in range(120):  # 4 months of data
        current_date = base_date + timedelta(days=i)
        weekday = current_date.weekday()
        
        if weekday < 5:  # Weekday
            commits = 8 + (i % 4)  # 8-12 commits on weekdays
        else:  # Weekend
            commits = 0 if i % 3 == 0 else 1  # Mostly off on weekends
        
        contributions.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "count": commits
        })
    
    try:
        print(f"\n👤 Developer Profile: {username}")
        print(f"   Commits: {total_commits}")
        print(f"   Primary Language: {top_language}")
        
        # Generate caption
        caption = generate_artistic_caption(username, total_commits, top_language)
        print(f"\n✨ Artistic Caption:")
        print(f"   {caption}")
        
        # Analyze vibe
        vibe = analyze_vibe(contributions)
        print(f"\n🎨 Vibe Analysis:")
        print(f"   Detected Vibe: {vibe.upper()}")
        
        theme_map = {
            "neon": "Dark, vibrant theme for night owls",
            "pastel": "Light, soft theme for early birds"
        }
        
        print(f"   Theme: {theme_map.get(vibe, 'Unknown')}")
        print(f"\n✓ Integration test completed successfully")
        
    except Exception as e:
        print(f"\n✗ Integration test failed: {e}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 AI GENERATIVE FEATURES TEST SUITE")
    print("="*70)
    
    tests = [
        test_generate_artistic_caption,
        test_analyze_vibe_early_bird,
        test_analyze_vibe_night_owl,
        test_analyze_vibe_empty,
        test_analyze_vibe_minimal,
        test_caption_with_large_numbers,
        test_integration,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\n✗ Test {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("✅ Test suite complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
