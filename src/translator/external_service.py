from openai import AsyncOpenAI


client = AsyncOpenAI()


async def translate_external_api(text: str, language: str) -> str:
    """
    This function takes two parameters: text and language.
    It uses the OpenAI API to translate the text into the given language.

    Parameters:
        text (str): The text to be translated.
        language (str): The target language for the translation.

    Returns:
        str: The translated text.

    Usage:
        result = asyncio.run(translate_external_api("Hello", "French"))
        print(result) # output can be: "Bonjour"
    """
    prompt = f"Translate the following text to {language}: '{text}'"

    response = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-3.5-turbo",
    )

    return response.choices[0].message.content.strip()
