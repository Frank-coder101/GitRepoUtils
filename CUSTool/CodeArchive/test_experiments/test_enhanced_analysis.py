#!/usr/bin/env python3
"""
Test Enhanced TestCaseCreator with Documentation Analysis
"""

import os
from TestCaseCreator import TestCaseCreator

def test_enhanced_analysis():
    """Test TestCaseCreator with both source code and documentation"""
    
    defi_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
    docs_path = os.path.join(defi_path, "docs")
    
    print("=== ENHANCED TESTCASECREATOR WITH DOCUMENTATION ANALYSIS ===")
    print(f"Source path: {defi_path}")
    print(f"Documentation path: {docs_path}")
    
    # Check if paths exist
    if not os.path.exists(defi_path):
        print("✗ Source path does not exist")
        return False
    
    if not os.path.exists(docs_path):
        print("✗ Documentation path does not exist")
        return False
    
    try:
        # Create TestCaseCreator
        creator = TestCaseCreator()
        
        # Run enhanced analysis with both source and documentation
        print("\nRunning enhanced analysis...")
        results = creator.run_full_analysis(
            source_paths=[defi_path],
            blueprint_paths=[docs_path]
        )
        
        # Display results
        print("\n=== ANALYSIS RESULTS ===")
        print(f"Menu options found: {len(results['menu_options'])}")
        print(f"Documentation insights: {len(results['documentation_insights'])}")
        print(f"Simulation rules: {len(results['simulation_dict'])}")
        print(f"Test sequences: {len(results['test_sequences'])}")
        
        # Show some menu options
        print(f"\n=== SAMPLE MENU OPTIONS ===")
        for i, (trigger, option) in enumerate(results['menu_options'].items()):
            if i < 5:
                docs_refs = len(option.documentation_refs) if hasattr(option, 'documentation_refs') else 0
                print(f"  {i+1}. '{trigger}'")
                print(f"     Expected inputs: {option.expected_inputs}")
                print(f"     Documentation refs: {docs_refs}")
        
        # Show documentation insights
        print(f"\n=== DOCUMENTATION INSIGHTS ===")
        insight_types = {}
        for insight in results['documentation_insights']:
            insight_type = insight.insight_type
            if insight_type not in insight_types:
                insight_types[insight_type] = []
            insight_types[insight_type].append(insight)
        
        for insight_type, insights in insight_types.items():
            print(f"  {insight_type.upper()}: {len(insights)} insights")
            for i, insight in enumerate(insights[:3]):  # Show first 3
                filename = os.path.basename(insight.source_file)
                print(f"    {i+1}. From {filename}: {insight.content[:50]}...")
        
        # Show enhanced test sequences
        print(f"\n=== TEST SEQUENCES ===")
        sequence_types = {}
        for seq in results['test_sequences']:
            # Check if this is a documentation-based sequence
            if hasattr(seq, 'coverage_tags'):
                if 'requirement_based' in seq.coverage_tags:
                    seq_type = 'requirement_based'
                elif 'documented_test' in seq.coverage_tags:
                    seq_type = 'documented_test'
                elif 'flow_based' in seq.coverage_tags:
                    seq_type = 'flow_based'
                else:
                    seq_type = 'source_code_based'
            else:
                seq_type = 'source_code_based'
            
            if seq_type not in sequence_types:
                sequence_types[seq_type] = []
            sequence_types[seq_type].append(seq)
        
        for seq_type, sequences in sequence_types.items():
            print(f"  {seq_type.upper()}: {len(sequences)} sequences")
        
        # Show coverage report
        print(f"\n=== COVERAGE REPORT ===")
        coverage = results['coverage_report']
        print(f"Total sequences: {coverage.get('total_test_sequences', 0)}")
        print(f"High priority: {coverage.get('priority_distribution', {}).get(1, 0)}")
        print(f"Medium priority: {coverage.get('priority_distribution', {}).get(2, 0)}")
        print(f"Low priority: {coverage.get('priority_distribution', {}).get(3, 0)}")
        
        # Show generated files
        print(f"\n=== GENERATED FILES ===")
        generated_files = [
            "simulation_dictionary.txt",
            "test_sequences.json",
            "documentation_insights.json"
        ]
        
        for filename in generated_files:
            if os.path.exists(filename):
                print(f"✓ {filename}")
            else:
                print(f"✗ {filename} (not found)")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_enhanced_analysis()
    
    if success:
        print("\n✅ SUCCESS: Enhanced TestCaseCreator with documentation analysis works!")
        print("\nBenefits of documentation analysis:")
        print("1. More comprehensive test coverage")
        print("2. Requirements-based test cases")
        print("3. Better understanding of expected behaviors")
        print("4. Enhanced simulation dictionaries")
        print("5. Documentation-driven test sequences")
        print("\nNext steps:")
        print("1. Review generated documentation_insights.json")
        print("2. Check enhanced simulation_dictionary.txt")
        print("3. Examine test_sequences.json for doc-based tests")
        print("4. Run MasterController.py with blueprint paths")
    else:
        print("\n❌ FAILURE: Enhanced analysis failed")

if __name__ == "__main__":
    main()
