#!/usr/bin/env python3
"""
IssuePromptGenerator - AI-Optimized Defect Reporting System

Generates comprehensive issue prompts for AI-assisted debugging when test cases fail.
Integrates with SequenceRunner and CUS to capture failure context automatically.

Features:
- Severity-based classification (Critical, Error, Warning, Info)
- Comprehensive failure context collection
- AI-optimized prompt format (Markdown + JSON metadata)
- Screenshot capture with annotations
- Documentation traceability
- External program directory integration
"""

import os
import json
import time
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid

# Import for screenshot annotation (we'll add this capability)
try:
    from PIL import Image, ImageDraw, ImageFont
    ANNOTATION_AVAILABLE = True
except ImportError:
    ANNOTATION_AVAILABLE = False

class IssueSeverity(Enum):
    """Issue severity levels"""
    CRITICAL = "Critical"    # External program crashes, data corruption
    ERROR = "Error"         # Test failures, functional issues
    WARNING = "Warning"     # Performance issues, minor deviations
    INFO = "Info"          # Information only, no action required

class FailureType(Enum):
    """Types of test failures"""
    CUS_SIMULATION_FAILURE = "CUS_Simulation_Failure"
    OCR_MISMATCH = "OCR_Mismatch"
    EXTERNAL_PROGRAM_CRASH = "External_Program_Crash"
    EXTERNAL_PROGRAM_ERROR = "External_Program_Error"
    TIMEOUT = "Timeout"
    NAVIGATION_FAILURE = "Navigation_Failure"
    VALIDATION_FAILURE = "Validation_Failure"

@dataclass
class ScreenshotInfo:
    """Information about captured screenshots"""
    screenshot_id: str
    file_path: str
    timestamp: datetime
    screenshot_type: str  # 'failure', 'before', 'after', 'annotated'
    description: str
    annotations: List[Dict] = field(default_factory=list)

@dataclass
class DocumentationReference:
    """Reference to documentation that relates to the test case"""
    file_path: str
    reference_type: str  # 'requirement', 'architecture', 'test_case', 'design'
    reference_id: Optional[str] = None
    line_number: Optional[int] = None
    section_title: Optional[str] = None

@dataclass
class TestCaseContext:
    """Complete context of a test case for issue generation"""
    test_case_name: str
    test_sequence_id: str
    expected_behavior: str
    actual_behavior: str
    failure_step: int
    reproduction_steps: List[str]
    documentation_refs: List[DocumentationReference]
    related_test_cases: List[str]
    dependency_chain: List[str]

@dataclass
class IssuePrompt:
    """Complete issue prompt data structure"""
    issue_id: str
    timestamp: datetime
    test_run_id: str
    severity: IssueSeverity
    failure_type: FailureType
    test_case_context: TestCaseContext
    screenshots: List[ScreenshotInfo]
    error_details: Dict[str, Any]
    system_context: Dict[str, Any]
    ai_assistance_request: str

class IssuePromptGenerator:
    """
    Generates comprehensive issue prompts for AI-assisted debugging
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._load_default_config()
        self.external_program_path = self.config.get("external_program_path", "")
        self.defect_prompts_path = self._setup_defect_prompts_directory()
        self.current_test_run_id = self._generate_test_run_id()
        
    def _load_default_config(self) -> Dict:
        """Load default configuration"""
        return {
            "external_program_path": "",
            "capture_before_after": False,
            "capture_sequence": False,
            "annotate_screenshots": True,
            "severity_mapping": {
                "external_crash": IssueSeverity.CRITICAL,
                "external_error": IssueSeverity.ERROR,
                "cus_failure": IssueSeverity.ERROR,
                "ocr_mismatch": IssueSeverity.WARNING,
                "timeout": IssueSeverity.WARNING
            },
            "screenshot_settings": {
                "save_original": True,
                "save_annotated": True,
                "annotation_color": "red",
                "annotation_width": 3
            }
        }
    
    def _setup_defect_prompts_directory(self) -> str:
        """Setup the defect prompts directory in the external program's location"""
        if self.external_program_path and os.path.exists(self.external_program_path):
            # Use external program directory
            if os.path.isfile(self.external_program_path):
                base_dir = os.path.dirname(self.external_program_path)
            else:
                base_dir = self.external_program_path
        else:
            # Fallback to current directory
            base_dir = os.getcwd()
        
        defect_prompts_dir = os.path.join(base_dir, "UserSimulator", "DefectPrompts")
        os.makedirs(defect_prompts_dir, exist_ok=True)
        
        # Create subdirectories
        subdirs = ["screenshots", "metadata", "archives"]
        for subdir in subdirs:
            os.makedirs(os.path.join(defect_prompts_dir, subdir), exist_ok=True)
        
        return defect_prompts_dir
    
    def _generate_test_run_id(self) -> str:
        """Generate unique test run ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"TESTRUN_{timestamp}_{str(uuid.uuid4())[:8].upper()}"
    
    def _generate_issue_id(self) -> str:
        """Generate unique issue ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"CUS_ISSUE_{timestamp}_{str(uuid.uuid4())[:8].upper()}"
    
    def detect_failure_type_and_severity(self, error_context: Dict) -> Tuple[FailureType, IssueSeverity]:
        """
        Determine failure type and severity based on error context
        """
        error_type = error_context.get("error_type", "unknown")
        error_message = error_context.get("error_message", "").lower()
        
        # Determine failure type
        if "external_program_crash" in error_type:
            failure_type = FailureType.EXTERNAL_PROGRAM_CRASH
        elif "external_program_error" in error_type:
            failure_type = FailureType.EXTERNAL_PROGRAM_ERROR
        elif "cus_simulation" in error_type:
            failure_type = FailureType.CUS_SIMULATION_FAILURE
        elif "ocr_mismatch" in error_type:
            failure_type = FailureType.OCR_MISMATCH
        elif "timeout" in error_message:
            failure_type = FailureType.TIMEOUT
        elif "navigation" in error_message:
            failure_type = FailureType.NAVIGATION_FAILURE
        else:
            failure_type = FailureType.VALIDATION_FAILURE
        
        # Determine severity
        severity_mapping = self.config["severity_mapping"]
        if failure_type == FailureType.EXTERNAL_PROGRAM_CRASH:
            severity = severity_mapping.get("external_crash", IssueSeverity.CRITICAL)
        elif failure_type == FailureType.EXTERNAL_PROGRAM_ERROR:
            severity = severity_mapping.get("external_error", IssueSeverity.ERROR)
        elif failure_type == FailureType.CUS_SIMULATION_FAILURE:
            severity = severity_mapping.get("cus_failure", IssueSeverity.ERROR)
        elif failure_type == FailureType.OCR_MISMATCH:
            severity = severity_mapping.get("ocr_mismatch", IssueSeverity.WARNING)
        else:
            severity = IssueSeverity.WARNING
        
        return failure_type, severity
    
    def capture_failure_screenshot(self, issue_id: str, annotation_data: Dict = None) -> ScreenshotInfo:
        """
        Capture screenshot of failure with optional annotations
        """
        try:
            # Import screenshot capability (already available from CUS)
            from PIL import ImageGrab
            
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Generate screenshot info
            timestamp = datetime.now()
            screenshot_id = f"{issue_id}_failure_{int(timestamp.timestamp())}"
            filename = f"{screenshot_id}.png"
            file_path = os.path.join(self.defect_prompts_path, "screenshots", filename)
            
            # Save original
            screenshot.save(file_path)
            
            screenshot_info = ScreenshotInfo(
                screenshot_id=screenshot_id,
                file_path=file_path,
                timestamp=timestamp,
                screenshot_type='failure',
                description="Screenshot captured at time of test failure"
            )
            
            # Create annotated version if requested and data available
            if self.config["screenshot_settings"]["save_annotated"] and annotation_data:
                annotated_info = self._create_annotated_screenshot(
                    screenshot, screenshot_info, annotation_data
                )
                return annotated_info
            
            return screenshot_info
            
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            # Return placeholder info
            return ScreenshotInfo(
                screenshot_id=f"{issue_id}_failure_unavailable",
                file_path="screenshot_unavailable",
                timestamp=datetime.now(),
                screenshot_type='failure',
                description=f"Screenshot capture failed: {e}"
            )
    
    def _create_annotated_screenshot(self, screenshot: Image, base_info: ScreenshotInfo, annotation_data: Dict) -> ScreenshotInfo:
        """
        Create annotated version of screenshot highlighting expected vs actual areas
        """
        if not ANNOTATION_AVAILABLE:
            return base_info
        
        try:
            # Create copy for annotation
            annotated = screenshot.copy()
            draw = ImageDraw.Draw(annotated)
            
            # Annotation settings
            color = self.config["screenshot_settings"]["annotation_color"]
            width = self.config["screenshot_settings"]["annotation_width"]
            
            # Add annotations based on data
            annotations = []
            
            if "expected_area" in annotation_data:
                area = annotation_data["expected_area"]
                draw.rectangle(area, outline=color, width=width)
                draw.text((area[0], area[1] - 20), "EXPECTED", fill=color)
                annotations.append({"type": "expected", "area": area})
            
            if "actual_area" in annotation_data:
                area = annotation_data["actual_area"]
                draw.rectangle(area, outline="blue", width=width)
                draw.text((area[0], area[1] - 20), "ACTUAL", fill="blue")
                annotations.append({"type": "actual", "area": area})
            
            if "error_location" in annotation_data:
                area = annotation_data["error_location"]
                draw.rectangle(area, outline="red", width=width)
                draw.text((area[0], area[1] - 20), "ERROR", fill="red")
                annotations.append({"type": "error", "area": area})
            
            # Save annotated version
            annotated_filename = f"{base_info.screenshot_id}_annotated.png"
            annotated_path = os.path.join(self.defect_prompts_path, "screenshots", annotated_filename)
            annotated.save(annotated_path)
            
            # Create annotated screenshot info
            annotated_info = ScreenshotInfo(
                screenshot_id=f"{base_info.screenshot_id}_annotated",
                file_path=annotated_path,
                timestamp=base_info.timestamp,
                screenshot_type='annotated',
                description="Annotated screenshot highlighting expected vs actual areas",
                annotations=annotations
            )
            
            return annotated_info
            
        except Exception as e:
            print(f"Error creating annotated screenshot: {e}")
            return base_info
    
    def generate_issue_prompt(self, 
                            test_case_context: TestCaseContext,
                            error_context: Dict,
                            screenshots: List[ScreenshotInfo] = None,
                            system_context: Dict = None) -> IssuePrompt:
        """
        Generate comprehensive issue prompt for AI assistance
        """
        # Generate unique identifiers
        issue_id = self._generate_issue_id()
        timestamp = datetime.now()
        
        # Determine failure type and severity
        failure_type, severity = self.detect_failure_type_and_severity(error_context)
        
        # Capture screenshot if not provided
        if not screenshots:
            screenshot_info = self.capture_failure_screenshot(
                issue_id, 
                error_context.get("annotation_data")
            )
            screenshots = [screenshot_info]
        
        # Create AI assistance request
        ai_request = self._generate_ai_assistance_request(
            test_case_context, error_context, failure_type, severity
        )
        
        # Create issue prompt
        issue_prompt = IssuePrompt(
            issue_id=issue_id,
            timestamp=timestamp,
            test_run_id=self.current_test_run_id,
            severity=severity,
            failure_type=failure_type,
            test_case_context=test_case_context,
            screenshots=screenshots,
            error_details=error_context,
            system_context=system_context or {},
            ai_assistance_request=ai_request
        )
        
        return issue_prompt
    
    def _generate_ai_assistance_request(self, 
                                      test_context: TestCaseContext,
                                      error_context: Dict,
                                      failure_type: FailureType,
                                      severity: IssueSeverity) -> str:
        """
        Generate AI-optimized assistance request
        """
        request_parts = [
            f"Please analyze this {severity.value.lower()} {failure_type.value.replace('_', ' ').lower()} and provide specific code fixes for the DeFiHuddleTradingSystem.",
            f"",
            f"**Focus Areas:**",
            f"1. Root cause analysis of the {failure_type.value.replace('_', ' ').lower()}",
            f"2. Specific code changes needed to fix the issue",
            f"3. Prevention measures to avoid similar issues",
            f"4. Impact assessment on related functionality"
        ]
        
        if failure_type == FailureType.EXTERNAL_PROGRAM_CRASH:
            request_parts.extend([
                f"",
                f"**Critical Priority**: This is a system crash requiring immediate attention.",
                f"- Analyze the crash logs and stack traces",
                f"- Identify memory leaks, null pointer exceptions, or resource issues",
                f"- Provide robust error handling and recovery mechanisms"
            ])
        elif failure_type == FailureType.CUS_SIMULATION_FAILURE:
            request_parts.extend([
                f"",
                f"**UI/Menu Analysis**: The simulation failed to find expected interface elements.",
                f"- Check if menu options have changed",
                f"- Verify UI element identifiers and trigger patterns",
                f"- Update menu navigation logic if needed"
            ])
        
        return "\n".join(request_parts)
    
    def save_issue_prompt(self, issue_prompt: IssuePrompt) -> str:
        """
        Save issue prompt to markdown file with JSON metadata
        """
        try:
            # Create markdown content
            markdown_content = self._create_markdown_prompt(issue_prompt)
            
            # Create JSON metadata
            json_metadata = self._create_json_metadata(issue_prompt)
            
            # Save markdown file
            markdown_filename = f"{issue_prompt.issue_id}.md"
            markdown_path = os.path.join(self.defect_prompts_path, markdown_filename)
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Save JSON metadata
            json_filename = f"{issue_prompt.issue_id}_metadata.json"
            json_path = os.path.join(self.defect_prompts_path, "metadata", json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_metadata, f, indent=2, default=str)
            
            print(f"Issue prompt saved: {markdown_path}")
            print(f"Metadata saved: {json_path}")
            
            return markdown_path
            
        except Exception as e:
            print(f"Error saving issue prompt: {e}")
            return ""
    
    def _create_markdown_prompt(self, issue_prompt: IssuePrompt) -> str:
        """
        Create markdown-formatted issue prompt
        """
        content_parts = [
            f"# CUS Test Failure Report",
            f"",
            f"## Issue Identification",
            f"- **Error ID**: {issue_prompt.issue_id}",
            f"- **Timestamp**: {issue_prompt.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"- **Test Run ID**: {issue_prompt.test_run_id}",
            f"- **Severity**: {issue_prompt.severity.value}",
            f"- **Failure Type**: {issue_prompt.failure_type.value.replace('_', ' ')}",
            f"- **Test Case**: {issue_prompt.test_case_context.test_case_name}",
            f"",
            f"## Failure Summary",
            f"**Expected**: {issue_prompt.test_case_context.expected_behavior}",
            f"**Actual**: {issue_prompt.test_case_context.actual_behavior}",
            f"**Failed at Step**: {issue_prompt.test_case_context.failure_step}",
            f"",
            f"## Reproduction Steps"
        ]
        
        # Add reproduction steps
        for i, step in enumerate(issue_prompt.test_case_context.reproduction_steps, 1):
            if i == issue_prompt.test_case_context.failure_step:
                content_parts.append(f"{i}. **[FAILED]** {step}")
            else:
                content_parts.append(f"{i}. {step}")
        
        # Add visual evidence
        content_parts.extend([
            f"",
            f"## Visual Evidence"
        ])
        
        for screenshot in issue_prompt.screenshots:
            content_parts.extend([
                f"- **{screenshot.screenshot_type.title()} Screenshot**: `{screenshot.file_path}`",
                f"  - ID: {screenshot.screenshot_id}",
                f"  - Description: {screenshot.description}"
            ])
        
        # Add documentation references
        if issue_prompt.test_case_context.documentation_refs:
            content_parts.extend([
                f"",
                f"## Documentation References"
            ])
            
            for doc_ref in issue_prompt.test_case_context.documentation_refs:
                content_parts.extend([
                    f"### {doc_ref.reference_type.title()}",
                    f"- **File**: `{doc_ref.file_path}`"
                ])
                
                if doc_ref.reference_id:
                    content_parts.append(f"- **Reference ID**: {doc_ref.reference_id}")
                if doc_ref.line_number:
                    content_parts.append(f"- **Line**: {doc_ref.line_number}")
                if doc_ref.section_title:
                    content_parts.append(f"- **Section**: {doc_ref.section_title}")
        
        # Add error details
        content_parts.extend([
            f"",
            f"## Error Details",
            f"```json",
            json.dumps(issue_prompt.error_details, indent=2),
            f"```"
        ])
        
        # Add related test cases
        if issue_prompt.test_case_context.related_test_cases:
            content_parts.extend([
                f"",
                f"## Related Test Cases"
            ])
            for test_case in issue_prompt.test_case_context.related_test_cases:
                content_parts.append(f"- {test_case}")
        
        # Add dependency chain
        if issue_prompt.test_case_context.dependency_chain:
            content_parts.extend([
                f"",
                f"## Dependency Chain"
            ])
            for dependency in issue_prompt.test_case_context.dependency_chain:
                content_parts.append(f"- {dependency}")
        
        # Add AI assistance request
        content_parts.extend([
            f"",
            f"## AI Assistance Request",
            f"",
            issue_prompt.ai_assistance_request
        ])
        
        return "\n".join(content_parts)
    
    def _create_json_metadata(self, issue_prompt: IssuePrompt) -> Dict:
        """
        Create JSON metadata for programmatic processing
        """
        return {
            "issue_id": issue_prompt.issue_id,
            "timestamp": issue_prompt.timestamp.isoformat(),
            "test_run_id": issue_prompt.test_run_id,
            "severity": issue_prompt.severity.value,
            "failure_type": issue_prompt.failure_type.value,
            "test_case_name": issue_prompt.test_case_context.test_case_name,
            "test_sequence_id": issue_prompt.test_case_context.test_sequence_id,
            "failure_step": issue_prompt.test_case_context.failure_step,
            "screenshots": [
                {
                    "screenshot_id": s.screenshot_id,
                    "file_path": s.file_path,
                    "type": s.screenshot_type,
                    "description": s.description
                } for s in issue_prompt.screenshots
            ],
            "documentation_references": [
                {
                    "file_path": dr.file_path,
                    "reference_type": dr.reference_type,
                    "reference_id": dr.reference_id,
                    "line_number": dr.line_number,
                    "section_title": dr.section_title
                } for dr in issue_prompt.test_case_context.documentation_refs
            ],
            "related_test_cases": issue_prompt.test_case_context.related_test_cases,
            "dependency_chain": issue_prompt.test_case_context.dependency_chain,
            "error_details": issue_prompt.error_details,
            "system_context": issue_prompt.system_context
        }

def main():
    """Demo the IssuePromptGenerator"""
    print("=== IssuePromptGenerator Demo ===")
    
    # Create generator
    config = {
        "external_program_path": r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem",
        "annotate_screenshots": True
    }
    
    generator = IssuePromptGenerator(config)
    print(f"Defect prompts directory: {generator.defect_prompts_path}")
    
    # Create sample test case context
    test_context = TestCaseContext(
        test_case_name="test_main_menu_navigation_option_4",
        test_sequence_id="SEQ_001",
        expected_behavior="Menu option 4 should navigate to Transaction History",
        actual_behavior="Menu option 4 resulted in 'Invalid option' error",
        failure_step=3,
        reproduction_steps=[
            "Launch DeFiHuddleTradingSystem",
            "Wait for main menu display",
            "Simulate keypress: '4'",
            "Expect: Transaction History menu"
        ],
        documentation_refs=[
            DocumentationReference(
                file_path=r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem\docs\Project_Requirements.md",
                reference_type="requirement",
                reference_id="REQ-3.4.1",
                section_title="Menu Navigation"
            )
        ],
        related_test_cases=["test_main_menu_display", "test_transaction_history_access"],
        dependency_chain=["test_system_startup", "test_main_menu_display"]
    )
    
    # Create sample error context
    error_context = {
        "error_type": "cus_simulation_failure",
        "error_message": "Could not find expected trigger: 'Transaction History'",
        "ocr_text": "Main Menu\n1. Account Balance\n2. Transfer Money\n3. Settings\nInvalid option selected",
        "expected_text": "Transaction History",
        "annotation_data": {
            "expected_area": [100, 200, 300, 250],
            "actual_area": [100, 300, 300, 350]
        }
    }
    
    # Generate issue prompt
    issue_prompt = generator.generate_issue_prompt(test_context, error_context)
    
    # Save issue prompt
    saved_path = generator.save_issue_prompt(issue_prompt)
    
    if saved_path:
        print(f"✓ Demo issue prompt generated successfully!")
        print(f"  Issue ID: {issue_prompt.issue_id}")
        print(f"  Severity: {issue_prompt.severity.value}")
        print(f"  File: {saved_path}")
    else:
        print("✗ Failed to generate issue prompt")

if __name__ == "__main__":
    main()
