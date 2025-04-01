import importlib.resources as pkg_resources

import os
import subprocess
import shutil
import argparse
from datetime import datetime
import signal
import sys
import json

from openai import OpenAI


class Logger:
    """
    A simple logger class to handle logging of messages.
    Logs are stored as individual JSON files with timestamps.
    """

    def __init__(self, log_dir):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.index = self._get_initial_index()

    def _get_initial_index(self):
        existing_logs = [
            int(f.split('.')[0]) for f in os.listdir(self.log_dir)
            if f.endswith('.json') and f.split('.')[0].isdigit()
        ]
        return max(existing_logs) + 1 if existing_logs else 0

    def log(self, message):
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            **message
        }
        log_file = os.path.join(self.log_dir, f"{self.index}.json")
        with open(log_file, "w") as f:
            json.dump(log_entry, f, indent=2)
        self.index += 1


def parse_args():
    parser = argparse.ArgumentParser(description="Run AI-powered research tasks.")
    parser.add_argument("research_path", type=str, help="Path to research directory")
    parser.add_argument("--research_name", default="", help="Name of the research task")
    parser.add_argument("--model-name", default="gpt-4o", help="OpenAI model name")
    parser.add_argument("--max-messages", type=int, default=1000, help="Maximum number of messages")
    parser.add_argument("--restart", action="store_true", help="Restart the research task by removing existing data")
    return parser.parse_args()


def load_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return ""


def execute_action(action, research_dir):
    action_type = action.get("action")
    response = ""

    if action_type == "run":
        script = action.get("script", "")
        time_limit = action.get("tl", None)
        command = f"bash -c '{script}'"
        try:
            if time_limit:
                result = subprocess.run(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=int(time_limit)
                )
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            stdout = result.stdout.decode('utf-8').strip()
            stderr = result.stderr.decode('utf-8').strip()
            response = f"stdout:\n{stdout}\n\nstderr:\n{stderr}"
        except subprocess.TimeoutExpired:
            response = "Error: Script execution timed out."

    elif action_type == "read":
        fp = action.get("fp", "")
        fp = os.path.abspath(fp)
        if not os.path.exists(fp):
            response = f"The file {fp} does not exist."
        elif os.path.isdir(fp):
            response = f"The path {fp} is a directory."
        else:
            response = load_file(fp)

    elif action_type == "write":
        fp = action.get("fp", "")
        content = action.get("content", "")
        fp = os.path.abspath(fp)
        # Ensure the file path is within the research directory
        if not fp.startswith(os.path.abspath(research_dir)):
            response = f"Error: Access to {fp} is denied."
        else:
            dirpath = os.path.dirname(fp)
            os.makedirs(dirpath, exist_ok=True)
            try:
                with open(fp, "w") as f:
                    f.write(content)
                response = f"The file {fp} has been written."
            except Exception as e:
                response = f"Error writing to {fp}: {str(e)}"

    elif action_type == "to_human":
        question = action.get("question", "No question provided.")
        user_input = input(f"Human Consultation - {question}\n> ").strip()
        response = user_input

    else:
        response = f"Unknown action: {action_type}"

    return response


def signal_handler(sig, frame):
    print("\nInterrupt received, shutting down gracefully...")
    sys.exit(0)


def load_messages_from_logs(log_dir):
    """
    Load messages from log JSON files in the specified log directory.
    Returns a list of message dictionaries sorted by index.
    """
    messages = []
    if not os.path.exists(log_dir):
        return messages

    log_files = [f for f in os.listdir(log_dir) if f.endswith('.json') and f.split('.')[0].isdigit()]
    # Sort log files based on index
    log_files_sorted = sorted(log_files, key=lambda x: int(x.split('.')[0]))
    for log_file in log_files_sorted:
        with open(os.path.join(log_dir, log_file), "r") as f:
            log_entry = json.load(f)
            role = log_entry.get("role")
            content = log_entry.get("content", "")
            messages.append({"role": role, "content": content})
    return messages


def extract_json(content):
    """
    Extract JSON string from a Markdown code block if present.
    """
    if content.startswith("```json"):
        if not content.endswith("```"):
            return "",False
        content = content[7:-3].strip()
    return content,True

def get_prompts():
    """
    Load the research and mistake prompt text files from the package assets.
    Returns:
        A tuple (research_prompt, mistake_prompt)
    """
    research_prompt = pkg_resources.read_text("ai_scientist.assets.prompts", "research_prompt.txt")
    mistake_prompt = pkg_resources.read_text("ai_scientist.assets.prompts", "mistake_prompt.txt")
    return {"research_prompt": research_prompt, "mistake_prompt": mistake_prompt}

def main():
    # Handle termination signals gracefully
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = parse_args()
    data_dir = args.research_path
    research_name = args.research_name
    if research_name == "":
        research_name = os.path.basename(data_dir)
    model_name = args.model_name
    max_messages = args.max_messages
    restart = args.restart
    print(f"===== Starting research task: {research_name} =====\n")

    # Define directories
    thisfile = os.path.abspath(__file__)
    research_dir = os.path.join(data_dir, f"{research_name}")
    log_dir = os.path.join(research_dir, "logs")

    # Load prompts
    prompts=get_prompts()
    research_prompt=prompts["research_prompt"].replace("RESEARCH_NAME",research_name)
    mistake_prompt=prompts["mistake_prompt"].replace("RESEARCH_NAME",research_name)


    if restart:
        # If --restart is provided, remove existing research directory
        print(">> Restart flag detected. Removing existing research data...\n")
        shutil.rmtree(research_dir, ignore_errors=True)
        # Setup research directory
        os.makedirs(log_dir, exist_ok=True)
        # Initialize messages with initial_message
        research_prompt_combined = research_prompt
        initial_message = {"role": "user", "content": research_prompt_combined,"auto_user":False}
        messages = [initial_message]
        # Initialize logger and log the initial message
        logger = Logger(log_dir)
        logger.log(initial_message)
    else:
        # If not restarting, check if research_dir exists
        if os.path.exists(research_dir):
            print(">> Research directory detected. Loading previous messages...\n")
            # Load messages from log_dir
            messages = load_messages_from_logs(log_dir)
            if not messages:
                print(">> No messages found in research directory. Starting fresh...\n")
                shutil.rmtree(research_dir, ignore_errors=True)
                os.makedirs(log_dir, exist_ok=True)
                # Initialize messages with initial_message
                research_prompt_combined = research_prompt
                initial_message = {"role": "user", "content": research_prompt_combined,"auto_user":False}
                messages = [initial_message]
                # Initialize logger and log the initial message
                logger = Logger(log_dir)
                logger.log(initial_message)
            else:
                print(f">> Loaded {len(messages)} messages from research directory.\n")
                # Initialize logger with research_log_dir
                logger = Logger(log_dir)
        else:
            print(">> No research directory found. Starting fresh...\n")
            # Remove existing research directory if it exists
            shutil.rmtree(research_dir, ignore_errors=True)
            # Setup research directory
            os.makedirs(log_dir, exist_ok=True)
            # Initialize messages with initial_message
            research_prompt_combined = research_prompt
            initial_message = {"role": "user", "content": research_prompt_combined,"auto_user":False}
            messages = [initial_message]
            # Initialize logger and log the initial message
            logger = Logger(log_dir)
            logger.log(initial_message)

    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    while True:
        if len(messages) >= max_messages:
            print("\n===== Max messages reached. Ending session. =====")
            break

        try:
            response = client.beta.chat.completions.parse(
                model=model_name,
                messages=messages,
            )
        except Exception as e:
            print(f"\nError communicating with OpenAI: {str(e)}")
            break

        assistant_message = response.choices[0].message.model_dump()
        message_content = assistant_message.get("content", "").strip()

        # Extract JSON from Markdown code block if present
        clean_json,success = extract_json(message_content)

        messages.append({"role": "assistant", "content": clean_json})
        logger.log(assistant_message)

        # Print Assistant's message
        print("----- Assistant -----")
        print(message_content)
        print("---------------------\n")

        try:
            assert success
            data = json.loads(clean_json)
            actions = data.get("actions", [])
            # You can also access the summary if needed
            summary = data.get("summary", "")
            if summary:
                print(f"**Summary:** {summary}\n")
            if not isinstance(actions, list):
                raise ValueError("`actions` should be a list.")
            if len(actions) == 0:
                raise ValueError("No actions provided.")
        except json.JSONDecodeError as e:
            print(f"\n**Invalid JSON from AI:** {str(e)}\n")
            user_message = {"role": "user", "content": mistake_prompt,"auto_user":True}
            messages.append(user_message)
            logger.log(user_message)
            # Print User's message
            print("----- User -----")
            print(mistake_prompt)
            print("-----------------\n")
            continue
        except ValueError as ve:
            print(f"\n**Invalid action format:** {str(ve)}\n")
            user_message = {"role": "user", "content": mistake_prompt,"auto_user":True}
            messages.append(user_message)
            logger.log(user_message)
            # Print User's message
            print("----- User -----")
            print(mistake_prompt)
            print("-----------------\n")
            continue

        # Execute each action sequentially
        for action in actions:
            auto_user = False if "to_human" in action.get("action") else True
            user_content = execute_action(action, research_dir)
            user_message = {"role": "user", "content": user_content, "auto_user": auto_user}
            messages.append(user_message)
            logger.log(user_message)

            # Print User's message
            print("----- User -----")
            print(user_content)
            print("-----------------\n")

            # Check for termination condition
            if action.get("action") == "to_human" and user_content.strip().lower() == "quit":
                print("===== Closing research task... =====")
                return


if __name__ == "__main__":
    main()
