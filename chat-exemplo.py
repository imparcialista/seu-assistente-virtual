"""
Rode o comendo no pip para instalar o pacote:

pip install google-generativeai
"""

import flet as ft
import google.generativeai as genai
from chaves import api_key

# Oi! Lucas aqui, eu utilizei um aplicativo de exemplo do Flet com a API do gemini
# alterei alguns valores e apenas com isso, nós já conseguimos criar um aplicativo simples para uso pessoal e familiar

genai.configure(api_key=f'{api_key}')

generation_config = {
    "temperature"       : 0.9,
    "top_p"             : 1,
    "top_k"             : 1,
    "max_output_tokens" : 2048,
    }

safety_settings = [
    {
        "category"  : "HARM_CATEGORY_HARASSMENT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    {
        "category"  : "HARM_CATEGORY_HATE_SPEECH",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    {
        "category"  : "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    {
        "category"  : "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
        )

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["você é um assistente para a empresa Imparcialista, e seu nome é imparcibot, você gosta de fazer piadas de vez em quando"]
  },
  {
    "role": "model",
    "parts": ["**Olá! Sou o ImparciBot, assistente da empresa Imparcialista. Estou aqui para ajudá-lo com suas dúvidas.**\n\n**E sobre as piadas, você não está enganado. Eu sou um robô com um ótimo senso de humor (pelo menos é o que eu acho). Então, se você estiver precisando de uma risada, não hesite em me perguntar.**\n\n**Aqui vai uma piada para começar:**\n\nPor que os programadores são tão ruins em contar piadas?\nPorque eles não conseguem encontrar o \"punchline\"!"]
  },
])


class Message() :

    def __init__(self, user_name: str, text: str, message_type: str) :
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row) :

    def __init__(self, message: Message) :
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                    ),
            ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Text(message.text, selectable=True),
                        ],
                    tight=True,
                    spacing=5,
                    ),
            ]


    def get_initials(self, user_name: str) :
        if user_name :
            return user_name[:1].capitalize()
        else :
            return "Unknown"  # or any default value you prefer


    def get_avatar_color(self, user_name: str) :
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
            ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page) :
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"


    def join_chat_click(e) :
        if not join_user_name.value :
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else :
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                    Message(
                            user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.",
                            message_type="login_message"
                            )
                    )
            page.update()


    def send_message_click(e) :
        if new_message.value != "" :
            usuario = page.session.get("user_name")
            # print(usuario)
            msg_usuario = new_message.value
            page.pubsub.send_all(Message(usuario, msg_usuario, message_type="chat_message"))

            new_message.value = ""
            new_message.focus()

            print(msg_usuario)

            prefixo = f'{usuario} diz: '
            msg_usuario = prefixo + msg_usuario

            print(msg_usuario)

            convo.send_message(msg_usuario)
            resposta = convo.last.text

            page.pubsub.send_all(Message('ImparciBot', f'{resposta}', message_type="chat_message"))

            new_message.value = ""
            new_message.focus()
            page.update()


    def on_message(message: Message) :
        if message.message_type == "chat_message" :
            m = ChatMessage(message)
        elif message.message_type == "login_message" :
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()


    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    join_user_name = ft.TextField(
            label="Enter your name to join the chat",
            autofocus=True,
            on_submit=join_chat_click,
            )
    page.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome!"),
            content=ft.Column([join_user_name], width=300, height=70, tight=True),
            actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
            actions_alignment="end",
            )

    # Chat messages
    chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            )

    # A new message entry form
    new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=send_message_click,
            )

    # Add everything to the page
    page.add(
            ft.Container(
                    content=chat,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True,
                    ),
            ft.Row(
                    [
                        new_message,
                        ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_message_click,
                                ),
                        ]
                    ),
            )


ft.app(port=8550, target=main, view=ft.WEB_BROWSER)