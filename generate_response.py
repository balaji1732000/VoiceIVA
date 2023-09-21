import openai
import json
import streamlit as st
from speech_func import Speech
from function_call import Functions_call


# create an object for the function_call class

function_call = Functions_call()

openai.api_key = "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"


class response_function:
    @staticmethod
    def generate_response(input_text, conversation_history):
        intial_prompt = (
            "picture this: you're a tech pro or business owner facing a snag. That's where I step in. I'll guide you step by step to fix your tech hiccup.\n"
            "Please provide these: 1. Describe the issue. 2. Your OS and browser? 3. When did it start? Any changes?\n"
            "4. Steps taken? 5. Any error messages? I'll use my knowledge to help. Let's tackle tech troubles together!\n"
            "you'll sprinkle in those filler words like 'Um,' 'Er,' 'Uh,' 'Ah,' and 'Hmm' for more human-like conversation.\n"
            "And, er, I'll keep my responses, ah, within 50 words or less for, um, simplicity."
        )
        messages = [
            {
                "role": "system",
                "content": intial_prompt,
            },
        ]

        messages.extend(conversation_history)
        messages.append({"role": "user", "content": input_text})
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA, Bangalore",
                        },
                        "unit": {"type": "string", "enum": ["celsius"]},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "send_email",
                "description": "Send mail to the given email and subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_email": {
                            "type": "string",
                            "description": "The email or gmail,  e.g. balaji@gmail.com, abhijeet@wipro.com",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Subject of the email or gmail, e.g. Can you fix meet today, What is the status of the task",
                        },
                        "content": {
                            "type": "string",
                            "description": "Content of the email or gmail, e.g. Dear Subscriber, We are excited to introduce our monthly newsletter, where you'll discover the latest updates, news, and exclusive offers from our company.",
                        },
                    },
                    "required": ["to_email", "subject", "content"],
                },
            },
        ]

        # response = openai.Completion.create(
        #     engine="text-davinci-002",
        #     messages=messages,
        # )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        print(response)
        response_message = response["choices"][0]["message"]

        if response_message.get("function_call"):
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_current_weather": function_call.get_current_weather,
                "send_email": function_call.send_email,
            }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])

            if function_name == "get_current_weather":
                location = function_args.get("location")
                function_response = function_to_call(location=location)
            elif function_name == "send_email":
                to_email = function_args.get("to_email")
                subject = function_args.get("subject")
                content = function_args.get("content")
                function_response = function_to_call(
                    to_email=to_email, subject=subject, content=content
                )
            # Step 4: send the info on the function call and function response to GPT
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response

            print(messages)
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )
            second_response_text = (
                second_response.choices[0].message["content"].replace('"', "")
            )  # get a new response from GPT where it can see the function response
            return second_response_text

        else:
            response_text = response.choices[0].message["content"].replace('"', "")
            return response_text
