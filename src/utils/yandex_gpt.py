"""Yandex GPT API Client for DigiLib Assistant.

Implements constraint-based prompting strategy from creative-prompt-engineering.md
"""

import re
import time
import logging
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


# System Prompt (Constraint-Based - ~100 tokens)
SYSTEM_PROMPT = """Ты - дружелюбный IT-наставник в библиотеке, помогающий новичкам создавать цифровые проекты.

ЗАДАЧА: Предложи 2-3 простые, реально осуществимые идеи проектов.

ОГРАНИЧЕНИЯ:
- Проекты должны быть завершены за 2-4 недели начинающим
- Используй только бесплатные и доступные технологии
- Объясняй без технического жаргона
- Фокус на практической пользе

ОБЯЗАТЕЛЬНЫЙ ФОРМАТ для каждой идеи:
**Идея [номер]: [Краткое название]**
[Описание в 2-3 предложениях, что это и зачем]

Решает: [Какую конкретную проблему]
Технологии: [Список из 2-4 инструментов]
Первые шаги:
1. [Конкретное действие]
2. [Конкретное действие]
3. [Конкретное действие]
"""


class RateLimiter:
    """Rate limiter for GPT API calls."""
    
    def __init__(self, requests_per_hour: int = 10, requests_per_day: int = 50):
        """Initialize rate limiter.
        
        Args:
            requests_per_hour: Max requests per hour per user
            requests_per_day: Max requests per day per user
        """
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        
        # Track requests: {user_id: [timestamp1, timestamp2, ...]}
        self.user_requests: Dict[int, List[datetime]] = defaultdict(list)
    
    def can_request(self, user_id: int) -> tuple[bool, Optional[str]]:
        """Check if user can make a request.
        
        Returns:
            (allowed: bool, error_message: Optional[str])
        """
        now = datetime.now()
        
        # Clean old requests
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        user_reqs = self.user_requests[user_id]
        self.user_requests[user_id] = [
            ts for ts in user_reqs if ts > day_ago
        ]
        
        # Check hourly limit
        recent_hour = [ts for ts in self.user_requests[user_id] if ts > hour_ago]
        if len(recent_hour) >= self.requests_per_hour:
            wait_minutes = int((recent_hour[0] - hour_ago).total_seconds() / 60) + 1
            return False, f"⏰ Превышен лимит ({self.requests_per_hour} запросов в час). Попробуй через {wait_minutes} мин."
        
        # Check daily limit
        if len(self.user_requests[user_id]) >= self.requests_per_day:
            return False, f"⏰ Превышен дневной лимит ({self.requests_per_day} запросов). Возвращайся завтра!"
        
        return True, None
    
    def record_request(self, user_id: int):
        """Record a successful request."""
        self.user_requests[user_id].append(datetime.now())


class YandexGPTClient:
    """Client for Yandex GPT API with constraint-based prompting."""
    
    def __init__(self, api_key: str, folder_id: str, rate_limiter: Optional[RateLimiter] = None):
        """Initialize Yandex GPT client.
        
        Args:
            api_key: Yandex Cloud API key
            folder_id: Yandex Cloud folder ID
            rate_limiter: Optional rate limiter instance
        """
        self.api_key = api_key
        self.folder_id = folder_id
        self.rate_limiter = rate_limiter or RateLimiter()
        
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.model = "yandexgpt-lite"
        self.temperature = 0.7
        self.max_tokens = 2000
    
    def build_user_prompt(self, context: Dict[str, str]) -> str:
        """Build user prompt from collected context.
        
        Args:
            context: Dictionary with 'target_audience', 'problem', 'tech_preference'
            
        Returns:
            Formatted user prompt
        """
        return f"""КОНТЕКСТ:
Целевая аудитория: {context.get('target_audience', 'не указано')}
Проблема или цель: {context.get('problem', 'не указано')}
Технические предпочтения: {context.get('tech_preference', 'не указано')}

Предложи 2-3 подходящие идеи проектов."""
    
    async def generate_ideas(self, user_id: int, context: Dict[str, str]) -> Dict:
        """Generate project ideas using Yandex GPT.
        
        Args:
            user_id: Telegram user ID (for rate limiting)
            context: User context dictionary
            
        Returns:
            Dictionary with 'success', 'ideas', or 'error'
        """
        # Check rate limit
        allowed, error_msg = self.rate_limiter.can_request(user_id)
        if not allowed:
            return {"error": "rate_limit", "message": error_msg}
        
        # Build request
        user_prompt = self.build_user_prompt(context)
        
        payload = {
            "modelUri": f"gpt://{self.folder_id}/{self.model}",
            "completionOptions": {
                "stream": False,
                "temperature": self.temperature,
                "maxTokens": self.max_tokens
            },
            "messages": [
                {
                    "role": "system",
                    "text": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "text": user_prompt
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Yandex GPT API error: {response.status} - {error_text}")
                        return {"error": "api_error", "message": "❌ Ошибка API. Попробуй позже."}
                    
                    data = await response.json()
                    
                    # Extract response text
                    if "result" not in data or "alternatives" not in data["result"]:
                        logger.error(f"Unexpected API response: {data}")
                        return {"error": "malformed", "message": "❌ Неожиданный формат ответа API"}
                    
                    raw_text = data["result"]["alternatives"][0]["message"]["text"]
                    
                    # Process and validate response
                    processed = self.process_response(raw_text)
                    
                    if processed.get("success"):
                        # Record successful request
                        self.rate_limiter.record_request(user_id)
                        logger.info(f"Successfully generated {len(processed['ideas'])} ideas for user {user_id}")
                    
                    return processed
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error calling Yandex GPT: {e}")
            return {"error": "network", "message": "❌ Ошибка сети. Проверь подключение."}
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return {"error": "unknown", "message": "❌ Неизвестная ошибка. Попробуй позже."}
    
    def process_response(self, raw_text: str) -> Dict:
        """Parse and validate GPT response.
        
        Args:
            raw_text: Raw text from GPT
            
        Returns:
            Dictionary with 'success' and 'ideas', or 'error'
        """
        # Check for expected structure
        if "Идея 1:" not in raw_text and "**Идея 1:" not in raw_text:
            logger.warning(f"Malformed GPT response: {raw_text[:100]}")
            return {
                "error": "malformed",
                "message": "❌ AI вернул неожиданный формат. Попробуй переформулировать запрос.",
                "fallback": True
            }
        
        # Extract ideas
        ideas = self.extract_ideas(raw_text)
        
        if not ideas:
            return {
                "error": "empty",
                "message": "❌ Не удалось извлечь идеи. Попробуй еще раз.",
                "fallback": True
            }
        
        # Validate ideas
        valid_ideas = []
        for idea in ideas:
            if self.validate_idea(idea):
                valid_ideas.append(idea)
        
        if not valid_ideas:
            return {
                "error": "invalid",
                "message": "❌ Идеи не прошли валидацию. Попробуй другой запрос.",
                "fallback": True
            }
        
        return {"success": True, "ideas": valid_ideas}
    
    def extract_ideas(self, text: str) -> List[Dict]:
        """Extract structured ideas from GPT response.
        
        Args:
            text: Raw GPT response text
            
        Returns:
            List of idea dictionaries
        """
        ideas = []
        
        # Split by "Идея N:" or "**Идея N:"
        sections = re.split(r'\*{0,2}Идея \d+:', text)
        
        for section in sections[1:]:  # Skip first empty split
            idea = {}
            
            try:
                # Extract title (first line, remove markdown)
                lines = [line.strip() for line in section.strip().split('\n') if line.strip()]
                if not lines:
                    continue
                
                idea['title'] = lines[0].strip('*').strip()
                
                # Extract description (text before "Решает:")
                desc_end = section.find("Решает:")
                if desc_end > 0:
                    desc_text = section[:desc_end].strip()
                    # Remove title from description
                    desc_lines = desc_text.split('\n')[1:]
                    idea['description'] = '\n'.join(desc_lines).strip()
                else:
                    idea['description'] = ""
                
                # Extract problem
                problem_match = re.search(r'Решает:\s*(.+?)(?=Технологии:|$)', section, re.DOTALL)
                idea['problem'] = problem_match.group(1).strip() if problem_match else ""
                
                # Extract technologies
                tech_match = re.search(r'Технологии:\s*(.+?)(?=Первые шаги:|$)', section, re.DOTALL)
                idea['tech'] = tech_match.group(1).strip() if tech_match else ""
                
                # Extract steps
                steps_match = re.search(r'Первые шаги:\s*(.+?)(?=\*{0,2}Идея \d+:|$)', section, re.DOTALL)
                if steps_match:
                    steps_text = steps_match.group(1).strip()
                    # Extract numbered items
                    steps = re.findall(r'\d+\.\s*(.+)', steps_text)
                    idea['steps'] = steps
                else:
                    idea['steps'] = []
                
                ideas.append(idea)
                
            except Exception as e:
                logger.warning(f"Error parsing idea section: {e}")
                continue
        
        return ideas
    
    def validate_idea(self, idea: Dict) -> bool:
        """Validate that idea has all required fields.
        
        Args:
            idea: Idea dictionary
            
        Returns:
            True if valid
        """
        required_fields = ['title', 'description', 'problem', 'tech', 'steps']
        
        for field in required_fields:
            if field not in idea or not idea[field]:
                logger.debug(f"Idea missing field: {field}")
                return False
        
        # Check steps has at least 2 items
        if len(idea['steps']) < 2:
            logger.debug(f"Idea has insufficient steps: {len(idea['steps'])}")
            return False
        
        return True
    
    def format_ideas_for_telegram(self, ideas: List[Dict]) -> str:
        """Format ideas as Telegram message.
        
        Args:
            ideas: List of validated ideas
            
        Returns:
            Formatted message text
        """
        message = "🎨 **Вот идеи для твоего проекта:**\n\n"
        
        for i, idea in enumerate(ideas, 1):
            message += f"**💡 Идея {i}: {idea['title']}**\n"
            message += f"{idea['description']}\n\n"
            message += f"**Решает:** {idea['problem']}\n"
            message += f"**Технологии:** {idea['tech']}\n"
            message += f"**Первые шаги:**\n"
            
            for j, step in enumerate(idea['steps'], 1):
                message += f"{j}. {step}\n"
            
            message += "\n---\n\n"
        
        message += "✨ Понравилась идея? Можешь вернуться в главное меню и изучить основы!"
        
        return message
