# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from google import genai
# import time

# load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")


# if not api_key:
#     raise ValueError("GOOGLE_API_KEY not found in .env!")


# # # List all the available models 


# # # client = genai.Client(api_key = api_key)

# # # print("Avaiable Models:\n")

# # # for model in client.models.list():
# # #     print(model.name)

# # llm = GoogleGenerativeAI(
# #     model = "gemini-2.5-flash",
# #     google_api_key = api_key,
# #     temperature = 0.2
# # )

# # prompt = "What is Function in cpp in simple terms"

# # response = llm.invoke(
# #     [HumanMessage(content=prompt)]
# # )

# # print(response)


# from google import genai

# # client = genai.Client(api_key=api_key)

# # start = time.time()
# # response = client.models.generate_content(
# #     model="gemini-3.1-flash-lite",
# #     contents="What is Function in cpp in simple terms"
# # )
# # print(f"Time taken: {time.time() - start:.2f} seconds")
# # print(response.text)


# client = genai.Client(api_key=api_key)
# from google.genai import types
# start = time.time()
# result = client.models.generate_images(
#     model="imagen-3.0-generate-002",
#     prompt="What is Function in cpp in simple terms",
#     config=types.GenerateImagesConfig(
#         number_of_images=1,
#         output_mime_type="image/jpeg",
#         # Supports high-fidelity resolution configurations
#         aspect_ratio="1:1" 
#     )
# )

# for i, generated_image in enumerate(result.generated_images):
#     with open(f"output_image_{i}.jpg", "wb") as f:
#         f.write(generated_image.image.image_bytes)

# print("Image generated successfully via gemini-3-pro-image.")




# #gemini-3-pro-image



import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# start = time.time()
# result = client.models.generate_images(
#     model="imagen-3.0-generate-002",
#     prompt="A stylized conceptual blueprint chart explaining functions in computer programming",
#     config=types.GenerateImagesConfig(
#         number_of_images=1,
#         output_mime_type="image/jpeg",
#         aspect_ratio="1:1" 
#     )
# )

# for i, generated_image in enumerate(result.generated_images):
#     with open(f"output_image_{i}.jpg", "wb") as f:
#         f.write(generated_image.image.image_bytes)

# print(f"Image generated successfully in {time.time() - start:.2f} seconds.")
client = genai.Client(api_key=api_key)

print("Checking your API key permissions...")
print("====================================")

# Loop through all models available to your specific API key
for model in client.models.list():
    # Capture the actions this specific model is capable of performing
    actions = model.supported_actions
    
    # Check if the model supports image generation or content generation
    if "generate_images" in actions or "generateImages" in actions:
        print(f"[IMAGE MODEL] -> {model.name}")
    elif "generate_content" in actions or "generateContent" in actions:
        print(f"[TEXT MODEL]  -> {model.name}")


response = client.models.generate_content(
    model="gemini-3-pro-image",
    contents="A high-quality, clear conceptual diagram explaining functions in C++ in simple terms, minimalist style"
)

try:
    for candidate in response.candidates:
        for part in candidate.content.parts:
            # Check if the part contains image/inline data
            if hasattr(part, 'inline_data') and part.inline_data:
                with open("output_image.jpg", "wb") as f:
                    f.write(part.inline_data.data)
                print(f"Image generated successfully in {time.time() - start:.2f} seconds!")
                break
except Exception as e:
    print(f"Could not parse image data: {e}")
    # If the model returned text explanation instead of drawing an image, print it
    print("Response text:", response.text)