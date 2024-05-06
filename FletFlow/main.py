import time
import flet as ft
from flet import *
import os

def main(page: ft.Page):
    audio_src = "C:/Users/User/Downloads/ODESZA - Behind The Sun - Official Video.mp3"
    a_filter=g_filter="none"
    page.window_width = 400
    page.window_height = 800
    page.padding=0
    #data base simulation
    genres_color = ["purple", "blue", "red", "yellow", "black"]
    genres = ["HipHop", "Classic", "Rock", "Country", "Techno"]
    authors = []
    database = [
        ("Luis Fonsi", "https://international-artists.com/wp-content/uploads/2023/04/Luis-Fonsi.png", "HipHop", "Despacito", "Luis Fonsi - Despacito ft. Daddy Yankee.mp3"),
        ("Ed Sheeran", "https://hips.hearstapps.com/hmg-prod/images/ed-sheeran-GettyImages-494227430_1600.jpg", "Classic", "Shape of you", "Ed Sheeran - Shape of You (Official Music Video).mp3"),
        ("Mark Ronson", "https://upload.wikimedia.org/wikipedia/commons/c/ce/Mark_Ronson_and_Jennifer_Su%2C_2011_%28cropped%29.jpg", "Rock", "Uptown Funk", "Mark Ronson - Uptown Funk (Official Video) ft. Bruno Mars.mp3"),
        ("PSY", "https://d.newsweek.com/en/full/399470/11-30-15-psy.jpg", "Country", "Gangnam Style", "PSY - GANGNAM STYLE(강남스타일) MV.mp3"),
        ("El Chombo", "https://peru21.pe/resizer/nsEC3AsCDJtvOcRsNCrORxJR-wY=/1200x900/smart/filters:format(jpeg):quality(75)/arc-anglerfish-arc2-prod-elcomercio.s3.amazonaws.com/public/TJWWIY4SPZCYDOBQPUL5TXYIT4.jpg", "Country", "Dame Tu Cosita", "El Chombo - Dame Tu Cosita feat. Cutty Ranks (Official Video) [Ultra Records].mp3"),
        ("Mark Ronson",
         "https://upload.wikimedia.org/wikipedia/commons/c/ce/Mark_Ronson_and_Jennifer_Su%2C_2011_%28cropped%29.jpg",
         "Techno", "Late Night Feelings", "Mark Ronson - Late Night Feelings (Official Video) ft. Lykke Li.mp3"),
        ("Luis Fonsi", "https://international-artists.com/wp-content/uploads/2023/04/Luis-Fonsi.png", "Classic",
         "Roma", "Luis Fonsi, Laura Pausini - Roma (Official Video).mp3"),]


    def slider_changed(e):
        duration_slider.value= int(e.data) / music.get_duration() * 100
        duration_slider.update()
        progress_button.text=f"{round(music.get_current_position() / 60000)}:{int(music.get_current_position() / 1000) % 60:02}/{round(music.get_duration() / 1000 / 60)}:{int(music.get_duration() / 1000) % 60:02}"
        progress_button.update()
    def set_time(e):
        value= e.control.value / 100 * music.get_duration()
    def nothing(e):
        pass
    def open_profile(e):
        pass
    music = Audio(
        src=audio_src,
        autoplay=False,
        volume=1,
        balance=0,
        on_position_changed=nothing
    )
    page.overlay.append(music)
    def filter_expand(index, items):
        if top_bar.controls[1].controls[index].width==150:
            top_bar.controls[1].controls[index].width = 60
            top_bar.controls[1].controls[index].height = 25
            top_bar.controls[1].controls[index].content.controls[1].controls.clear()
        else:
            top_bar.controls[1].controls[index].width = 150
            top_bar.controls[1].controls[index].height = 100
            for item in items:
                top_bar.controls[1].controls[index].content.controls[1].controls.append(
                    (Container(gradient=LinearGradient(
                        begin=alignment.bottom_left,
                        end=alignment.top_right,
                        colors=["grey700", "black"]
                    ),border_radius=25, on_click=lambda _, ite=item:set_filter(ite, index),content=Row(controls=[Text(item)]))))
        top_bar.controls[1].controls[index].update()
    def set_filter(item, index):
        nonlocal a_filter,g_filter
        if index==1:
            a_filter=item
            top_bar.controls[1].controls[index].width = 60
            top_bar.controls[1].controls[index].height = 25
            top_bar.controls[1].controls[3]=(FilledTonalButton(text=item,on_click=lambda _: remove_filter(a_filter,3)))
            top_bar.controls[1].update()
        if index==2:
            g_filter=item
            top_bar.controls[1].controls[index].width = 60
            top_bar.controls[1].controls[index].height = 25
            top_bar.controls[1].controls[4]=(FilledTonalButton(text=item,on_click=lambda _:remove_filter(a_filter,4)))
            top_bar.controls[1].update()
    def remove_filter(filter,index):
        nonlocal a_filter,g_filter
        if index==3:
            a_filter="none"
        if index==4:
            g_filter="none"
        top_bar.controls[1].controls[index] =Text("")
        _search.update()
    def results(i):
        return Container(
            height=50,
            width=400,
            on_click=lambda e,index=i:change_page(e,index),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["grey", "orange", "brown900"]
            ),
            border_radius=25,
            padding=padding.only(
                left=20,
            ),
            content=Row(
                controls=[
                    Stack(
                        controls=[
                            Image(
                                src=database[i][1],
                                width=50,
                                height=50,
                                fit=ft.ImageFit.COVER,
                                border_radius=10

                            ),
                            FilledTonalButton(
                                text=" ",
                                opacity=0,
                                on_click=lambda e, index=i: open_author(e,index),
                                height=50
                            ),

                        ]
                    ),
                    Column(
                        controls=[
                            ft.Text(
                                database[i][3],
                                italic=True,
                                color="white",
                            ),

                            Container(
                                width=200,
                                height=5,
                                bgcolor='white12',
                                border_radius=20,
                                content=Container(
                                    bgcolor="white10",
                                ),
                            ),
                        ]
                    ),
                    play_immed[i]
                ]
            ))
    def search(song, author, genre):
        nonlocal a_filter,g_filter
        for i in range(len(database)):
            if song in database[i][3].lower() and (author == database[i][0] or author == "none") and (genre == database[i][2] or genre == "none"):
                _search.content.controls.append(results(i))



    #on_click methods
    def search_page(e):
        _search.content.controls.clear()
        _search.content.controls.append(top_bar)
        page.clean()
        search(srch.value, a_filter, g_filter)
        page.add(_search)
        page.update()

    def change_page(e,i):
        music.release()
        play_immed[i].text="▶"
        page.clean()
        if i==-1:
            _author.content.controls[0].controls.clear()
            _author.content.controls[1].controls.clear()
            music.on_position_changed = nothing
            page.add(_c)
            page.update()
        else:
            music.on_position_changed = slider_changed
            music.src= "songs/" + database[i][4]
            music.update()
            page.add(_player)
            page.update()
            _player.content.controls[1].controls[0].controls[0].controls[0].text= os.path.basename(music.src)[:48] + "..."
            _player.content.controls[1].controls[0].controls[0].controls[0].update()
            _player.content.controls[1].controls[0].controls[2].controls[0].src=database[i][1]
            _player.content.controls[1].controls[0].controls[2].controls[0].update()
            music.play()

        time.sleep(0.4)
    def main_page(e):
        page.clean()
        page.add(_c)
        page.update()
    def open_author(e,index):
        nonlocal play_immed
        page.clean()
        _author.content.controls[0].controls.append(Row(controls=[Column(controls=[FilledTonalButton(text="<",on_click=lambda e:change_page(e,-1)), Image(src=database[index][1], width=150, height=150, border_radius=10, fit=ft.ImageFit.COVER)]), Text(database[index][0], size=35, italic=True)]))
        for i in range(len(database)):
            if database[index][0]==database[i][0]:
                _author.content.controls[1].controls.append(
                    Container(
                        on_click=lambda e, index=i:change_page(e,index),
                        gradient=LinearGradient(
                        begin=alignment.bottom_center,
                        end=alignment.top_center,
                        colors=["green", "grey700"]
                        ),
                        height=50,
                        border_radius=15,
                        content=Row(controls=[play_immed[i], Text(database[i][3])])))
        page.add(_author)
        page.update()

    def play_player(e):
        music.play()
        if pr_button.text=="▶️":
            pr_button.text="❚❚"
            pr_button.update()
    def play_song(e, index, song):
        nonlocal music, play_immed
        if music.src != "C:/Users/User/Downloads/" + database[index][4]:
            music.src = "C:/Users/User/Downloads/" + database[index][4]
            music.update()
            time.sleep(0.1)
            music.play()
            for i in range(len(play_immed)):
                play_immed[i].text = "▶️"
                play_immed[i].update()
            play_immed[index].text = "❚❚"
            play_immed[index].update()
        elif play_immed[index].text == "❚❚":
            music.pause()
            play_immed[index].text = "▶️"
            play_immed[index].update()
        else:
            music.resume()
            play_immed[index].text = "❚❚"
            play_immed[index].update()

    def pause(_):
        if pr_button.text=="❚❚":
            music.pause()
            pr_button.text="▶️"
            pr_button.update()
        else:
            music.resume()
            pr_button.text="❚❚"
            pr_button.update()
    def volume_change(e):
        value=e.control.value/100
        if value > 0 and value<1:
            volume.label = str(round(value*100))+"%"
            sound.text=str(round(value*100))+"%"
        elif value==0:
            volume.label = "🔇"
            sound.text="🔇"
        elif value==1:
            volume.label = "🔊"
            sound.text="🔊"
        sound.update()
        volume.opacity = 1
        volume.update()
        music.volume = value
        music.update()

    def show_volume(e):
        if e.data=="true":
            volume.opacity=1
            volume.update()
        else:
            volume.opacity=0
            volume.update()

    def mute(e):
        global start_volume
        if music.volume>0:
            start_volume=music.volume
            volume.value = 0
            volume.label = "🔇"
            volume.update()
            music.volume = 0
            music.update()
            sound.text = "🔇"
            sound.update()
        else:
            music.volume=start_volume
            music.update()
            volume.value=start_volume*100
            volume.update()
            sound.text=str(round(volume.value))+"%"
            sound.update()

    def expand(e, index):
        nonlocal genres_card
        if genres_card.controls[index].height < 450:
            genres_card.controls[index].height = 450
            genres_card.controls[index].width = 250
            genres_card.controls[index].content.controls[0].controls[2].width = 225
            genres_card.controls[index].content.controls[0].controls[0].spacing = 150

            leng = len(database)
            for i in range(leng):
                if genres[index]==database[i][2]:
                    song_result = database[i][3][:15] + "..."
                    genres_card.controls[index].content.controls[0].controls.append(
                        Container(
                            height=50,
                            width=220,
                            border_radius=10,
                            on_click=lambda e, index=i, song=database[i][3]: play_song(e, index, song),
                            gradient=LinearGradient(
                                begin=alignment.bottom_center,
                                end=alignment.top_center,
                                colors=[genres_color[index], "white"]
                            ),
                            animate_opacity=300,

                            padding=padding.only(
                                left=20,
                            ),
                            content=Row(
                                controls=[
                                    Stack(
                                        controls=[
                                            Image(
                                                src=database[i][1],
                                                width=50,
                                                height=50,
                                                border_radius=10,
                                                fit=ft.ImageFit.COVER,

                                            ),
                                            FilledTonalButton(
                                                text=" ",
                                                on_click=lambda e, index=i: open_author(e,index),
                                                opacity=0
                                            )
                                        ]
                                    ),
                                    Column(
                                        controls=[
                                            ft.Text(
                                                song_result,
                                                color="white",
                                            ),

                                        ]
                                    ),
                                ]
                            )),
                    )
            genres_card.update()
        else:
            genres_card.controls[index].height = 110
            genres_card.controls[index].width = 170
            genres_card.controls[index].content.controls[0].controls[2].width = 140
            del genres_card.controls[index].content.controls[0].controls[4:4 + len(database[3])]
            genres_card.controls[index].content.controls[0].controls[0].spacing = 70
            genres_card.update()

    duration_slider=ft.Slider(min=0, max=100, value=0, divisions=100, on_change=set_time, width=350)
    play_player=ft.FilledTonalButton("Play", on_click=play_player)
    pr_button = ft.FilledTonalButton("❚❚", on_click=pause)
    progress_button = ft.CupertinoButton(text="0/0", color=ft.colors.GREY)
    volume = ft.Slider(min=0, max=100, value=100, divisions=10, on_change=volume_change, width=105, opacity=0,
                       label="🔊", animate_opacity=1000)
    sound = ft.ElevatedButton(text="🔊", on_click=mute)

    #buttons for direct play
    play_immed = []

    #popular
    hits = Column(height=200, scroll='auto')
    hot_songs = []
    for i in range(len(database)):
        play = FilledTonalButton(text="▶", on_click=lambda e, index=i, song=database[i][3]: play_song(e, index, song))
        play_immed.append(play)
        hit = results(i)
        hot_songs.append(hit)
        hits.controls.append(hot_songs[i])

    authors_card=Row(height=220,controls=[Row()],scroll='auto')
    channels=[]
    current_row = Column()
    authors_card.controls.append(current_row)

    for i in range(len(database)):
        author = database[i][0]
        if author not in authors:
            a = Container(
                border_radius=border_radius.only(bottom_left=20, bottom_right=20, top_right=20),
                width=105,
                height=105,
                padding=15,
                gradient=LinearGradient(
                    begin=alignment.bottom_left,
                    end=alignment.top_right,
                    colors=["grey800", "black"]
                ),
                scale=ft.transform.Scale(scale=1),
                animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
                content=Column(
                    controls=[
                        Row(
                            controls=[
                                Stack(
                                    controls=[
                                        Image(
                                            src=database[i][1],
                                            fit=ft.ImageFit.COVER,
                                            border_radius=10,
                                            width=40,
                                            height=40
                                        ),
                                        FilledTonalButton(
                                            on_click=lambda e, index=i: open_author(e, index),
                                            opacity=0
                                        )
                                    ]
                                ),
                                Text("△")
                            ]
                        ),
                        Text(author, size=14)
                    ]
                )
            )
            channels.append(a)
            current_row.controls.append(channels[len(channels) - 1])
            authors.append(author)

            if len(current_row.controls) == 2:
                current_row = Column()
                authors_card.controls.append(current_row)

    #genres
    genres_card = Row(scroll="auto")
    cards = []
    for i, category in enumerate(genres):
        c = Container(
            border_radius=border_radius.only(top_left=20,bottom_right=20),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["white", genres_color[i], "brown900"]
            ),
            width=170,
            height=110,
            padding=15,
            animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
            on_click=lambda e, index=i: expand(e, index),
            content=Row(
                controls=[
                    Column(
                        controls=[
                            Row(
                                spacing=70,
                                controls=[
                                    Text('Genre'), IconButton(icon=ft.icons.SEARCH)
                                ]
                            ),
                            Text(category),
                            Container(
                                width=140,
                                height=5,
                                bgcolor='white12',
                                border_radius=20,
                                animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
                                content=Container(
                                    bgcolor="white10",
                                ),
                            ),
                            Container(
                                height=20
                            )
                        ]
                    )
                ]
            ),
        )
        cards.append(c)
        genres_card.controls.append(cards[i])

    #main screen
    f_authors=Container(
        bgcolor="yellow",
        width=60,
        height=25,
        border_radius=25,
        on_click=lambda _:filter_expand(1,authors),
        content=(
            Row(
                controls=[
                    Text("authors",color="black"),
                    Column(
                        scroll='auto',
                        controls=[]
                    )]
            )
        )
    )
    f_genres=Container(
        bgcolor="yellow",
        width=60,
        height=25,
        border_radius=25,
        on_click=lambda _:filter_expand(2,genres),
        content=(
            Row(
                controls=[
                    Text("genres",color="black"),
                    Column(
                        scroll='auto',
                        controls=[]
                    )]
            )
        )
    )
    srch=TextField(label="search song", width=250, height=25, border_radius=25, border_color="yellow", on_submit=search_page)
    main_bar=Column(controls=[
        Row(controls=[IconButton(
            icon=ft.icons.ACCESSIBILITY, icon_color="yellow", on_click=open_profile
        ), srch,
            IconButton(
                icon=ft.icons.SEARCH,
                icon_color="yellow",
                on_click=search_page

            )]),
    ])
    top_bar=Column(controls=[
        Row(controls=[IconButton(
            icon=ft.icons.ACCESSIBILITY, icon_color="yellow", on_click=open_profile
        ), srch,
            IconButton(
                icon=ft.icons.SEARCH,
                icon_color="yellow",
                on_click=search_page

            )]),
        Row(controls=[FilledTonalButton(text="<", on_click=lambda e: change_page(e, -1)),f_authors,f_genres,Text(""),Text("")])
    ])
    _c = Container(
        width=400,
        height=750,

        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[ft.colors.BLACK12, ft.colors.GREY_900, ft.colors.DEEP_ORANGE_700]
        ),
        border_radius=35,
        bgcolor='black',
        padding=10,

        content=Column(
            spacing=20,
            scroll='auto',
            controls=[
                Row(alignment='spaceBetween',
                    controls=[
                    ]),main_bar,

                Container(content=authors_card),

                Container(padding=padding.only(top=10, bottom=20),
                          content=genres_card),

                Stack(
                    controls=[
                        hits,
                    ]
                )
            ]
        ))
    _player=Container(
        width=400,
        height=700,
        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=["black", "lightblue900"]
        ),
        border_radius=35,
        bgcolor='black',
        padding=10,
        content=Stack(
            width=350,
            height=550,
            controls=[
                Container(padding=padding.only(bottom=50)),
                Row(
                    alignment="center",
                    spacing=300,
                    controls=[
                        Column(
                            controls=[
                                Row(
                                    alignment="center",
                                    controls=[
                                        ft.ElevatedButton(
                                            text=os.path.basename(music.src),
                                        )
                                    ]
                                ),
                                Divider(height=20, thickness=20,color="white10"),
                                Row(
                                    controls=[
                                        ft.Image(
                                            src=f"https://static2.radiobonton.pl/data/articles/xga-1x1-luis-fonsi-stefflon-don-calypso-1653406576.webp",
                                            width=350,
                                            height=350,
                                            fit=ft.ImageFit.COVER,
                                            border_radius=ft.border_radius.all(100)
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    spacing=57,
                                    controls=[
                                        Column(
                                            controls=[
                                                play_player,
                                            ],
                                        ),
                                        Column(
                                            spacing=2,
                                            controls=[
                                                progress_button,
                                            ]
                                        ),
                                        Column(
                                            spacing=2,
                                            controls=[
                                                pr_button
                                            ]
                                        )

                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        duration_slider,
                                    ]
                                ),
                                ft.Row(

                                    spacing=2,
                                    controls=[
                                        #back_rewind,
                                        Container(
                                            content=Row(
                                                controls=[
                                                    FilledTonalButton(
                                                        text="back",
                                                        on_click=lambda e: change_page(e, -1)
                                                    ),
                                                    sound,
                                                    volume,


                                                ]
                                            ),
                                            on_hover=show_volume
                                        ),

                                        ft.CupertinoButton(text=" "),
                                        #forw_rewind,
                                    ]
                                )


                            ]
                        )
                    ]
                ),

            ]
        )
    )
    _author=Container(
        width=400,
        height=700,
        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=["black", "grey700"]
        ),
        border_radius=35,
        content=Column(
            controls=[
                Row(
                    controls=[],
                ),
                Column(scroll='auto',
                       controls=[])
            ]
        )
    )
    _search= Container(
        width=400,
        height=750,

        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[ft.colors.BLACK12, ft.colors.GREY_900, ft.colors.DEEP_ORANGE_700]
        ),
        border_radius=35,
        bgcolor='black',
        padding=10,
        content=Column(
            scroll='auto',
            controls=[]))
    page.add(
        _c,

    )
    page.update()


ft.app(target=main)
