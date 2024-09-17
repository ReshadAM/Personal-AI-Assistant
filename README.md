# JUNE | The Personal AI Assistant: Final Project-Harvard University's CS50 course
#### Video Demo: [Watch on YouTube](https://www.youtube.com/watch?v=mI_MglLQMS8)

#### Description:
June is a personal AI assistant built with Python, capable of handling a wide range of tasks through a natural conversational interface. Designed to simulate human-like interactions, June helps users manage daily activities such as adding items to shopping lists, creating and appending data to files, and even performing more advanced tasks like putting your device to sleep. Inspired by Amazon's Alexa, June was crafted to offer more intelligent responses and handle requests with greater precision. One of June's standout features is its scalability; by leveraging its training data, users can easily enhance June's capabilities and achieve accurate outputs with simple English commands. Many of June’s behaviors can be customized by adjusting its underlying training model, making it adaptable for various use cases.

June’s primary purpose is to boost productivity by offering a seamless interface for text-based and voice-based interactions. Powered by OpenAI's GPT-4 for generating intelligent responses, Eleven Labs' API for realistic voice synthesis, and Google Cloud’s Speech-to-Text for recognizing verbal input, June can dynamically engage with users, generate human-like audio responses, and carry out tasks in real-time. It blends cutting-edge machine learning with user-friendly controls, providing personalized interactions that enhance user experience.

## TODO

### `project.py`
This is the core file of the project. It contains the logic that handles the interaction between the user and the AI system. Key features include:
- **Chat with AI**: June processes user input and responds using OpenAI's GPT model. Users can choose to interact via text or voice commands.
- **Special Commands**: June supports custom commands such as adding items to a shopping list, creating files, and appending data to files.
- **File Operations**: Users can create files, modify content, and manage shopping lists using June. File operations are executed with confirmation prompts to ensure proper user control.
- **Voice Responses**: June generates voice responses using the Eleven Labs API, providing an audible output for users.
- **Error Handling**: The project includes error management and prompts the user in case of file-related or AI-related issues.

### `GPT.py`
This file contains the `MyAI` class, which interfaces with OpenAI’s GPT API. It handles communication with the GPT model to generate responses based on user input and June's training data.

### `elevenAPI.py`
This file includes the `ElevenAPI` class, which interacts with the Eleven Labs API for voice generation. It allows June to convert text-based AI responses into audio, creating a more interactive experience.

### `speech_to_text.py`
This file contains functions to handle speech-to-text conversion using Google Cloud’s Speech-to-Text API. It allows users to give voice commands, which are then transcribed and processed as text.

### `JUNE_TRAINING_DATA` (directory)
This directory stores the training data used to customize June's behavior and ability to perform specialized tasks. By modifying the files in this directory, users can adjust June’s responses and interactions with the OpenAI GPT model, fine-tuning the AI assistant for specific use cases or personal preferences.

### `created_files` (directory)
This directory stores all the files created by June during user interactions. Whenever a user asks June to create or modify a file, those files are stored in this directory, organized for easy access and management.

### `audio_files` (directory)
This directory contains pre-generated audio files used by June, including the introductory greeting when the AI is launched. If the audio file for June’s introduction is missing, it is automatically regenerated using the Eleven Labs API.

### `requirements.txt`
This file lists all the Python modules and dependencies used in the project. It ensures that anyone running the project has the correct versions of the libraries required for June to function.

### `.env`
This file securely stores environment variables such as API keys. It ensures that sensitive information like the OpenAI API key, Eleven Labs API key, and Google Cloud Speech-to-Text credentials are not hardcoded into the source code. These variables are loaded into the application at runtime using the `dotenv` package, allowing June to access external services while keeping the credentials private and secure.

**Key variables include:**
- `OPENAI_API_KEY`: API key for interacting with the OpenAI GPT-4 API.
- `ELEVENLABS_API_KEY`: API key for the Eleven Labs voice synthesis service.
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to the credentials file for Google Cloud’s Speech-to-Text API.

### `test_project.py`
This file contains unit tests for validating the functionality of June's core features. Using the `pytest` framework, it ensures that key functions like file creation, data appending, and shopping list updates behave as expected. The test cases simulate real-world scenarios to confirm that June handles user commands properly and responds appropriately.
