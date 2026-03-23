"""Handler for /scores command"""

from typing import Optional
import httpx
from utils import normalize_lab_id
from services.lms_api import lms_client


async def handle_scores(lab: Optional[str] = None) -> str:
    """Handle /scores command - get scores for a lab"""
    if not lab:
        return "Please specify a lab: /scores lab-01"
    
    try:
        # First verify the lab exists
        items = await lms_client.get_items()
        labs = [i for i in items if i.get("type") == "lab"]
        
        # Extract lab number for matching
        lab_num = normalize_lab_id(lab)
        
        # Find lab by ID or title match
        lab_info = None
        for item in labs:
            lab_id = str(item.get("id", ""))
            title = item.get("title", "")
            
            # Match by ID (e.g., "4" or "lab-04") or title containing the number
            if lab_id == lab_num or lab.lower() in title.lower():
                lab_info = item
                break
            # Also try matching by lab number in title (e.g., "Lab 04" matches "lab-04")
            if lab_num in title:
                lab_info = item
                break
        
        if not lab_info:
            return f"❌ Lab '{lab}' not found. Use /labs to see available labs."
        
        lab_title = lab_info.get("title", lab)
        lab_id = lab_info.get("id")
        
        # Try to get pass rates
        pass_rates = await lms_client.get_pass_rates(str(lab_id))
        
        if not pass_rates:
            return f"📊 No pass rate data available for {lab_title} yet. (No submissions recorded)"
        
        lines = [f"📊 Pass rates for {lab_title}:"]
        for task in pass_rates:
            task_name = task.get("task_name", task.get("task_id", "Unknown"))
            pass_rate = task.get("pass_rate", 0)
            attempts = task.get("attempts", 0)
            lines.append(f"- {task_name}: {pass_rate:.1f}% ({attempts} attempts)")
        
        return "\n".join(lines)
    except httpx.ConnectError:
        return "❌ Backend error: connection refused. Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"❌ Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}."
    except httpx.HTTPError as e:
        return f"❌ Backend error: {str(e)}"
    except Exception as e:
        return f"❌ Backend error: {str(e)}"
