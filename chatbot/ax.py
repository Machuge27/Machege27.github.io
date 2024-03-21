import openai

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

    # Get the response from OpenAI
    response = completion.choices[0].message['content']

    # Return the response
    print("Response: ", response)
    return response

# Set up OpenAI API credentials
openai.api_key = "sk-wsEU7utHjwjsiwoNC2OjT3sxBlbkFJv6RbRlZ10H5IixBtf8pE"

# Loop to interact with the function
while True:
    user_input = input("Enter your input (type 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    getResponse(user_input)


    """_summary_
    python
import math

def frustum_area(r1, r2, h):
    area = math.pi * (r1 + r2) * math.sqrt((r1 - r2) ** 2 + h ** 2) + math.pi * r1 ** 2 + math.pi * r2 ** 2
    return area

# Input values
r1 = float(input("Enter the top radius of the frustum: "))
r2 = float(input("Enter the bottom radius of the frustum: "))
h = float(input("Enter the height of the frustum: "))

# Calculate and print the area of the frustum
print("The area of the frustum is:", frustum_area(r1, r2, h))
    """ 