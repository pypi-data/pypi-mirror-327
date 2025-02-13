# Automate-GPT

`Automate-GPT` is a Python library that allows users to automate interactions with ChatGPT through a web driver. This library simplifies the process of sending prompts to ChatGPT and receiving responses in an automated manner.

---

## Features

- Automate interactions with ChatGPT.
- Use an undetected Chrome driver to bypass detection.
- Simplified interface for sending prompts and retrieving responses.
- Supports Reset Chat feature to clear the chat history.
- Supports Search internet feature to search for information.
---

## Installation

To install `Automate-GPT`, use pip:

```bash
pip install Automate-GPT
```

---

## Requirements

- Python 3.7 or higher
- [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)

---

## Usage

Here is a basic example of how to use the `Automate-GPT` library:

### Example

```python
from Automate_GPT import ChatGPTAutomation
import undetected_chromedriver as uc

# Initialize the undetected Chrome driver
driver = uc.Chrome()

# Initialize ChatGPTAutomation with the Chrome driver
chatbot = ChatGPTAutomation(driver)
response = chatbot.chat("What is the capital of France?")
print(response)  # Output: Paris
chatbot.reset_chat()
chatbot.search_enable(False)
chatbot.get_conversation()
```

---

## API Reference

### `Automate_GPT.ChatGPTAutomation`

A class to automate interactions with ChatGPT.

#### **`__init__(self, driver: undetected_chromedriver.Chrome)`**

Initializes the `ChatGPTAutomation` instance.

- **Parameters**:
  - `driver` (*undetected_chromedriver.Chrome*): The Chrome web driver instance for interacting with ChatGPT.

#### **`prompt(self, prompt: str) -> str`**

Sends a prompt to ChatGPT and retrieves the response.

- **Parameters**:
  - `prompt` (*str*): The text prompt to send to ChatGPT.
- **Returns**:
  - (*str*): The response from ChatGPT.

#### **`reset_chat(self)`**
Resets the chat history.

#### **`search_enable(self, enable: bool)`**
Enables or disables the search internet feature.
- **Parameters**:
  - `enable` (*bool*): Whether to enable or disable the search internet feature.
#### **`get_conversation(self) -> list[dict]`**
Retrieves the conversation history.
- **Returns**:
  - (*list[dict]*): The conversation history.
---
## Notes

- Ensure you have the latest version of Chrome and the corresponding chromedriver installed.
- `undetected-chromedriver` is used to prevent detection during automated browser interactions.

---
## Acknowledgments
Created by [Sheth Jenil](https://github.com/dummyjenil/)