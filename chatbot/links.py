"""
import openai
import re

def getResponse(user_input):
    # Set up OpenAI API credentials
    openai.api_key = "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"

    # Send the user input to OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
    )

    # Extract and print the response from OpenAI
    response = completion.choices[0].message['content']
    print("Response: ", response)
    
    # Access and extract links from the response
    links = re.findall(r'(https?://\S+)', response)
    for link in links:
        print("Link: ", link)
        
    return response, links

# Test the function
user_input = "Can you provide some information about programming?"
response, links = getResponse(user_input)

# You can now use the 'response' and 'links' variables to display the content in your frontend,
# making the links clickable if needed.

""" 
import openai

def processResponse(response):
    """Process the GPT-3 response."""
    # Extract the messages from the response
    messages = response['choices'][0]['message']['messages']
    
    # Loop through each message in the response
    for message in messages:
        role = message['role']
        content = message['content']
        
        # Print the content based on the role
        if role == 'user':
            print(f"User: {content}")
        elif role == 'assistant':
            print(f"Assistant: {content}")
        elif role == 'system':
            print(f"System: {content}")

            # Check if the content contains a link or code block
            if '<link>' in content:
                # Extract the link and print it
                link = content.split('<link>')[1].split('</link>')[0]
                print(f"Clickable Link: {link}")
            elif '<code>' in content:
                # Extract the code block and print it
                code = content.split('<code>')[1].split('</code>')[0]
                print("Code Block:")
                print(code)
        else:
            # Handle other roles if needed
            pass

# Set up OpenAI API credentials
openai.api_key = "your_api_key_here"

# Send the user input to OpenAI
response = openai.ChatCompletion.create(
    model="text-davinci-003",  # Adjust the model as needed
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, GPT-3!"},
    ],
    max_tokens=150,  # Adjust the max tokens as needed
    temperature=0.7,  # Adjust the temperature as needed
)

# Process and print the response
processResponse(response)

