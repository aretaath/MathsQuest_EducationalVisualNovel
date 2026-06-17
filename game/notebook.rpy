image icon_notebook = "images/notebook/icon_notebook.png"
image icon_notebook_hover = "images/notebook/icon_notebook_hover.png"
image notebook_bg = "images/notebook/notebook.png"

default unlocked_notes = []
define note_spacing = 60
define page_height = 605
define left_page_x = 225
define right_page_x = 750
define page_y = 140
default notebook_notification = ""
default notebook_notification_show = False

define note_data = {

    "faces_edges": {
        "image" : "note_faces_edges",
        "width" : 470,
        "height": 245
    },

    "footprint": {
        "image" : "note_footprint",
        "width" : 470,
        "height": 270
    },

    "handprint": {
        "image" : "note_handprint",
        "width" : 470,
        "height": 270
    },

    "painting": {
        "image" : "note_painting",
        "width" : 470,
        "height": 175
    },

    "southwest": {
        "image" : "note_southwest",
        "width" : 470,
        "height": 40
    }
}

init python:

    def unlock_note(note_id):
        if note_id not in store.unlocked_notes:
            store.unlocked_notes.append(note_id)
            show_notebook_notification(_("New Note Added"))

    def show_notebook_notification(message):
        store.notebook_notification = message
        store.notebook_notification_show = True
        renpy.sound.play("notification.mp3", channel="sound", loop=False)
        renpy.restart_interaction()

## Icon
screen notebook_icon():
    zorder 200

    if notebook_notification_show:

        frame:
            background "#2c1a0eee"
            xpos 225
            ypos 280
            xpadding 15
            ypadding 8

            text notebook_notification:
                color "#f5e6c8"
                size 32

        timer 3.0 action [
            SetVariable("notebook_notification_show", False),
            SetVariable("notebook_notification", "")
        ] repeat False

    imagebutton:
        idle "icon_notebook"
        hover "icon_notebook_hover"
        xalign 0.021
        yalign 0.25
        xsize 161
        ysize 188

        action If(
            inventory_mode == "use",
            NullAction(),
            If(
                renpy.get_screen("notebook_panel"),
                Hide("notebook_panel"),
                [
                    Hide("inventory_panel"),
                    Show("notebook_panel"),
                    IncrementVariable("notebook_open_count", 1),
                    Function(update_js_logs)
                ]
            )
        )

# Panel notebook
screen notebook_panel():
    zorder 100
    modal True

    add "#00000093"

    key "dismiss" action Hide("notebook_panel")
    key "K_ESCAPE" action Hide("notebook_panel")

    frame:
        background Frame("images/notebook/notebook.png", 30, 30)
        xalign 0.5
        yalign 0.5
        xsize 1450
        ysize 950

        button:
            background None
            xfill True
            yfill True
            action NullAction()

        fixed:

            $ left_y = page_y
            $ right_y = page_y

            for note_id in unlocked_notes:

                $ note = note_data[note_id]
                $ note_image = note["image"]
                $ note_width = note["width"]
                $ note_height = note["height"]

                if left_y + note_height <= page_y + page_height:
                    add Transform(
                        note_image,
                        xsize=note_width,
                        ysize=note_height
                    ):
                        xpos left_page_x
                        ypos left_y

                    $ left_y += note_height + note_spacing

                elif right_y + note_height <= page_y + page_height:
                    add Transform(
                        note_image,
                        xsize=note_width,
                        ysize=note_height
                    ):
                        xpos right_page_x
                        ypos right_y

                    $ right_y += note_height + note_spacing