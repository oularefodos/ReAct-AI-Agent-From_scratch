import yaml
import json
from groq import Groq
from dotenv import load_dotenv
import os
from colorama import Fore, Style
from src.helpers import extract_first_json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Agent(object):
    def __init__(self, groq_model_name="llama-3.3-70b-versatile", tools=[]):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.tools = {tool.name: tool for tool in tools}
        self.client = Groq(api_key=api_key)
        self.groq_model_name = groq_model_name
        self.system_prompt = self.load_system_prompt()
        self.messages = [{"role": "system", "content": str(self.system_prompt)}]
    
    def chat_completion(self):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=self.messages,
                model=self.groq_model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return {"error": str(e)}

    def load_system_prompt(self):
        try:
            with open("prompt.txt", "r") as file:
                prompt_text = file.read() # Read the plain text prompt
        except FileNotFoundError:
            print("Error: prompt.txt not found.")
            prompt_text = ""
            exit(1)
        
        # Build the system prompt as a dictionary
        tools_info = []
        for tool in self.tools:
            tools_info.append(f"({tool})")
        
        system_prompt = prompt_text.replace("{tools}", json.dumps(tools_info))
        return system_prompt
    
    def update_history(self, message, role="assistant"):
        self.messages.append({"content": message, "role": role});
    
    def observation(self, observation):
        self.update_history(f"last Observation: {observation}")
    
    def action(self, action):
        tool = self.tools.get(action["name"])
        if tool:
            return tool(action.get("input", None))
        else:
            return f"Tool {action['name']} not found"
    
    def think(self):
        try:
            response = self.chat_completion()
            response_parsed = extract_first_json(response)
            self.update_history("Last Thought: " + str(response_parsed))
            return response_parsed;
        except json.JSONDecodeError:
            error_msg = "Failed to decode JSON response, You must return only JSON format not string"
            self.update_history(error_msg)
            return error_msg
        except:
            self.update_history("An expected error occurred.")
            print("An expected error occurred.")
    
    def __call__(self, message, max_iterations=5):
        self.update_history(message, role="user");
        iterations = 0
        logger.info("Thinking...")
        while iterations < max_iterations:
            response_in_json = self.think()
            iterations += 1

            if "thought" in response_in_json:
                print(Fore.GREEN + f"{response_in_json["thought"]}" + Style.RESET_ALL)

            if "action" in response_in_json:
                try:
                    action = response_in_json["action"]
                    print(Fore.BLUE + f"Invoking {action['name']} because {action['reason']}" + Style.RESET_ALL)
                    output = self.action(action)
                    self.observation(output)
                except Exception as e:
                    try:
                        output = self.action(action)
                        self.observation(output)
                    except Exception as e:
                        self.observation(f"Error: {str(e)}")
            
            if "answer" in response_in_json:
                print("Finished thinking.");
                logger.info(f"Final answer: {response_in_json['answer']}")
                break
        else:
            print("Maximum iterations reached without a final answer.")
