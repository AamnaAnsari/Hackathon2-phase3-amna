"""
Gemini AI Integration for Todo Chatbot
Uses NEW google-genai package (NOT google.generativeai)
"""
import os
import json
import google.genai as genai  # ✅ NEW PACKAGE
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAssistant:
    def __init__(self):
        """Initialize Gemini AI with NEW package"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file")
        
        # Initialize client with NEW syntax
        self.client = genai.Client(api_key=self.api_key)
        
        # Use gemini-2.0-flash model (free & fast)
        self.model = "models/gemini-2.0-flash"
        
        logger.info(f"✅ Gemini Assistant initialized with model: {self.model}")
    
    def _generate_content(self, prompt: str) -> str:
        """Generate content with NEW API"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": 0.7,
                    "max_output_tokens": 500,
                }
            )
            return response.text
        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            # Fallback to simple response
            return "I understand you want to manage tasks."
    
    async def analyze_message(self, user_message: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze user message - SIMPLE VERSION
        """
        # Simple keyword matching (more reliable than AI)
        message_lower = user_message.lower()
        
        # 1. ADD TASK
        if any(word in message_lower for word in ["add", "create", "new task", "make task", "insert"]):
            title = self._extract_title(user_message)
            return {
                "action": "add_task",
                "parameters": {
                    "title": title,
                    "description": user_message,
                    "task_id": None,
                    "status_filter": None
                },
                "confidence": 0.95,
                "response": f"✅ Added: '{title}' to your tasks."
            }
        
        # 2. LIST TASKS
        elif any(word in message_lower for word in ["show", "list", "view", "see", "what tasks", "get tasks"]):
            filter_type = "all"
            if "pending" in message_lower or "incomplete" in message_lower:
                filter_type = "pending"
            elif "complete" in message_lower or "done" in message_lower:
                filter_type = "completed"
            
            return {
                "action": "list_tasks",
                "parameters": {
                    "title": None,
                    "description": None,
                    "task_id": None,
                    "status_filter": filter_type
                },
                "confidence": 0.9,
                "response": f"📋 Showing your {filter_type} tasks."
            }
        
        # 3. COMPLETE TASK
        elif any(word in message_lower for word in ["complete", "finish", "mark as done", "check off", "done task"]):
            task_id = self._extract_task_id(user_message)
            return {
                "action": "complete_task",
                "parameters": {
                    "title": None,
                    "description": None,
                    "task_id": task_id,
                    "status_filter": None
                },
                "confidence": 0.85 if task_id else 0.6,
                "response": f"🎯 Marked task {task_id} as complete!" if task_id else "Please specify a task number to complete."
            }
        
        # 4. DELETE TASK
        elif any(word in message_lower for word in ["delete", "remove", "clear task", "erase"]):
            task_id = self._extract_task_id(user_message)
            return {
                "action": "delete_task",
                "parameters": {
                    "title": None,
                    "description": None,
                    "task_id": task_id,
                    "status_filter": None
                },
                "confidence": 0.85 if task_id else 0.6,
                "response": f"🗑️ Deleted task {task_id}." if task_id else "Which task should I delete?"
            }
        
        # 5. UPDATE TASK
        elif any(word in message_lower for word in ["update", "change", "modify", "edit"]):
            task_id = self._extract_task_id(user_message)
            title = self._extract_title(user_message)
            return {
                "action": "update_task",
                "parameters": {
                    "title": title if title != user_message else None,
                    "description": user_message,
                    "task_id": task_id,
                    "status_filter": None
                },
                "confidence": 0.8 if task_id else 0.5,
                "response": f"📝 Updating task {task_id}." if task_id else "Which task should I update?"
            }
        
        # 6. GREETING
        elif any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return {
                "action": "unknown",
                "parameters": {},
                "confidence": 0.1,
                "response": "👋 Hello! I'm your AI Todo Assistant. I can help you add, list, complete, or delete tasks."
            }
        
        # 7. HELP
        elif any(word in message_lower for word in ["help", "what can you do", "how to use"]):
            return {
                "action": "unknown",
                "parameters": {},
                "confidence": 0.1,
                "response": "🤖 I can help you: 1) Add tasks 2) List tasks 3) Complete tasks 4) Delete tasks. Try: 'Add task to buy milk' or 'Show my tasks'"
            }
        
        # 8. UNKNOWN
        else:
            return {
                "action": "unknown",
                "parameters": {},
                "confidence": 0.1,
                "response": "🤔 I can help you manage tasks. Try saying: 'Add task to buy groceries' or 'Show my pending tasks'"
            }
    
    def _extract_title(self, message: str) -> str:
        """Extract task title from message"""
        import re
        
        patterns = [
            r"add task to (.+)",
            r"add task: (.+)",
            r"task to (.+)",
            r"buy (.+)",
            r"complete (.+)",
            r"finish (.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                title = match.group(1).strip().capitalize()
                if len(title) > 3:  # Valid title
                    return title
        
        # Fallback: use message as title
        clean_msg = message.replace("add", "").replace("task", "").replace("to", "").strip()
        if clean_msg and len(clean_msg) > 3:
            return clean_msg[:50]
        
        return "New Task"
    
    def _extract_task_id(self, message: str) -> Optional[int]:
        """Extract task ID number"""
        import re
        numbers = re.findall(r'\d+', message)
        return int(numbers[0]) if numbers else None
    
    async def generate_chat_response(self, user_message: str, action_result: Optional[Dict] = None) -> str:
        """Generate response"""
        if action_result and "response" in action_result:
            return action_result["response"]
        return "I'll help you manage your tasks."

def get_gemini_assistant() -> GeminiAssistant:
    """Get assistant instance"""
    return GeminiAssistant()

# Test function
if __name__ == "__main__":
    import asyncio
    
    async def test():
        try:
            print("🧪 Testing Gemini Assistant...")
            assistant = get_gemini_assistant()
            print("✅ Gemini initialized successfully!")
            
            # Test cases
            test_cases = [
                ("Add task to buy milk", "add_task"),
                ("Show my pending tasks", "list_tasks"),
                ("Complete task 3", "complete_task"),
                ("Delete task 2", "delete_task"),
                ("What can you do?", "unknown"),
                ("Hello", "unknown"),
                ("Add groceries to my list", "add_task"),
            ]
            
            for message, expected_action in test_cases:
                print(f"\n{'='*60}")
                print(f"📝 Message: '{message}'")
                result = await assistant.analyze_message(message)
                print(f"✅ Action: {result['action']} (expected: {expected_action})")
                print(f"💬 Response: {result['response']}")
                print(f"🎯 Confidence: {result['confidence']}")
                
                if result['parameters'].get('title'):
                    print(f"📌 Title: {result['parameters']['title']}")
                if result['parameters'].get('task_id'):
                    print(f"🔢 Task ID: {result['parameters']['task_id']}")
            
            print(f"\n{'='*60}")
            print("🎉 All tests completed!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Troubleshooting:")
            print("1. Run: pip install google-genai")
            print("2. Check .env file has GEMINI_API_KEY")
            print("3. Get API key from: https://makersuite.google.com/app/apikey")
    
    asyncio.run(test())