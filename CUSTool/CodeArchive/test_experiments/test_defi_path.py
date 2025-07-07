#!/usr/bin/env python3
"""
Test TestCaseCreator with DeFiHuddleTradingSystem path
"""

import os
from TestCaseCreator import TestCaseCreator

def test_path_analysis():
    """Test if TestCaseCreator can analyze the DeFiHuddleTradingSystem path"""
    
    defi_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
    docs_path = os.path.join(defi_path, "docs")
    
    print(f"Testing path: {defi_path}")
    print(f"Testing docs path: {docs_path}")
    
    # Check if path exists
    if os.path.exists(defi_path):
        print("✓ Path exists")
        
        # Check if it's a directory
        if os.path.isdir(defi_path):
            print("✓ Path is a directory")
            
            # List contents
            try:
                contents = os.listdir(defi_path)
                print(f"✓ Directory contains {len(contents)} items")
                
                # Show first few items
                for i, item in enumerate(contents[:10]):
                    item_path = os.path.join(defi_path, item)
                    item_type = "DIR" if os.path.isdir(item_path) else "FILE"
                    print(f"  {i+1}. [{item_type}] {item}")
                
                if len(contents) > 10:
                    print(f"  ... and {len(contents) - 10} more items")
                
                # Check for source files
                source_files = []
                for root, dirs, files in os.walk(defi_path):
                    for file in files:
                        if file.endswith(('.py', '.cpp', '.c', '.java', '.cs', '.js', '.ts', '.go', '.rs')):
                            source_files.append(os.path.join(root, file))
                
                print(f"✓ Found {len(source_files)} source files")
                
                # Show some source files
                for i, file in enumerate(source_files[:5]):
                    rel_path = os.path.relpath(file, defi_path)
                    print(f"  {i+1}. {rel_path}")
                
                if len(source_files) > 5:
                    print(f"  ... and {len(source_files) - 5} more source files")
                
                # Check for documentation files
                print(f"\n=== ANALYZING DOCUMENTATION ===")
                if os.path.exists(docs_path):
                    print("✓ Docs directory exists")
                    
                    doc_files = []
                    for root, dirs, files in os.walk(docs_path):
                        for file in files:
                            if file.endswith(('.md', '.txt', '.rst', '.doc', '.docx', '.pdf')):
                                doc_files.append(os.path.join(root, file))
                    
                    print(f"✓ Found {len(doc_files)} documentation files")
                    
                    # Show documentation files
                    for i, file in enumerate(doc_files[:10]):
                        rel_path = os.path.relpath(file, docs_path)
                        print(f"  {i+1}. {rel_path}")
                    
                    if len(doc_files) > 10:
                        print(f"  ... and {len(doc_files) - 10} more documentation files")
                    
                    # Look for key files
                    key_files = []
                    for file in doc_files:
                        filename = os.path.basename(file).lower()
                        if any(keyword in filename for keyword in ['requirement', 'blueprint', 'spec', 'design', 'architecture', 'test', 'case']):
                            key_files.append(file)
                    
                    if key_files:
                        print(f"✓ Found {len(key_files)} key documentation files:")
                        for i, file in enumerate(key_files):
                            rel_path = os.path.relpath(file, docs_path)
                            print(f"  {i+1}. {rel_path}")
                    
                else:
                    print("✗ Docs directory does not exist")
                
            except PermissionError:
                print("✗ Permission denied - cannot read directory contents")
                return False
            except Exception as e:
                print(f"✗ Error reading directory: {e}")
                return False
        else:
            print("✗ Path is not a directory")
            return False
    else:
        print("✗ Path does not exist")
        return False
    
    # Try to analyze with TestCaseCreator
    try:
        print("\n=== TESTING TESTCASECREATOR ANALYSIS ===")
        creator = TestCaseCreator()
        
        # Test analysis
        results = creator.analyze_source_code([defi_path])
        
        print(f"✓ Source code analysis completed successfully")
        print(f"  Menu options found: {len(results)}")
        
        if results:
            print("  Sample menu options:")
            for i, (trigger, option) in enumerate(results.items()):
                if i < 3:
                    print(f"    {i+1}. '{trigger}' -> {option.expected_inputs}")
        
        return True
        
    except Exception as e:
        print(f"✗ TestCaseCreator analysis failed: {e}")
        return False

def main():
    print("=== Testing DeFiHuddleTradingSystem Path Analysis ===")
    success = test_path_analysis()
    
    if success:
        print("\n✓ SUCCESS: TestCaseCreator can analyze the DeFiHuddleTradingSystem path")
    else:
        print("\n✗ FAILURE: TestCaseCreator cannot analyze the DeFiHuddleTradingSystem path")
        print("\nPossible solutions:")
        print("1. Check if the path exists and is accessible")
        print("2. Verify permissions on the directory")
        print("3. Use a different path or copy source files to current directory")

if __name__ == "__main__":
    main()
