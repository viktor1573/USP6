import flet as ft
from flet import *
import re


def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 800
    page.padding = 0
    page.window_resizable = False
    page.bgcolor = '#fafafa'
    page.horizontal_alignment = 'center'

    def register_page(e):
        page.clean()
        page.add(Register)
        page.update()

    def login_page(e):
        page.clean()
        page.add(Login)
        page.update()

    def validate_register(e):
        pass

    def validate_login(e):
        pass

    def is_valid_email(email):
        pattern = "^[a-zA-Z0-9_. +-]+@[a-zA-Z0-9-]+\. [a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    def is_valid_password(e):
        pass

    user_username_register = ft.TextField(
        label="Username", border_radius=border_radius.only(top_right=50, bottom_right=0),
        bgcolor='#ffffff', prefix_icon=icons.PERSON_ROUNDED,
        border_color='#e8e8e8',
        border_width=1,

    ),

    user_password_register = ft.TextField(
        label="Password", password=True,
        border_radius=border_radius.only(top_right=0, bottom_right=0),
        bgcolor='#ffffff', prefix_icon=icons.LOCK_ROUNDED,
        border_color='#e8e8e8',
        border_width=1,

    ),

    user_email_register = ft.TextField(
        label="Email",
        border_radius=border_radius.only(top_right=0, bottom_right=50),
        bgcolor='#ffffff', prefix_icon=icons.EMAIL_ROUNDED, suffix_text=".com",
        border_color='#e8e8e8',
        border_width=1,

    ),
    user_btn_register = ft.ElevatedButton(
        " ",
        color='white',
        bgcolor='#02c0f2',
        style=ft.ButtonStyle(shape=ft.CircleBorder(), ),
        icon=icons.CHECK_ROUNDED,
        width=60,
        height=60,
        disabled=True,

    ),

    Register = Container(

        Stack([
            Container(

                bgcolor='#159e96',

                border_radius=110,
                width=220,
                margin=margin.only(left=-80, top=-70),
                height=220,

            ),

            Container(

                bgcolor='#159e96',

                border_radius=105,
                width=210,
                margin=margin.only(left=60, top=-120),
                height=210,
            ),
            Container(

                bgcolor='#159e96',

                border_radius=110,
                width=220,
                margin=margin.only(left=130, top=680),

                height=220,
            ),

            Container(

                bgcolor='#159e96',

                border_radius=105,
                width=210,
                left=300, 
                top=600, 
                height=210,
            ),
            Container(
                ElevatedButton(
                    "Login",
                    color='#2b159e',
                    bgcolor='white',
                    on_click=lambda e: login_page(e)
                ), margin=margin.only(top=140),
                alignment=alignment.top_right,
            ),
            Container(

                Column([

                    Container(
                        Row([
                            ft.Text(
                                "Register",
                                color='black',
                                weight='w600',
                                size=36,

                            ),
                        ], ), margin=margin.only(left=120, bottom=25),
                    ),

                    Stack([
                        Row([
                            Column([
                                Row(
                                    user_username_register,
                                ),
                                Row(
                                    user_password_register,
                                ),
                                Row(
                                    user_email_register,
                                ),
                            ], spacing=0, width=270),
                            Column([
                                Stack(
                                    user_btn_register,
                                ),
                            ], ),
                        ], spacing=0),
                    ]),

                ]),
                margin=margin.only(top=200)),
        ]),
    )

    user_username_login = ft.TextField(
        label="Username", border_radius=border_radius.only(top_right=50, bottom_right=0),
        bgcolor='#ffffff', prefix_icon=icons.PERSON_ROUNDED,
        border_color='#e8e8e8',
        border_width=2
    ),

    user_password_login = ft.TextField(
        label="Password", password=True,
        border_radius=border_radius.only(top_right=0, bottom_right=50),
        bgcolor='#ffffff', prefix_icon=icons.LOCK_ROUNDED,
        border_color='#e8e8e8',
        border_width=2,
    ),

    user_btn_login = ft.ElevatedButton(
        " ",
        color='white',
        bgcolor='#02c0f2',
        style=ft.ButtonStyle(shape=ft.CircleBorder()),
        icon=icons.ARROW_RIGHT_ALT,
        disabled=False,
        width=60,
        height=60,
        on_click=validate_login
    ),

    Login = Container(

        Stack([
            Container(

                bgcolor='#2b159e',

                border_radius=110,
                width=220,
                margin=margin.only(left=-80, top=-70),
                height=220,

            ),

            Container(

                bgcolor='#2b159e',

                border_radius=105,
                width=210,
                margin=margin.only(left=60, top=-120),
                height=210,
            ),
            Container(

                bgcolor='#2b159e',

                border_radius=110,
                width=220,
                margin=margin.only(left=130, top=680),

                height=220,
            ),

            Container(

                bgcolor='#2b159e',

                border_radius=105,
                width=210,
                left=300,  # Позиционируем по горизонтали
                top=600,
                height=210,
            ),

            Container(

                Column([

                    Container(
                        Row([
                            ft.Text(
                                "Login",
                                color='black',
                                weight='w600',
                                size=36,

                            ),
                        ], ), margin=margin.only(left=120, bottom=25),
                    ),

                    Stack([
                        Row([
                            Column([
                                Row(
                                    user_username_login,
                                ),
                                Row(
                                    user_password_login,
                                )
                            ], spacing=0, width=270),
                            Column(
                                user_btn_login,
                            ),
                        ], spacing=0),
                    ]),
                    Container(
                        Text(
                            "Forgot password?",
                            weight='w600',
                            color='#e8e8e8'
                        ), margin=margin.only(left=150)
                    ),
                    Container(
                        ElevatedButton(
                            "Register",
                            color='red',
                            bgcolor='#ffffff',
                            on_click=lambda e: register_page(e)
                        ), margin=margin.only(top=75),
                    ),

                ]),
                margin=margin.only(top=200)),
        ]),
    )

    page.add(
        Login
    )

    page.update()


ft.app(target=main)
