image icon_inventory = "images/inventory/icon_inventory.png"
image icon_inventory_hover = "images/inventory/icon_inventory_hover.png"
image inventory_bg = "images/inventory/inventory.png"
image slot_blank = "images/inventory/empty_box.png"
image slot_locked = "images/inventory/locked_box.png"
image slot_hover = "images/inventory/hover_box.png"

image item_key = "images/inventory/items/key.png"
image item_pyramid = "images/inventory/items/pyramid.png"
image item_button = "images/inventory/items/button.png"
image item_jewellery = "images/inventory/items/necklace.png"
image item_painting = "images/inventory/items/painting.png"

default inventory_items = [None] * 5
default selected_item   = None
default inventory_mode = "normal"
default needed_item = None
default inventory_notification = ""
default inventory_notification_show = False

define items = {

    "key": {
        "image"      : "item_key",
        "label"      : "Key",
        "description": "An old iron key found hidden in a book",
    },

    "pyramid": {
        "image"      : "item_pyramid",
        "label"      : "Pyramid",
        "description": "A square-based pyramid with a hint",
    },

    "button": {
        "image"      : "item_button",
        "label"      : "Silver Button",
        "description": "A silver button found near the boiler room",
    },

    "jewellery": {
        "image"      : "item_jewellery",
        "label"      : "Jewellery",
        "description": "A necklace found in bread",
    },

    "painting": {
        "image"      : "item_painting",
        "label"      : "Paintings",
        "description": "A paintings found in boiler room",
    },
}

init python:

    def add_item(item_name):
        for i in range(len(store.inventory_items)):
            if store.inventory_items[i] is None:
                store.inventory_items[i] = item_name
                item_label = renpy.translate_string(
                    items[item_name]["label"]
                )
                notification_text = "{}: {}".format(
                    renpy.translate_string("New Item"),
                    item_label
                )
                show_inventory_notification(notification_text)
                return True
        return False

    def has_item(item_name):
        return item_name in store.inventory_items

    def show_inventory_notification(message):
        store.inventory_notification = message
        store.inventory_notification_show = True
        renpy.sound.play("notification.mp3", channel="sound", loop=False)
        renpy.restart_interaction()

## Icon
screen inventory_icon():
    zorder 200

    if inventory_notification_show:

        frame:
            background "#2c1a0eee"

            xpos 225
            ypos 85

            xpadding 15
            ypadding 8

            text inventory_notification:
                color "#f5e6c8"
                size 32

        timer 3.0 action [
            SetVariable("inventory_notification_show", False),
            SetVariable("inventory_notification", "")
        ] repeat False


    imagebutton:
        idle "icon_inventory"
        hover "icon_inventory_hover"

        xalign 0.02
        yalign 0.04
        
        xsize 182
        ysize 142

        action If(
            inventory_mode == "use",
            NullAction(),
            If(
                renpy.get_screen("inventory_panel"),

                [
                    SetVariable("selected_item", None),
                    Hide("inventory_panel")
                ],

                [
                    SetVariable("selected_item", None),
                    Hide("notebook_panel"),
                    Show("inventory_panel"),
                    IncrementVariable("inventory_open_count", 1),
                    Function(update_js_logs)
                ]
            )
        )

# Panel inventory
screen inventory_panel():
    zorder 100
    modal True

    add "#00000093"

    key "dismiss" action If(
        inventory_mode == "use",
        NullAction(),
        [
            SetVariable("selected_item", None),
            Hide("item_detail"),
            Hide("inventory_panel")
        ]
    )

    key "K_ESCAPE" action If(
        inventory_mode == "use",
        NullAction(),
        [
            SetVariable("selected_item", None),
            Hide("item_detail"),
            Hide("inventory_panel")
        ]
    )

    if inventory_mode == "use":
        frame:
            background "#000000aa"
            xalign 0.5
            yalign 0.5
            xpadding 30
            ypadding 20

            text _("Select an item to use"):
                size 32
                color "#f5e6c8"
                xalign 0.5

    frame:
        background Frame("images/inventory/inventory.png", 30, 30)

        xalign 0.5
        yalign 0.95
        xsize 1300
        ysize 320

        xpadding 80
        ypadding 100

        button:
            background None
            xfill True
            yfill True
            action NullAction()

        hbox:
            spacing 40
            xalign 0.5
            yalign 0.1

            for item in inventory_items:

                if item is None:
                    add "slot_blank":
                        xsize 186
                        ysize 186

                else:
                    $ item_data = items[item]

                    fixed:
                        xsize 186
                        ysize 186

                        if selected_item == item:
                            add "slot_hover":
                                xsize 186
                                ysize 186
                        else:
                            add "slot_blank":
                                xsize 186
                                ysize 186

                        imagebutton:
                            idle Transform(item_data["image"], xsize=160, ysize=160)
                            hover Transform(item_data["image"], xsize=160, ysize=160)

                            xalign 0.5
                            yalign 0.5

                            action If(
                                inventory_mode == "use",
                                [
                                    Function(log_item_use, item, needed_item),
                                    If(
                                        item == needed_item,
                                        Return(True),
                                        Return(False)
                                    )
                                ],
                                If(
                                    selected_item == item,
                                    SetVariable("selected_item", None),
                                    SetVariable("selected_item", item)
                                )
                            )
    
    if selected_item and inventory_mode != "use":
        $ item_data = items[selected_item]

        frame:
            background Frame("images/inventory/paper.png")
            xalign 0.5
            yalign 0.5
            xpadding 50
            ypadding 55
            xminimum 700
            yminimum 400

            vbox:
                spacing 10
                xalign 0.5

                add item_data["image"]:
                    xalign 0.5
                    xsize 150
                    ysize 150

                text _(item_data["label"]):
                    color "#0f0f0f"
                    xalign 0.5
                    size 50

                text _(item_data["description"]):
                    color "#0f0f0f"
                    xalign 0.5
                    text_align 0.5
                    size 28