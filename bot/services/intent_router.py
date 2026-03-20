"""Intent router for natural language queries using LLM."""

import sys
import json
from typing import Any, Optional

from services.llm_client import llm_client, TOOL_DEFINITIONS, SYSTEM_PROMPT
from services.lms_api import lms_client


async def route_intent(message: str, debug: bool = True) -> str:
    """
    Route user message to appropriate tool(s) using LLM.
    
    Args:
        message: User's natural language query
        debug: Whether to print debug info to stderr
        
    Returns:
        Formatted response string
    """
    # Initialize conversation with system prompt
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]
    
    max_iterations = 5  # Prevent infinite loops
    iteration = 0
    
    try:
        while iteration < max_iterations:
            iteration += 1
            
            # Call LLM with tool definitions
            try:
                response = await llm_client.chat(messages, tools=TOOL_DEFINITIONS)
            except Exception as llm_error:
                # LLM unavailable - provide helpful fallback
                if debug:
                    print(f"[llm_error] {str(llm_error)}", file=sys.stderr)
                return f"⚠️ I'm having trouble connecting to my brain right now. Here's what I can help with:\n\n" \
                       f"📚 Commands:\n" \
                       f"/start - Welcome message\n" \
                       f"/help - Show available commands\n" \
                       f"/health - Check backend status\n" \
                       f"/labs - List all labs\n" \
                       f"/scores <lab> - Get scores for a lab\n\n" \
                       f"Or ask me questions like:\n" \
                       f"- 'what labs are available?'\n" \
                       f"- 'show me scores for lab 4'\n" \
                       f"- 'which lab has the lowest pass rate?'"
            
            # Check if LLM wants to call tools
            choice = response.get("choices", [{}])[0]
            message_data = choice.get("message", {})
            
            # If no tool calls, return the LLM's direct response
            if not message_data.get("tool_calls"):
                content = message_data.get("content", "I'm not sure how to help with that.")
                return content
            
            # Execute tool calls
            tool_calls = message_data["tool_calls"]
            
            # Add the assistant's message with tool calls to conversation
            messages.append(message_data)
            
            # Execute each tool call and collect results
            tool_results = []
            for tool_call in tool_calls:
                func = tool_call.get("function", {})
                tool_name = func.get("name", "")
                tool_args_str = func.get("arguments", "{}")
                
                # Parse arguments (LLM returns JSON string)
                import json
                try:
                    tool_args = json.loads(tool_args_str) if tool_args_str else {}
                except json.JSONDecodeError:
                    tool_args = {}
                
                if debug:
                    print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)
                
                # Execute the tool
                result = await execute_tool(tool_name, tool_args)
                tool_results.append(result)
                
                if debug:
                    result_preview = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                    print(f"[tool] Result: {result_preview}", file=sys.stderr)
            
            # Add tool results back to conversation
            import json
            for tool_call, result in zip(tool_calls, tool_results):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id", ""),
                    "content": json.dumps(result) if not isinstance(result, str) else result,
                })
            
            if debug:
                print(f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM", file=sys.stderr)
        
        # If we hit max iterations, ask LLM to summarize what we have
        messages.append({
            "role": "system",
            "content": "Please provide a final answer based on the tool results you've received."
        })
        
        response = await llm_client.chat(messages)
        choice = response.get("choices", [{}])[0]
        return choice.get("message", {}).get("content", "I encountered an error processing your request.")
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


async def execute_tool(name: str, args: dict[str, Any]) -> Any:
    """Execute a tool by name with given arguments."""
    from utils import normalize_lab_id
    
    try:
        if name == "get_items":
            items = await lms_client.get_items()
            return {"items": items, "count": len(items)}
        
        elif name == "get_learners":
            learners = await lms_client.get_learners()
            return {"learners": learners, "count": len(learners)}
        
        elif name == "get_scores":
            lab = normalize_lab_id(args.get("lab", ""))
            scores = await lms_client.get_scores(lab)
            return {"lab": lab, "scores": scores}
        
        elif name == "get_pass_rates":
            lab = normalize_lab_id(args.get("lab", ""))
            rates = await lms_client.get_pass_rates(lab)
            return {"lab": lab, "pass_rates": rates}
        
        elif name == "get_timeline":
            lab = normalize_lab_id(args.get("lab", ""))
            timeline = await lms_client.get_timeline(lab)
            return {"lab": lab, "timeline": timeline}
        
        elif name == "get_groups":
            lab = normalize_lab_id(args.get("lab", ""))
            groups = await lms_client.get_groups(lab)
            return {"lab": lab, "groups": groups}
        
        elif name == "get_top_learners":
            lab = normalize_lab_id(args.get("lab", ""))
            limit = args.get("limit", 5)
            learners = await lms_client.get_top_learners(lab, limit)
            return {"lab": lab, "top_learners": learners, "limit": limit}
        
        elif name == "get_completion_rate":
            lab = normalize_lab_id(args.get("lab", ""))
            rate = await lms_client.get_completion_rate(lab)
            return {"lab": lab, "completion_rate": rate}
        
        elif name == "trigger_sync":
            result = await lms_client.sync_pipeline()
            return {"sync_result": result}

        else:
            return {"error": f"Unknown tool: {name}"}

    except Exception as e:
        return {"error": str(e)}
