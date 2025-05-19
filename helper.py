# 初始化deepseek
# client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

class OpenAI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url


class DeepSeeker:
    def __init__(self, client):
        self.client = client

    # def ask(self, question):
    #     response = self.client.chat.completions.create(
    #         model="deepseek-chat",
    #         messages=[
    #             {"role": "user", "content": question},
    #         ],
    #         stream=False
    #     )
    #     return response.choices[0].message.content

    def ask(self, question):
        return 'haha'

    def __str__(self):
        return "Hi,this is DeepSeeker."