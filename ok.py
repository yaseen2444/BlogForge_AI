import google.generativeai as genai

genai.configure(api_key="AIzaSyD-SwiNkOOsg2zP0emA9M5XxdSzlW4p7hM")

models = genai.list_models()
for model in models:
    print(model.name)
