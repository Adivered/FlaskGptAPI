# from genericpath import exists
from application import app
from flask import jsonify, request
from openai import OpenAI
from openai.error import OpenAIError, InvalidRequestError  # Import specific exceptions
import os, re

try:
    client = OpenAI()
except:
    print("No key has been found")


def gpt_execute(prompt_template, *args, **kwargs):
    verbose = kwargs.pop("verbose", False)
    max_tokens = kwargs.pop("max_tokens", 256)
    prompt = prompt_template.format(*args)
    message = [
        {"role": "user", "content": prompt},
    ]
    model = "gpt-4-turbo"
    temperature = 1
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0

    try:  # Sometimeds GPT returns HTTP 503 error
        response = client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            top_p=top_p,
        )
        if verbose:
            print(kwargs)
            print("Top K {}".format([x["index"] for x in response["choices"]]))
            print(
                "Top prompt_tokens : {} total_tokens: {}".format(
                    response["usage"]["prompt_tokens"],
                    response["usage"]["total_tokens"],
                )
            )

        return jsonify(response.choices[0].message.content)

    except (OpenAIError, InvalidRequestError) as e:
        print(f"OpenAI API error: {e}")
        return jsonify({"error": "OpenAI API error", "message": str(e)}), 500

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@app.route("/home", methods=["POST"])
def home():
    try:
        # Assuming prompt is coming from request body
        prompt = request.json
        res = gpt_execute(prompt_template=prompt)
        return res, 200

    except KeyError as e:
        print(f"Key error: {e}")
        return jsonify({"error": "Key error", "message": str(e)}), 400
    except ValueError as e:
        print(f"Value error: {e}")
        return jsonify({"error": "Value error", "message": str(e)}), 400
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500
