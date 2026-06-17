define y = DynamicCharacter("player_name")
define c = Character(_("The Standing Man"))
define w = Character(_("The Woman"))
define t = Character(_("The Sitting Man"))
define o = Character(_("The Owner"))

define fade_slow = Dissolve(0.3)
define fade_fast = Dissolve(0.2)
define flash = Fade(0.05, 0.1, 0.3, color="#fff")
define shake = hpunch

default player_name = ""
default player_age = ""
default player_gender = ""

default finished_library = False
default finished_cellar = False
default finished_kitchen = False

default choice_spacing = 350

default current_bgm = ""

init python:

    def lang_condition(path):
        return ConditionSwitch(
            "_preferences.language == 'id_zenpy'",
            "images/id/" + path,
            "True",
            "images/en/" + path
        )

    normal_bgm = {
        "intro_mansion", #001
        "mysterious_helper", #002
        "main_hall", #003
        "puzzle_1", #004
        "puzzle_2", #006
        "puzzle_3", #007
        "puzzle_4", #009
        "puzzle_5", #012
        "puzzle_6", #014
        "puzzle_7", #015
        "puzzle_8", #018
        "puzzle_9", #019
        "puzzle_10", #022
        "compass_direction_hint", #024
        "puzzle_11", #025
        "puzzle_12", #027
        "puzzle_13", #028
        "puzzle_14", #031
        "puzzle_15", #032
        "puzzle_16", #035
        "puzzle_17", #036
        "silver_button_hint", #038
        "puzzle_18", #039
        "puzzle_19", #040
        "puzzle_20", #042
        "puzzle_21", #045
        "bite_footprint_hint", #047
        "scribbled_note", #048
        "puzzle_22", #049
        "puzzle_23", #051
        "puzzle_24", #052
        "puzzle_25", #054
        "puzzle_26", #057
        "puzzle_27", #059
        "puzzle_28", #060
        "criminals_catched", #063
    }

    wrong_bgm = {
        "blast_of_flame", #005
        "snake_strike", #008
        "crashed_bookcase", #010
        "giant_centipede", #011
        "strange_fumes", #013
        "dark_pit",  #016
        "exploded_pyramid", #017
        "alive_mummy", #020
        "slippery_passage", #021
        "waste_of_time", #023
        "rat_bites", #026
        "green_eyes_creature", #029
        "minotaur",  #030
        "heated_room", #033
        "freezer_room", #034
        "loud_bark_noise", #037
        "scale_trap", #041
        "poisonous_spider", #043
        "strong_pepper", #044
        "ivy_trap", #046
        "wrong_time", #050
        "loud_alarm_sound", #053
        "scalding_water", #055
        "topple_into_empty_space", #056
        "flames_spurt", #058
        "empty_room_with_fire", #061
        "wrong_man", #062
    }

    def bgm_callback(label, abnormal):
        if renpy.game.context().init_phase: return
        if label.startswith("_"): return

        if label in normal_bgm: 
            music_file = "bgm.mp3"
        elif label in wrong_bgm: 
            music_file = "bgm_wrong.mp3"
        else:
            return

        if store.current_bgm == music_file: return

        store.current_bgm = music_file

        renpy.music.play(
            music_file,
            channel = "music",
            loop=True,
            fadeout = 0.5,
            fadein = 0.5
        )

    config.label_callback = bgm_callback



label splashscreen:
    scene splashscreen
    show title at truecenter
    with dissolve
    with Pause(2)
    hide title with dissolve
    return

label start:

    label input_name:
        show screen input_name
        $ player_name = renpy.input("", length=15)
        hide screen input_name
        $ player_name = player_name.strip()
        if player_name == "":
            jump input_name
    
    label input_age:
        show screen input_age
        $ player_age = renpy.input("", length=2, allow="0123456789")
        hide screen input_age
        $ player_age = player_age.strip()
        if player_age == "":
            jump input_age

    call screen input_gender
    show screen options_button
    show screen inventory_icon
    show screen notebook_icon
    $ start_session()

##### A #####

    #001
    label intro_mansion:
        scene exterior_mansion #BG-1
        with fade_slow

        play sound "ringing.mp3" volume 1 #SFX-1 
        "On a cold winter night, a 999 emergency call reports a crime at the Mansion of Mazes."
        "Jewellery and paintings have vanished."
        "Footprints mark the hall…"
        "Yet there are no signs of anyone entering or leaving."

        "The police are baffled. And now, they have asked you to solve the mystery."
        
    $ menu_question = _("Are your detective skills up to the challenge?")
    menu:
        "Yes, I am ready for the challenge (thumbs_up)":
            scene interior_mansion #BG-2
            with fade_slow

            "You are in the Grand Hall."
            
            show letter_hall at truecenter #SP-3
            with fade_fast
            "There is a small table in front of you. On it is a letter addressed to you!"
            hide letter_hall #SP-3
            with fade_fast

            show paintings_siluet at truecenter #SP-4
            with fade_fast
            "You look around and see shapes on the walls where priceless paintings once hung now they have been stolen."
            "You make a note of the shapes in your notebook. They might be important!"
            $ unlock_note("painting")
            hide paintings_siluet #SP-4
            with fade_fast

            jump main_hall #003

        "I am still not sure (thumbs_down)":
            jump mysterious_helper #002

    #002
    label mysterious_helper: 
        scene exterior_mansion #BG-1

        show barkimedes_siluet at truecenter #SP-5
        with fade_fast
        "Don't be afraid. Help is always nearby. Just follow the instructions one at a time, and see how far you get."
        hide barkimedes_siluet #SP-5
        with fade_fast
        
        "Now make your way to the Grand Hall to begin your adventure. Good luck!"

        scene interior_mansion #BG-2
        with fade_slow

        "You are in the Grand Hall."
        
        show letter_hall at truecenter #SP-3
        with fade_fast
        "There is a small table in front of you. On it is a letter addressed to you!"
        hide letter_hall #SP-3
        with fade_fast

        show paintings_siluet at truecenter #SP-4
        with fade_fast
        "You look around and see shapes on the walls where priceless paintings once hung now they have been stolen."
        "You make a note of the shapes in your notebook. They might be important!"
        $ unlock_note("painting")
        hide paintings_siluet #SP-4
        with fade_fast

        jump main_hall #003

    #003
    label main_hall:
        scene interior_mansion #BG-2
        with dissolve
        "You see suspicious footprints on the floor. They lead off in four directions."
        
        play sound "woodenfloor_creak.mp3" volume 1 #SFX-2 
        "Then you hear a floorboard creak."
        "The sound came from the top of the stairs!"

    $ choice_spacing = 0
    $ menu_question = _("Where should you investigate first?")
    menu:
        "Library (ch_library)":
            scene library #BG-3
            with fade_slow

            play sound "door_creak.mp3" volume 1 #SFX-3 
            "You step through the library doors."

            play sound "wind_blows.mp3" volume 1 #SFX-4 
            "Suddenly it feels cold. The wind whistles down the chimney. You start to feel scared."
            
            play sound "dog_woof.mp3" volume 1 #SFX-5 
            "But then you hear a friendly woof. You feel better again."

            play sound "locked.mp3" volume 1 #SFX-6 
            "You check the windows. They are locked. The burglars could not enter or leave that way."

            "Then you spot the safe. It's open! The jewels it held have been stolen with the paintings!"

            show note_safe at truecenter #SP-7
            with fade_fast
            "A note left inside the safe tells you what to do…"
            hide note_safe #SP-7
            with fade_fast

            $ choice_spacing = 350
            jump puzzle_1 #004

        "Cellar (ch_cellar)":
            scene cellar #BG-4
            with fade_slow

            play sound "door_creak.mp3" volume 1 #SFX-3 
            "You open the door labelled 'Cellars'. You see the footprints going down the stairs. The burglars have been down there!"

            play sound "flickering.mp3" volume 1 #SFX-7
            "The way ahead is dimly lit by flickering light bulbs hanging on fraying wires."
            
            show note_cellar at truecenter #SP-8
            with fade_fast
            "On the first step you find a ball of string resting on a note. You pick up the string and read the note…"
            hide note_cellar #SP-8
            with fade_fast

            show minotaursiluet at truecenter #SP-9
            with fade_fast
            "You've heard of the Minotaur. It was a mythical beast. It had a man's body and a bull's head! But there can't be one down here, can there?"
            hide minotaursiluet #SP-9
            with fade_fast

            "You tie one end of the string to the doorknob, and set off down the stairs. You unwind the string as you go."
            
            play sound "dog_step.mp3" volume 1 #SFX-9
            "Soft footsteps follow close behind but somehow you know they are friendly."
            
            $ choice_spacing = 350
            jump puzzle_11 #025

        "Kitchen (ch_kitchen)":
            scene kitchen #BG-5
            with fade_slow

            play sound "door_creak.mp3" volume 1 #SFX-3
            "The footprints lead you down a flight of steps to a large door labelled 'Kitchens'. The smell of fresh bread wafts through the door."
            
            play sound "dog_licking.mp3" volume 1 #SFX-10
            "Then you hear something it sounds like an animal licking its lips!"

            "The kitchens are huge. There is a great open fireplace. There are banks of ovens, huge wooden tables and racks of pots and pans."

            show note_kitchen at truecenter #SP-9
            with fade_fast
            "Just inside the door is a notice board with meal times and menus. Someone has pinned up a letter addressed to you!"
            hide note_kitchen #SP-9
            with fade_fast

            $ choice_spacing = 350
            jump puzzle_18 #039

        "Main Staircase (ch_mainstaircase)":
            $ choice_spacing = 350
            jump scribbled_note #048

##### B #####

    #004
    label puzzle_1:
        scene library #BG-3
        with fade_slow

        "You look around for clues. Then you see patterns carved around the fireplace."
        # show fireplace_pattern at truecenter #SP-10
        "They are not as dusty as the rest of the room. Someone has been touching them! You step closer. The patterns are triangles!"
        # hide fireplace_pattern

    $ menu_question = _("Which one is an equilateral triangle?")
    $ start_puzzle_timer()
    menu:
        "Triangle A (p1_triangleA)":
            $ log_answer("puzzle_1", "2d_shapes", False)
            jump blast_of_flame #005

        "Triangle B (p1_triangleB)":
            $ log_answer("puzzle_1", "2d_shapes", True)

            play sound "stone.mp3" volume 1 #SFX-13
            "You see fingerprints on triangle B, so you press it."

            scene black
            with fade_slow

            show secret_door at truecenter #SP-76
            with fade_fast
            play sound "stone_move.mp3" volume 1 #SFX-23 
            "The bookcase to the right of the fireplace swings open. It's a secret door. There is a hiding place behind the wall. You made the right choice!"
            
            hide secret_door #SP-76
            with fade_fast

            jump puzzle_2 #006
    
    #005
    label blast_of_flame:
        scene blackscreen #BG-27
        with shake
        show blast_of_flame at truecenter #SP-11
        play sound "flame_blast.mp3" volume 1 #SFX-12
        "You press triangle A. A blast of flame roars from the fireplace! Strong teeth grab your belt and pull you to safety. Who was that?"
        hide blast_of_flame #SP-11

        show equilateral_triangle at truecenter #SP-12
        "It was the wrong triangle. An equilateral triangle has three equal sides and three equal angles."
        "Triangle A has only two equal sides and angles. The third side and angle are different from the others. It is an isosceles triangle."
        hide equilateral_triangle #SP-12

        jump puzzle_1 #004

    #006
    label puzzle_2:
        scene hiding_place #BG-6
        with fade_slow

        "You step through the doorway into the hiding place. It's a tiny room with walls made from stone blocks." 
        
        show note_hiding_place at truecenter #SP-13
        with fade_fast
        "There is a stool in the centre. On the stool is a note..."
        hide note_hiding_place #SP-13
        with fade_fast

        "You sit on the stool and look around."
        "Someone has scratched lines on the walls perhaps centuries ago when they were hiding from highwaymen! The lines make shapes around the stones."

    $ menu_question = _("Which stone is hexagonal and holds a clue in its center?")
    $ start_puzzle_timer()
    menu:
        "Stone A (p2_stoneA)":
            $ log_answer("puzzle_2", "2d_shapes", True)

            "The stone at the centre of the shape is loose. You pull it out with your fingertips. Someone has hidden a slip of paper in the space behind. There is something written"
            show note_stone at truecenter #SP-15
            with fade_fast
            "It's the title of a book! But what does E,5 mean?"
            hide note_stone #SP-15
            with fade_fast

            jump puzzle_3 #007

        "Stone B (p2_stoneB)":
            $ log_answer("puzzle_2", "2d_shapes", False)
            jump snake_strike #008

    #007
    label puzzle_3:
        scene library #BG-3
        with fade_slow

        "You step back into the library. Now you must find the book. There are thousands of them!"
        "They are so old and dusty you can't read the titles on their spines. Finding Through the Looking Glass is going to take forever!"

        show marked_bookcase at truecenter #SP-16
        with fade_fast
        "Then you see that the bookcases and shelves are marked with letters and numbers. Some are so worn you cannot read them, but you can work out where E.5 is!"
        hide marked_bookcase
        with fade_fast

    $ menu_question = _("Which shelf is E,5?")
    $ start_puzzle_timer()
    menu:
        "Shelf X (p3_shelfX)":
            $ log_answer("puzzle_3", "coordinates", True)

            "You start to take down the books from shelf X. The fourth one you open is Through the Looking Glass you chose the correct shelf!"
            jump puzzle_4 #009

        "Shelf Y (p3_shelfY)":
            $ log_answer("puzzle_3", "coordinates", False)
            jump crashed_bookcase #010

    #008
    label snake_strike:
        scene blackscreen #BG-27
        play sound "stone.mp3" volume 1 #SFX-13
        "The stone at the centre of the shape is loose. You pull it out with your fingertips."
        
        show snake at truecenter #SP-17
        with shake
        play sound "snake_hiss.mp3" volume 1 #SFX-44
        "In the dark space behind you see a pair of bright eyes and the flicker of a forked tongue."
        "There's a snake in there! Quickly, before the snake can strike, you push the stone back."
        hide snake #SP-17

        "You chose a shape with eight sides that's an octagon. How many sides does a hexagon have?"
    
        jump puzzle_2 #006
    
    #009
    label puzzle_4:
        scene library #BG-3
        with fade_slow

        show folded_sheet at truecenter #SP-18
        with fade_fast
        "Inside the cover of Through the Looking Glass, you find a folded sheet of paper. It's another clue!"
        hide folded_sheet #SP-18
        with fade_fast

        show three_book at truecenter #SP-19
        with fade_fast
        "You look at the first three books you took down. Each has a shape on the cover. Which shape is not symmetrical? That's the book you must open."
        hide three_book
        with fade_fast 

        show symmetrical at truecenter #SP-85
        with fade_fast
        "You can see that each side of the heart would look identical if held against a mirror. It has a line of symmetry down the middle."
        "The left half is a mirror image of the right. But which of shapes A and B is not symmetrical?"
        hide symmetrical #SP-85
        with fade_fast
        
    $ menu_question = _("Which shape is not symmetrical?")
    $ start_puzzle_timer()
    menu:
        "Book A (p4_bookA)":
            $ log_answer("puzzle_4", "2d_shapes", False)
            jump giant_centipede #011

        "Book B (p4_bookB)":
            $ log_answer("puzzle_4", "2d_shapes", True)

            show hidden_iron_key at truecenter #SP-20
            with fade_fast
            play sound "book_open.mp3" volume 1 #SFX-14
            "You open the cover. The pages have been cut to make a secret hiding place inside." 
            "There is a large iron key hidden in the space. This must be the key in the letter!"

            "You've chosen the correct book! You slip the key into your bag."

            $ add_item("key")

            hide hidden_iron_key
            with fade_fast

            jump puzzle_5 #012

    #010
    label crashed_bookcase:
        scene blackscreen #BG-27
        "You reach up to take the books down from shelf Y."
        
        play sound "loud_bark.mp3" volume 1 #SFX-15
        "As you pull out the first book, a loud bark makes you jump to one side."

        show bookcase_crashes at truecenter #SP-21
        with shake
        play sound "bookcase_crashes.mp3" volume 1 #SFX-16
        "The bookcase topples and crashes to the floor just where you had been standing. That was close! Where did that bark come from?"
        hide bookcase_crashes #SP-21

        show marked_bookcase at truecenter #SP-16
        "You chose the wrong shelf. The E and the 5 are coordinates. Count along the book cases A, B, C, D, E. Count up the shelves 1, 2, 3, 4, 5."
        hide marked_bookcase #SP-16

        jump puzzle_3 #007

    #011
    label giant_centipede:
        scene blackscreen #BG-27
        show giant_centipede at truecenter #SP-22
        with shake
        play sound "giant_centipede.mp3" volume 1 #SFX-17
        "You open the book. The pages have been cut to make a secret space inside. There is something in there."
        "It's a giant centipede! It starts to crawl towards your hand. Then a loud bark makes you jump into action. You slam the book shut."
        hide giant_centipede #SP-22

        "You chose the wrong book! The face is symmetrical. It has a line of symmetry like the heart"

        jump puzzle_4 #009

    #012
    label puzzle_5:
        scene library #BG-3
        with fade_slow

        "Now you have the key you must find the 'ancient shape'. What can it be?"
        "You look around the library for more clues."

        show library_desk at truecenter #SP-23
        with fade_fast
        "There is a large desk in the centre of the room. It is covered with drawings and plans."
        "You take a closer look. One plan seems to be for the library you are standing in! Someone has scribbled a note in one corner…"
        "There is a secret trapdoor! Something important could be hidden there. And the plan shows all the carpets in the room."
        "Which one should you look under to find the trapdoor?"
        hide library_desk
        with fade_fast

    $ menu_question = _("Which carpet with a 6 metres perimeter hides the trapdoor?")
    $ start_puzzle_timer()
    menu:
        "Carpet A (p5_carpetA)":
            $ log_answer("puzzle_5", "perimeter_area", False)
            jump strange_fumes #013

        "Carpet B (p5_carpetB)":
            $ log_answer("puzzle_5", "perimeter_area", True)

            show carpet_perimeter_b at truecenter #SP-82
            with fade_fast
            "You roll up carpet B. There is a trapdoor in the floor beneath! You chose the correct carpet. Its perimeter is 2 m + 1 m + 2 m + 1 m = 6 m."
            hide carpet_perimeter_b #SP-82
            with fade_fast

            jump puzzle_6 #014
    
    #013
    label strange_fumes:
        scene blackscreen #BG-27
        "You roll up carpet A."
        
        show strange_fumes at truecenter #SP-23
        "Strange fumes start to rise from between the floorboards."
        "You are passing out! Then something pushes the carpet back into place."
        hide strange_fumes #SP-23

        play sound "dog_licking.mp3" volume 1 #SFX-10
        "You feel a wet tongue lick your face, and you come around."

        "You chose the wrong carpet! The perimeter is the distance all the way around the shape."
        
        show carpet_perimeter_a at truecenter #SP-24
        "The diagram below shows how to calculate the perimeter of the carpet. Try this with carpet B."
        "Perimeter = 2 m + 2m + 2m + 2 m = 8m"
        hide carpet_perimeter_a #SP-24

        jump puzzle_5 #012

    #014
    label puzzle_6:
        scene library #BG-3
        with fade_slow

        show trapdoor at truecenter #SP-25
        with fade_fast
        "The trapdoor does not have a handle. It is made from squares of wood like a chess board. Some of the squares are coloured to make patterns."
        hide trapdoor #SP-25
        with fade_fast

        show trapdoor_note at truecenter #SP-26
        with fade_fast
        "Then you spot a message scratched into the floorboards…"
        hide trapdoor_note
        with fade_fast

    $ menu_question = _("In what order should you press the shapes from smallest to largest area?")
    $ start_puzzle_timer()
    menu:
        "2, 3, 1 (p6_231)":
            $ log_answer("puzzle_6", "perimeter_area", False)
            jump dark_pit #016

        "2, 1, 3 (p6_213)":
            $ log_answer("puzzle_6", "perimeter_area", True)

            # show dark_hole at truecenter #SP-26
            play sound "door_creak.mp3" volume 1 #SFX-3 
            "It's the correct sequence. The trapdoor swings smoothly up to reveal a dark hole. There is an iron ladder going down below."
            
            scene blackscreen #BG-27
            play sound "steps.mp3" volume 1 #SFX-19 
            "You climb down the ladder into the dark. There are 20 rungs before you reach a cold stone floor. It's a good job you didn't fall!"\

            "As you step off the ladder your foot touches something. It rolls away. You put your hand down and feel around."
            "It's a torch! You press the button and the torch lights up the room. It's an amazing sight!"

            scene storeroom #BG-7
            with fade_slow

            play sound "door_slam.mp3" volume 1 #SFX-20 
            "The trapdoor slams shut above you. Now you are trapped!"
            jump puzzle_7 #015

    #015
    label puzzle_7:
        scene storeroom #BG-7
        with fade_slow

        "You are in a store room under the library."
        "There are boxes of books, and cabinets filled with strange objects a telescope, a brass microscope and other ancient scientific instruments."
        "Everything is covered with cobwebs. In one corner you see a set of mathematical shapes on a shelf."
        "You remember the description in the letter, 'an ancient shape with 5 faces and 8 edges'."
        "Perhaps one of these is the shape you need? You start to count the faces and edges. You record the numbers in a table in your notebook…"
        $ unlock_note("faces_edges")
        "The first three shapes you check don't have the correct number of faces and edges. What about the two that are left?"
    
    $ menu_question = _("Which shape has 5 faces and 8 edges?")
    $ start_puzzle_timer()
    menu:
        "Triangle based pyramid (p7_triangle_based_pyramid)":
            $ log_answer("puzzle_7", "3d_shapes", False)
            jump exploded_pyramid #017

        "Square based pyramid (p7_square_based_pyramid)":
            $ log_answer("puzzle_7", "3d_shapes", True)
            jump puzzle_8 #018


    #016
    label dark_pit:
        scene blackscreen #BG-27
        "You press the shapes in the order 2, 3, 1. Nothing happens, so you press harder."
        
        show dark_pit at truecenter #SP-78
        with shake
        play sound "slam_open.mp3" volume 1 #SFX-21 
        "Suddenly the trapdoor gives way. You are falling into a dark pit!"

        "At the last minute strong teeth grab your shoes. You are dragged back from the danger."
        hide dark_pit #SP-78

        play sound "door_slam.mp3" volume 1 #SFX-20 
        "The trapdoor swings up and slams shut."
        
        show trapdoor_area at truecenter #SP-79
        "You pressed the shapes in the wrong order."
        "The area is the amount of surface a shape covers."
        "When a shape is drawn on a grid you can find its area by counting the squares it surrounds."
        hide trapdoor_area #SP-79

        jump puzzle_6 #014

    #017
    label exploded_pyramid:
        scene blackscreen #BG-27
        "You reach for the triangle-based pyramid. As you grasp it, the pyramid starts to glow. It's getting hotter and hotter! You can't let go!"

        with shake
        "Sparks fly from its corners and your whole body starts to tingle and shake. Then something large leaps across the table, knocking the pyramid from your hand." 
        
        show exploded_pyramid at truecenter #SP-27
        play sound "explosion.mp3" volume 1 #SFX-22
        with flash 
        "Just in time - it explodes into a thousand pieces with a flash like lightning!"

        "You chose the wrong shape. A triangle-based pyramid has 4 faces and 6 sides."
        hide exploded_pyramid #SP-27
        jump puzzle_7 #015
    
    #018
    label puzzle_8:
        scene storeroom #BG-7
        with fade_slow

        show square_based_pyramid at truecenter #SP-28
        with fade_fast
        "You pick up the square-based pyramid. It's heavy in your hand. You turn it around. There is a picture of the Sun and a message on one face."
        "It doesn't make sense! You understand that you will need the pyramid later on, but what's all that about a mummy's case and You look desperately around."
        hide square_based_pyramid #SP-28
        with fade_fast

        show mummy_cases at truecenter #SP-29
        with fade_fast
        "Then your torch shines on two large objects against the wall. They are Egyptian mummy cases! Egyptian mummies were placed inside them in the pyramids!"
        "You walk over to the mummy cases. They have strange symbols on the front. You recognize the symbols! They are mathematical nets."
        "If you draw them on card, you can cut them out and fold them to make solid shapes! One must be the net for a pyramid. That's the one you need."
        hide mummy_cases #SP-29
        with fade_fast

    $ menu_question = _("Which mummy case has the net for a pyramid?")
    $ start_puzzle_timer()
    menu:
        "Red Mummy (p8_redmummy)":
            $ log_answer("puzzle_8", "nets", False)
            jump alive_mummy #020

        "Blue Mummy (p8_bluemummy)":
            $ log_answer("puzzle_8", "nets", True)

            play sound "stone_move.mp3" volume 1 #SFX-23 
            show secret_passage at truecenter #SP-66
            with fade_fast
            "Cautiously you reach forwards and open the lid. It's not a case at all. It's the entrance to a secret passage! You made the right choice."
            hide secret_passage #SP-66
            with fade_fast
            
            scene passage #BG-8
            with fade_slow

            "You pop the pyramid in the bag with the key, shine your torch to show the way, and set off along the passage."

            $ add_item("pyramid")

            jump puzzle_9 #019
    
    #019
    label puzzle_9:
        scene two_cube_passage #BG-28
        with fade_slow

        "Very soon the passage divides. Which way should you go?"
        
        show message_wall at truecenter #SP-30
        with fade_fast
        "Then you see someone has chalked a message and a shape on the wall."
        "You shine your torch along the two passageways. There is a pile of blocks in each one."
        "The piles are turned compared to your drawing. But one of them must have the blocks in the same pattern which will you choose?"

    $ menu_question = _("Which pile of blocks matches the drawing?")
    $ start_puzzle_timer()
    menu:
        "Left Passage (p9_leftpassage)":
            $ log_answer("puzzle_9", "3d_shapes", True)

            hide message_wall #SP-30
            with fade_fast
            "You take the left-hand passage. It's the correct passage!"
            
            scene mansion_garden #BG-10
            with fade_slow

            "Soon it opens into a small building surrounded by trees. You recognize where you are. You are in the Mansion garden not far from the front door."
            "You look back at the Mansion. You see a blaze of light in a window at the top of a turret."
            jump puzzle_10 #022
        
        "Right Passage (p9_rightpassage)":
            $ log_answer("puzzle_9", "3d_shapes", False)
            hide message_wall #SP-30
            with fade_fast
            jump slippery_passage #021

    #020
    label alive_mummy:
        scene blackscreen #BG-27
        show alive_mummy at truecenter #SP-31
        with shake
        "Cautiously, you reach forwards and open the lid."
        "Inside is a mummy wrapped in bandages. Its eyes glow red. Its bony hands reach out to grab your neck. It's going to pull you inside!"
        hide alive_mummy

        play sound "door_slam.mp3" volume 1 #SFX-20 
        "Suddenly the mummy case slams shut. Someone has pushed the door and there are paw marks on it! The mummy is trapped inside again."

        "You chose the wrong case. This is the net for a prism, not a pyramid."

        jump puzzle_8 #018

    #021
    label slippery_passage:
        scene blackscreen #BG-27
        with shake
        "You take the right-hand passage. It is steep and slippery. Your shoes lose their grip. You start to slide, dislodging small pebbles along the way."
        "Then something grabs your collar and pulls you back to safety."

        scene passage #BG-8
        play sound "water_splash.mp3" volume 1 #SFX-24 
        "You hear the pebbles splash into a deep underground pool, that could have been you!"

        "You chose the wrong shape. Try to turn the shapes in your mind to match the one in the drawing. Look at the block at the top of the shape, that will help you."
        jump puzzle_9 #019
    
    #022
    label puzzle_10:
        scene mansion_garden #BG-10
        with fade_slow

        "Which turret was that? You will need to know when you go back inside."
        
        show mansion_plan at truecenter #SP-32
        with fade_fast
        "Then you see a design on the stone floor of the garden building. It's a plan of the Mansion."
        "At the centre of the Mansion there is a square hole with triangular sides. Against one side there is a picture of the sun."
        "Of course! It's the sun from the pyramid! The hole is a pyramid shape!"
        hide mansion_plan #SP-32
        with fade_fast

        "You take the pyramid from your bag" 

        $ done = False
        while not done:
            $ inventory_mode = "use"
            $ needed_item = "pyramid"

            call screen inventory_panel
            $ result = _return
            $ inventory_mode = "normal"
            $ needed_item = None

            if result is True:
                "You used the correct item."
                $ done = True

            elif result is False:
                "That's not the item needed."

        show pyramid_base at truecenter #SP-72
        with fade_fast
        "Turn it upside down and drop it in the hole making sure the sun is on the correct side."
        hide pyramid_base #SP-72
        with fade_fast

        show mansion_plan_pyramid at truecenter #SP-77
        with fade_fast
        "A diagram on the base of the pyramid shows the points of the compass. Now you can tell which turret is which!"
        hide mansion_plan_pyramid #SP-77

    $ menu_question = _("Which turret is to the south-west?")
    $ start_puzzle_timer()
    menu:
        " (p10_southwest)":
            $ log_answer("puzzle_10", "cardinal_directions", True)
            with fade_fast

            jump compass_direction_hint #024

        " (p10_northwest)":
            $ log_answer("puzzle_10", "cardinal_directions", False)
            with fade_fast

            jump waste_of_time #023
    
    #023
    label waste_of_time:
        scene blackscreen #BG-27
        with fade_slow
        "That's the wrong turret! If you go there you will waste too much time."
        jump puzzle_10 #022

    #024
    label compass_direction_hint:
        scene mansion_garden #BG-10
        with fade_slow

        "That's the correct turret. You write 'south-west' in your notebook. You pick up the pyramid and head back to the Grand Hall."
        $ unlock_note("southwest")

        $ finished_library = True
        jump main_hall #003

##### C #####

    #025
    label puzzle_11:
        scene two_passage #BG-9
        with fade_slow

        "After a few steps the passage splits in two. Which way should you go?"
        
        show message_wall2 at truecenter #SP-33
        with fade_fast
        "Then you see a message chalked on the wall…"
    
    $ menu_question = _("Which passage is perpendicular to your direction?")
    $ start_puzzle_timer()
    menu:
        "Left (p11_left)":
            $ log_answer("puzzle_11", "lines", True)
            hide message_wall2 #SP-33
            with fade_fast

            scene passage #BG-8
            with fade_slow

            "You took the correct passage! Perpendicular means 'at a right angle', or 90 degrees. The other passageway was at a 45-degree angle to your direction."
            jump puzzle_12 #027

        "Right Slant (p11_right)":
            $ log_answer("puzzle_11", "lines", False)
            hide message_wall2 #SP-33
            with fade_fast

            jump rat_bites #026

    #026
    label rat_bites:
        scene blackscreen #BG-27
        "You turn right and keep walking. The passage goes on and on. It's getting cold and damp. You shiver."
        
        play sound "scurrying.mp3" volume 1 #SFX-25
        with shake
        "Suddenly there is a scurrying sound. Something runs over your foot."
        show rats at truecenter #SP-34
        "There are rats down here, hundreds of them! They are biting at your trouser legs!"
        hide rats #SP-34

        play sound "loud_bark.mp3" volume 1 #SFX-15
        "Then something big jumps among the rats - barking and yapping. They scurry away."

        "You took the wrong passage! Perpendicular means 'at a right angle', or 90 degrees. You follow the string back to the turning point."    
    
        jump puzzle_11 #025
    
    #027
    label puzzle_12:
        scene three_passage #BG-11
        with fade_slow

        "The passage soon divides again this time in three directions."
        
        show pinned_note at truecenter #SP-35
        with fade_fast
        "There is another set of instructions pinned to the wall…"

    $ menu_question = _("Which direction should you turn clockwise?")
    $ start_puzzle_timer()
    menu:
        "Left (p12_left)":
            $ log_answer("puzzle_12", "angles", False)
            hide pinned_note #SP-35
            with fade_fast

            jump green_eyes_creature #029

        "Right (p12_right)":
            $ log_answer("puzzle_12", "angles", True)
            hide pinned_note #SP-35
            with fade_fast

            jump puzzle_13 #028
    
    #028
    label puzzle_13:
        scene two_passage #BG-9
        with fade_slow

        "It's the correct direction. But soon the passageway splits again, this is giving you a headache!"
        
        show note_wall at truecenter #SP-36
        with fade_fast
        "There are more instructions taped on the wall."
    
    $ menu_question = _("Which direction is an obtuse angle?")
    $ start_puzzle_timer()
    menu:
        "Left (p13_left)":
            $ log_answer("puzzle_13", "angles", False)
            hide note_wall #SP-36
            with fade_fast

            jump minotaur #030

        "Right (p13_right)":
            $ log_answer("puzzle_13", "angles", True)
            hide note_wall #SP-36
            with fade_fast

            scene passage #BG-8
            with fade_slow

            "You have taken the right direction. An obtuse angle is between 90 degrees and 180 degrees. The other direction was less than 90 degrees to your tunnel, that's an acute angle."
            jump puzzle_14 #031

    #029
    label green_eyes_creature:
        scene blackscreen #BG-27
        play sound "flickering.mp3" volume 1 #SFX-7
        with flash
        "You turn left and carry on. The light bulbs start to flicker faster and faster. Then they go out! It is completely dark!"

        show green_eyes at truecenter #SP-84
        play sound "growling.mp3" volume 1 #SFX-26
        with shake
        "You hear a deep growling sound ahead. Two green eyes appear from the shadows. What is it?"
        
        play sound "loud_bark.mp3" volume 1 #SFX-15
        "From behind you comes a loud barking sound. The eyes back away."
        hide green_eyes #SP-84

        "You turn and follow your string back to the turning place. The lights come back on."
        "When you turned to the left you turned anticlockwise. You should have turned clockwise and gone to the right."

        jump puzzle_12 #027
    
    #030
    label minotaur:
        scene blackscreen #BG-27
        "You turn to the right by less than a right angle, but suddenly come to a dead-end."
        
        show minotaur at truecenter #SP-37
        with shake
        "You turn around. A dog with huge jaws and glowing green eyes blocks your path. It's Minotaur, the bull-mastifl!"
        
        play sound "dog_growl.mp3" volume 1 #SFX-47
        "Then you hear growling from behind you. Minotaur looks nervous. The growling gets louder until Minotaur runs away."
        hide minotaur #SP-37

        "You chose the wrong direction."
        "An obtuse angle is between 90 degrees and 180 degrees. You turned less than 90 degrees, that's an acute angle."
        "You follow the string back to the turning point."

        jump puzzle_13 #028
    
    #031
    label puzzle_14:
        scene candle_storage #BG-12
        with fade_slow

        "The passageway ends at a door labelled 'Candle Store'."
        
        play sound "door_creak.mp3" volume 1 #SFX-3 
        "You turn the handle and enter. The storeroom is packed with candles on shelves."

        "You remember the note at the top of the cellar stairs said, You will need a shape with no flat faces and no edges to light your way.' It could be a candle!"

    $ menu_question = _("Which candle has no flat faces and no edges?")
    $ start_puzzle_timer()
    menu:
        "Spherical (p14_spherical)":
            $ log_answer("puzzle_14", "3d_shapes", True)

            "You take a spherical candle from the shelf. You step back through the door."
            show sphere_candle at truecenter #SP-73
            with fade_fast
            "Suddenly all the lights in the passage fail! But a flame appears on your candle. It lights your way - just as the letter said it would!"
            "You were right. A sphere has no flat surfaces or edges. Its surface is a smooth curve all over."
            hide sphere_candle #SP-73
            with fade_fast

            jump puzzle_15 #032

        "Cylindrical (p14_cylindrical)":
            $ log_answer("puzzle_14", "3d_shapes", False)
            jump heated_room #033
    
    #032
    label puzzle_15:
        scene candle_storage #BG-12
        with fade_slow

        show note_pinned at truecenter #SP-38
        with fade_fast
        "As you leave the Candle Store you see another note pinned to the door. You study the directions on the note…"
        hide note_pinned #SP-38
        with fade_fast

        "You leave the Candle Store, turning left out of the door." 
        
        scene four_passage #BG-13
        with fade_slow

        "Soon you come to a space with passages leading in four directions, just as the note said you would."
        "Which one is parallel to the passage along which you came?"
    
    $ menu_question = _("Which passage is parallel to the one you came from?")
    $ start_puzzle_timer()
    menu:
        "Passage 2 (p15_passage2)":
            $ log_answer("puzzle_15", "lines", False)
            jump freezer_room #034

        "Passage 4 (p15_passage4)":
            $ log_answer("puzzle_15", "lines", True)

            scene passage #BG-8
            with fade_slow

            "You have chosen the correct direction! You walk along the passage."
            play sound "steam_hiss.mp3" volume 1 #SFX-28
            queue sound "flame_blast.mp3" volume 1 #SFX-12
            "The air gets warmer. You hear the hiss of steam and the roar of flames. You must be heading for the boiler room. That's where the letter told you to go!"
            jump puzzle_16 #035

    #033
    label heated_room:
        scene heated_room #BG-14
        play sound "flame.mp3" volume 1 #SFX-29
        with shake
        "You lift down a cylindrical candle from the shelf. Its wick bursts into flame. The other candles start to light, too."
        "The small room gets hotter and hotter! The candles start to melt the flames start to spread!"

        "You spot a bucket of sand in the corner. You spread the sand to smother the flames that was close!"
        
        scene candle_storage #BG-12
        "You chose the wrong candle. A cylinder has two flat surfaces in the shape of circles one at either end."

        jump puzzle_14 #031

    #034
    label freezer_room:
        scene passage #BG-8
        "You set off along passage 2. It gets colder the further you go. There is a door at the end marked 'Ice Store'."
        
        scene freezer_room #BG-15
        play sound "door_creak.mp3" volume 1 #SFX-3
        "You open it and look inside. The walls and ceiling are covered in frost."
        
        play sound "door_slam.mp3" volume 1 #SFX-20
        with shake 
        "Then the door slams behind you. You hear the key turn in the lock! You are trapped! You will freeze!"
        
        play sound "scrabbling.mp3" volume 1 #SFX-30
        "Then you hear paws scrabbling at the door."
        
        play sound "key_clang.mp3" volume 1 #SFX-31
        "The key drops to the floor with a clang. It is pushed under the door so you can escape!"

        scene passage #BG-8
        "You chose the wrong direction. When two directions are parallel they are the same distance apart at every point and never meet."
        "You follow your string back along the passageway."

        jump puzzle_15 #032

    #035
    label puzzle_16:
        scene boiler_room #BG-16
        with fade_slow

        play sound "steam_hiss.mp3" volume 1 #SFX-28
        "The boiler room door is open. It's very hot inside. The fire is blazing inside the furnace. Hot steam pipes rattle and hiss."
        "The pressure gauge shows danger when the boiler is about to explode!"
        
        show boiler_notice at truecenter #SP-39
        with fade_fast
        "You see a notice on the boiler wall…"
        
        with fade_fast

    $ menu_question = _("Which valve shows the position after being rotated 360 degrees?")
    $ start_puzzle_timer()
    menu:
        " (p16_180)":
            $ log_answer("puzzle_16", "angles", False)
            hide boiler_notice #SP-39
            "You've made half a turn. That's only 180 degrees! The pipes start to shake and squeal!"
            "You realize your mistake. You turn the wheel another half turn. That makes 360 degrees altogether. The pressure starts to fall."
            jump puzzle_17 #036

        " (p16_360)":
            $ log_answer("puzzle_16", "angles", True)
            hide boiler_notice #SP-39
            "You have turned the wheel a whole turn. That's correct. One whole turn is 360 degrees. The pressure starts to fall and the boiler settles down."
            jump puzzle_17 #036

    #036
    label puzzle_17:
        scene boiler_room #BG-16
        with fade_slow

        "You look around the rest of the boiler room, In one corner you see a stack of thin parcels wrapped with brown paper."
        
        show wrapped_painting at truecenter #SP-40
        with fade_fast
        "Are they the stolen paintings? You look closely at the parcels, You recognize some of the shapes, but there are too many!"
        hide wrapped_painting #SP-40
        with fade_fast

        show parcel_note at truecenter #SP-69
        with fade_fast
        "Then you find a note on one of the parcels…"
        hide parcel_note
        with fade_fast

        "You look back at your notebook for the shapes of the paintings."
        
        show screen notebook_panel
        "You've written 'square, rectangle, hexagon, octagon'."

    $ menu_question = _("Which parcels contain the real paintings?")
    $ start_puzzle_timer()
    menu:
        "Shape B (p17_shapeB)":
            $ log_answer("puzzle_17", "2d_shapes", False)
            jump loud_bark_noise #037

        "Shape A (p17_shapeA)":
            $ log_answer("puzzle_17", "2d_shapes", True)
            jump silver_button_hint #038

    #037
    label loud_bark_noise:
        scene boiler_room #BG-16
        play sound "loud_bark.mp3" volume 1 #SFX-15
        "A loud barking noise warns you that something is wrong. You have not picked up all the real paintings! Quickly you replace the fake paintings."
        
        show trapezium at truecenter #SP-79
        "This shape is a trapezium, not a hexagon. A hexagon has six sides."
        hide trapezium #SP-79

        show pentagon at truecenter #SP-80
        "This shape is a pentagon, not an octagon. An octagon has eight sides."    
        hide pentagon #SP-80

        jump puzzle_17 #036

    #038
    label silver_button_hint:
        scene boiler_room #BG-16
        with fade_slow

        "You have taken the correct paintings! You run from the boiler room with them in your arms."

        $ add_item("painting")
        
        scene passage #BG-8
        with fade_slow

        play sound "heavy_footstep.mp3" volume 1 #SFX-32
        "You hear heavy footsteps coming down the passageway."

        play sound "scrabbling.mp3" volume 1 #SFX-30
        "Which way should you go? Then you hear a scraping sound. A hidden door is opening in the wall!"
        "You feel afraid and turn to run, but strong teeth grab you from behind. They pull you through the door."
        
        scene treasure_room #BG-17
        with fade_slow

        "You are in a small room filled with precious china, silver plates and candlesticks."
        "This is where the Mansion's valuables are kept! It's a great place to hide the paintings."
        
        play sound "shout.mp3" volume 1 #SFX-33
        "Then you hear an angry shout. The burglar has discovered the paintings are gone!"

        play sound "running.mp3" volume 1 #SFX-34
        "He or she runs back the way they came. You hear footsteps disappearing into the distance."

        "You have saved the paintings! But there is still much to do. There are burglars to catch!"
        
        play sound "door_creak.mp3" volume 1 #SFX-3
        scene passage #BG-8
        with fade_slow
        "The secret door opens again as you push it. You begin to follow the string to find your way back."
        
        show silver_button at truecenter #SP-41
        with fade_fast 
        "As you pass the boiler room you see something shining on the floor."
        "It's a silver button. It could be another clue! You pop it in your pocket, and follow the string all the way back to the entrance hall."

        $ add_item("button")

        hide silver_button #SP-41 
        with fade_fast

        $ finished_cellar = True
        jump main_hall #003

##### D #####
    
    #039
    label puzzle_18:
        scene kitchen #BG-5
        with fade_slow

        "You look around. Then you see a set of kitchen scales on a table. Next to it is a bag of flour, and a floury hand print on the table top."
        
        show flour_hand_print at truecenter #SP-42
        with fade_fast 
        "The hand that made the print has a scar! You sketch the print in your notebook."
        $ unlock_note("handprint")
        hide flour_hand_print #SP-42
        with fade_fast 

        show flour_note1 at truecenter #SP-43
        with fade_fast
        "Someone has left a list of instructions on a scrap of paper next to the flour. You decide to follow the instructions to work out what they were doing!"
        hide flour_note1
        with fade_fast

    $ menu_question = _("How much flour should you add to reach exactly 0,5 kg?")
    $ start_puzzle_timer()
    menu:
        " (p18_05kg)":
            $ log_answer("puzzle_18", "measurement", True)

            "You chose the correct weights! You add the flour until the scales are level."
            jump puzzle_19 #040

        " (p18_005kg)":
            $ log_answer("puzzle_18", "measurement", False)
            jump scale_trap #041

    #040
    label puzzle_19:
        scene kitchen #BG-5
        with fade_slow

        show bowl_note at truecenter #SP-68
        with fade_fast
        "You read the next instruction…"
        hide bowl_note #SP-44
        with fade_fast

        "There is a row of bowls of all different sizes - high on a shelf."
        "But which is the 15 cm radius bow!? Then you remember your school ruler is 30 cm long."

        show bowls at truecenter #SP-45
        with fade_fast
        "You try to imagine your ruler next to each of the bowls."
        hide bowls #SP-45
        with fade_fast

    $ menu_question = _("Which bowl has a radius of 15 cm?")
    $ start_puzzle_timer()
    menu:
        "Bowl X (p19_bowlx)":
            $ log_answer("puzzle_19", "circles", True)

            "You have chosen the correct bowl. Its diameter is 30 cm. so its radius is 15 cm."
            show water_note at truecenter #SP-74
            with fade_fast
            "You read the next instruction…"
            hide water_note
            with fade_fast

            jump puzzle_20 #042

        "Bowl Y (p19_bowly)":
            $ log_answer("puzzle_19", "circles", False)
            jump poisonous_spider #043

    #041
    label scale_trap:
        scene blackscreen #BG-27
        play sound "crashed.mp3" volume 1 #SFX-27
        with shake 
        "You start pouring the flour. The scales tilt with a jerk. Someone has tied a string to one pan. It's a trap!"

        show oven_fire at truecenter #SP-75
        with flash
        play sound "flame.mp3" volume 1 #SFX-29
        "The string pulls a jar of oil from a shelf onto an oven. The jar shatters. The oil catches fire! You must not put water on an oil fire because it will spread!"

        play sound "loud_bark.mp3" volume 1 #SFX-15
        "Then a bark makes you turn. You see a fire blanket next to the ovens. You grab it and spread it over the flames. The flames go out."
        hide oven_fire #SP-75

        "There are 1000 g in a kg, so 0.5 kg is 500 g not 50 g."

        jump puzzle_18 #039

    #042
    label puzzle_20:
        scene kitchen #BG-5
        with fade_slow

        show shaker_note at truecenter #SP-46
        with fade_fast
        "You look around for some salt. You see three shakers on a shelf. There is a note next to them…"
        hide shaker_note #SP-46
        with fade_fast

        show shaker at truecenter #SP-47
        with fade_fast
        "You decide to see how the shapes roll."
        "You try the cuboid first. You lay it on its side but it will not roll at all."
        "Then you try the cylinder and the cone. One of them rolls in a straight line away from you. The other rolls around in a circle and comes back!"
        hide shaker
        with fade_fast

    $ menu_question = _("Which shaker rolls but will not roll away?")
    $ start_puzzle_timer()
    menu:
        "Cylinder (p20_cylinder)":
            $ log_answer("puzzle_20", "3d_shapes", False)
            jump strong_pepper #044

        "Cone (p20_cone)":
            $ log_answer("puzzle_20", "3d_shapes", True)

            play sound "shaker.mp3" volume 1 #SFX-35
            "You shake the cone over the flour bowl. It's the right shaker. A sprinkle of salt falls onto the flour."
            "A cone rolls in a circle when you lay it on its side."
            "On the shelf next to the shakers you see a jar labelled 'yeast', You add a spoonful of that to your mixture, too."
            jump puzzle_21 #045
    
    #043
    label poisonous_spider:
        scene blackscreen #BG-27
        "As you lift the bowl from the shelf you look inside. A row of shiny white eyes stares back!"
        
        show spider at truecenter #SP-48
        with shake
        play sound "spider.mp3" volume 1 #SFX-50
        queue sound "loud_bark.mp3" volume 1 #SFX-15
        "It's a huge poisonous spider! A loud bark makes you drop the bowl. It shatters. The spider scuttles behind the sinks."
        hide spider #SP-48

        show radius_diameter at truecenter #SP-83
        "You chose the wrong bowl! The radius of a circle is half its diameter. Bowl Y has a diameter of 15 cm, so its radius is 7.5 cm."
        hide radius_diameter #SP-83

        jump puzzle_19 #040
    
    #044
    label strong_pepper:
        scene blackscreen #BG-27
        show pepper_shaker at truecenter #SP-81
        play sound "shaker.mp3" volume 1 #SFX-35
        with shake
        "You shake the cylinder over the flour bowl. It's pepper, not salt."
        "But this is not ordinary pepper, it is extra strong! Your eyes are watering, your nose running and your mouth burning. You think your head will explode!"
        hide pepper_shaker #SP-81

        "Then something pushes you to the sinks you need to wash the pepper away. You hold your head under a running tap until you feel better."
        "A cylinder rolls in a straight line when you lay it on its side."

        jump puzzle_20 #042
    
    #045
    label puzzle_21:
        scene kitchen #BG-5
        with fade_slow

        "Now you need some water. There are plenty of taps over the sinks, but how will you measure 250 ml? You see a measuring jug. That's what you need!"
        show jug_scale at truecenter #SP-49
        with fade_fast
        "The jug has a scale. It is marked 1 litre at the top, but the only other markings are fractions."
        "Luckily you think you know how many millilitres there are in a litre. So you fill the jug to the correct level."
        hide jug_scale
        with fade_fast

    $ menu_question = _("Which measuring cup shows exactly 250 ml of water?")
    $ start_puzzle_timer()
    menu:
        " (p21_500ml)":
            $ log_answer("puzzle_21", "measurement", False)
            jump ivy_trap #046

        " (p21_250ml)":
            $ log_answer("puzzle_21", "measurement", True)

            "You have measured correctly! As you stir in the water, the mixture becomes soft and rubbery. It's bread dough! That must be the clue."
            "You remember smelling baking bread. Someone had been baking just before you arrived. It must have been the burglars, but why would they bake bread in the middle of a robbery?"
            jump bite_footprint_hint #047

    #046
    label ivy_trap:
        scene blackscreen #BG-27
        play sound "shatters.mp3" volume 1 #SFX-36
        "That's too much water! As you lift the jug, its handle snaps. It had been partly cut through! The jug shatters. The water seeps between the flagstones on the kitchen floor."
        
        show ivy at truecenter #SP-50
        with shake
        "Ivy starts to grow from the cracks. It wraps around your ankles you are trapped!"
        hide ivy #SP-50
        "Then you feel strong jaws grab your belt and pull."
        "You break free from the tendrils. Quickly, you sprinkle salt on the ivy leaves, and they shrink back."
        "There are 1000 ml in a litre. So 250 ml is less than ½ litre. What fraction of 1000 is 250?"

        jump puzzle_21 #045
    
    #047
    label bite_footprint_hint:
        scene larder #BG-18
        with fade_slow

        "You look around for the newly baked bread. The smell leads you into the larder where there is a pile of fresh loaves."
        
        show bite_bread at truecenter #SP-51
        with fade_fast
        "One of the loaves has a bite mark in it. The burglar could not resist eating the warm bread!"
        "Then you notice something odd. There is a gap in the teeth marks, It's another clue! This burglar has a missing tooth! You take the piece with the teeth marks to use as evidence."
        "As you pick up the loaf it feels too heavy for bread. You break the loaf open."
        hide bite_bread #SP-51
        with fade_fast

        show necklace_bread at truecenter #SP-52
        with fade_fast
        "There is a necklace inside! You feel the other loaves. They are heavy, too. That's how the burglars have hidden the jewels!"

        $ add_item("jewellery")

        hide necklace_bread #SP-52
        with fade_fast

        queue sound "footstep.mp3" volume 1 #SFX-37
        "Then you hear footsteps in the corridor. One of the burglars is coming back. Quickly you hide the broken bread under the other loaves."

        "You spot a cupboard where you can hide, but before you get inside, you sprinkle flour on the floor"
        "From inside the cupboard you hear the burglar's footsteps. Luckily he or she doesn't spot the broken loaf. You keep still until the footsteps retreat."

        show footprint_flour at truecenter #SP-53
        with fade_fast
        "As you climb out from the cupboard you look at the floor. The burglar has left clear footprints in the flour. You take out your notebook and make a careful sketch..."
        $ unlock_note("footprint")
        hide footprint_flour #SP-53
        with fade_fast

        show pawprint_flour at truecenter #SP-54
        with fade_fast
        "There are some paw prints as well!"
        hide pawprint_flour #SP-54
        with fade_fast

        scene kitchen #BG-5
        with fade_slow

        "Now you have located the jewels in the kitchen, and found the teeth marks in the bread, you must look for clues in other parts of the Mansion."
        "You head back to the Grand Hall as fast as you can!"

        $ finished_kitchen = True
        jump main_hall #003

##### E #####

    #048
    label scribbled_note:
        scene interior_mansion #BG-2
        with fade_slow

        show scribbled_note at truecenter #SP-55
        with fade_fast
        "You run up the stairs. On the top step you find a scribbled note…"
        hide scribbled_note
        with fade_fast 
    
    $ required_items = ["key", "jewellery", "painting"]
    $ missing_items = []

    python:
        for item in required_items:
            if not has_item(item):
                missing_items.append(items[item]["label"])

    if missing_items:
        $ renpy.say(None, _("You haven't found all the lost items yet."))

        python:
            not_found_text = renpy.translate_string("You haven't found")
            for item_name in missing_items:
                translated_item = renpy.translate_string(item_name)
                renpy.say(None, "{} {}.".format(not_found_text, translated_item))

        jump main_hall #003

    else:
        "You have found all the lost items."
        jump puzzle_22 #049

    #049
    label puzzle_22:
        scene interior_mansion #BG-2
        with fade_slow

        show barkimedes at truecenter #SP-56
        with fade_fast
        "Suddenly you realize a large friendly dog is bounding up the stairs with you."
        "It's Barkimedes the bloodhound. The Mansion is his home, and he's been helping you all along!"
        hide barkimedes #SP-56
        with fade_fast

        "On the first-floor landing there are rows of doors. All are closed apart from one. You step inside."

        play sound "door_creak.mp3" volume 1 #SFX-3
        scene owner_bedroom #BG-19
        with fade_slow

        "It's the owner's bedroom! The burglars have been in and stolen some of his clothes! Why would they do that? In their hurry they seem to have knocked the clock from the table." 

        show knocked_clock at truecenter #SP-57
        with fade_fast
    
    $ menu_question = _("What time does the stopped clock show?")
    $ start_puzzle_timer()
    menu:
        " (p22_0245)":
            $ log_answer("puzzle_22", "time", False)
            hide knocked_clock #SP-57
            with fade_fast

            jump wrong_time #050

        " (p22_0915)":
            $ log_answer("puzzle_22", "time", True)
            hide knocked_clock #SP-57
            with fade_fast
            
            jump puzzle_23 #051
    
    #050
    label wrong_time:
        scene blackscreen #BG-27
        "That's the wrong time! The big hand shows the minutes and the little hand the hours."
        "The little hand is on the nine. The big hand is pointing at three a quarter of the way around the clock face."
        "It is a quarter past nine. We could also call this nine fifteen (9:15) because there are 60 minutes in an hour and so a quarter of an hour is 15 minutes."

        jump puzzle_22 #049
    
    #051
    label puzzle_23:
        scene owner_bedroom #BG-19
        with fade_slow
        "That's the correct time! The clock was stopped at a quarter past nine."
        
        show clock_note at truecenter #SP-58
        with fade_fast
        "Then you see a note on the mantelpiece. You read it carefully…"
        hide clock_note #SP-58
        with fade_fast

        show watch at truecenter #SP-59
        with fade_fast
        "You look at your watch to see the time now…"
    
    $ menu_question = _("What time do you set the clock to now?")
    $ start_puzzle_timer()
    menu:
        " (p23_130)":
            $ log_answer("puzzle_23", "time", True)

            hide watch #SP-59
            with fade_fast
            play sound "ticking.mp3" volume 1 #SFX-45
            "That's correct! As you move the hands to the correct time, it starts to tick."
            
            jump puzzle_24 #052

        " (p23_1215)":
            $ log_answer("puzzle_23", "time", False)

            hide watch #SP-59
            with fade_fast

            jump loud_alarm_sound #053
    
    #052
    label puzzle_24:
        scene owner_bedroom #BG-19
        with fade_slow

        "You look around the bedroom for more clues. You see a door next to the bed. The door is open a crack and you see the light is on."

        play sound "door_creak.mp3" volume 1 #SFX-3
        scene bathroom #BG-20
        with fade_slow

        "You open the door slowly and find yourself in a small bathroom. The basin is a mess. Someone has been using hair dye and hair clippers!"
        
        "Then you see someone has been playing noughts and crosses in the steam on the bathroom mirror. There is a message underneath..."
    
    $ menu_question = _("Which symbol makes the pattern symmetrical?")
    $ start_puzzle_timer()
    menu:
        " (p24_x)":
            $ log_answer("puzzle_24", "2d_shapes", True)

            scene bathroom_cross #BG-33
            with fade_slow
            "A cross is correct! The pattern looks the same if you turn it by 90 degrees or 180 degrees, or look at it in a mirror."

            scene bathroom_message #BG-29
            with fade_slow

            "As you add the cross, steam starts to clear from the mirror. Another message is revealed…"
            
            scene hallway #BG-32
            with fade_slow

            "Barkimedes leads the way. Together you follow the burglars' footprints from the bedroom into the passage."
            "The passage twists and turns. You pass dozens more rooms, but they are all empty."
            "The passage finally ends at an old wooden door, leading to the turrets."
            play sound "locked.mp3" volume 1 #SFX-6 
            "The door is locked! But you have the old iron key."
            jump puzzle_25 #054

        " (p24_o)":
            $ log_answer("puzzle_24", "2d_shapes", False)
            jump scalding_water #055
    
    #053
    label loud_alarm_sound:
        scene blackscreen #BG-27
        play sound "loud_alarm.mp3" volume 1 #SFX-38
        with shake
        "You've set the clock to the wrong time! Its alarm starts to sound loudly."
        "The burglars will hear it! Quickly, you take a pillow from the bed and muffle the sound until it stops. '1:30' is the same as 'half-past one'."

        jump puzzle_23 #051

    #054
    label puzzle_25:
        scene hallway #BG-32
        with fade_slow

        "You take the key from your bag and fit it in the keyhole."
        
        $ done = False
        while not done:
            $ inventory_mode = "use"
            $ needed_item = "key"

            call screen inventory_panel
            $ result = _return
            $ inventory_mode = "normal"
            $ needed_item = None

            if result is True:
                "You used the correct item."
                $ done = True

            elif result is False:
                "That doesn't work."
        
        play sound "unlocked.mp3" volume 1 #SFX-39
        "It's stiff but you manage to turn it."
        
        scene round_room #BG-21
        with fade_slow
        
        "A short flight of steps climbs to a circular room. Four passageways lead from the room at right angles to each other."
        "The passages lead to the turrets! But which is which?"
        "Then you see it! There is a pyramid-shaped hole at the centre of the floor."
        "Just like the one in the garden! You take the pyramid from your bag and drop it into the hole with the sun picture on the correct side."

        $ done = False
        while not done:
            $ inventory_mode = "use"
            $ needed_item = "pyramid"

            call screen inventory_panel
            $ result = _return
            $ inventory_mode = "normal"
            $ needed_item = None

            if result is True:
                scene round_room_pyramid #BG-30
                with fade_slow
                "You used the correct item."
                $ done = True

            elif result is False:
                "That's not the item needed."
        
        "Now you can go to the correct turret! Which do you choose?"

    $ menu_question = _("Which turret leads to the south-west?")
    $ start_puzzle_timer()
    menu:
        "Turret X (p25_turretx)":
            $ log_answer("puzzle_25", "cardinal_directions", True)
            # hide pyramid #SP-61
            jump puzzle_26 #057

        "Turret Y (p25_turrety)":
            $ log_answer("puzzle_25", "cardinal_directions", False)
            # hide pyramid #SP-61
            jump topple_into_empty_space #056
    
    #055
    label scalding_water:
        scene steamed_bathroom #BG-31
        play sound "water_flow.mp3" volume 1 #SFX-40
        with flash
        "As you add a nought to the pattern, the bathroom begins to fill with steam."
        "The taps gush scalding water. You can't turn them off! The door is locked you cannot escape!"

        play sound "door_crash.mp3" volume 1 #SFX-43
        with shake
        "Then there is a loud crash. It's Barkimedes! He has broken through the door. He has a large spanner in his mouth. You use the spanner to turn off the taps."
        "Adding the nought did not make the pattern symmetrical. There are now more noughts on the right than on the left."

        jump puzzle_24 #052

    #056
    label topple_into_empty_space:
        scene blackscreen #BG-27
        "You set off along the passage and spot another door. It must lead into the turret."
        
        show hole at truecenter #SP-62
        with shake
        "You open it, but there is no floor! You start to topple over into empty space. But Barkimedes grabs your shirt with his teeth and pulls you back."
        hide hole #SP-62

        "You took the wrong passage. With the compass points facing this way, turret Y is to the north-east."

        jump puzzle_25 #054
    
    #057
    label puzzle_26:
        scene hallway #BG-32
        # with fade_slow

        "You set off along the passage. Soon you see footprints. You are going in the right direction! At the end of the passage you find a door."
        
        scene turret #BG-22
        with fade_slow
        "It opens onto a spiral staircase. You saw the light at the top of the turret, so you climb up."

        show turret_door at truecenter #SP-63
        with fade_fast
        "You're getting so used to all this maths that you decide to count the stairs as you climb. There are exactly 28. The staircase ends at another door."
        hide turret_door #SP-63
        with fade_fast

        show turret_note at truecenter #SP-67
        with fade_fast
        "There is a note pinned to the wood. You read it carefully…"
        "There are two handles on the door, one labelled January, the other February."
        hide turret_note
        with fade_fast

    $ menu_question = _("Which month has fewer days?")
    $ start_puzzle_timer()
    menu:
        " (p26_january)":
            $ log_answer("puzzle_26", "time", False)
            jump flames_spurt #058

        " (p26_february)":
            $ log_answer("puzzle_26", "time", True)

            "You grip the February handle and turn it."
            show old_rhyme at truecenter #SP-70
            with fade_fast
            "The door opens. You had remembered the old rhyme..."
            hide old_rhyme #SP-70
            with fade_fast
            
            "You step inside, ready to face the burglars. Barkimedes is with you."
            
            jump puzzle_27 #059
    
    #058
    label flames_spurt:
        scene blackscreen #BG-27
        show flames_spurt at truecenter #SP-64
        play sound "flame.mp3" volume 1 #SFX-29
        with shake
        with flash
        "The January handle comes away in your hand! The door starts to shake. Smoke and flames spurt from the edges."
        "Quickly you place the handle back in position. How many days are there in January? How many in February?"
        
        jump puzzle_26 #057
    
    #059
    label puzzle_27:
        scene empty_room #BG-23
        with fade_slow
        show table_note at truecenter #SP-65
        with fade_fast
        "The room is empty! There is just a lamp standing on a table next to a hastily written letter…"
        with fade_fast
        hide table_note
        
        scene turret #BG-22
        with fade_slow
        "As fast as you can you race down the stairs, counting as you go... three hundred and sixty, three hundred and sixty one, three hundred and sixty two…"
        

    $ menu_question = _("How many days are there in a normal year?")
    $ start_puzzle_timer()
    menu:
        " (p27_365)":
            $ log_answer("puzzle_27", "time", True)

            scene turret #BG-22
            with fade_slow
            "You reach step 365 and stop. There is a door on your left. This must be it! You listen for a moment."
            play sound "mumblling.mp3" volume 1 #SFX-41
            "There are voices inside!"
            "Taking a deep breath you open the door and step through. Barkimedes is by your side."

            jump puzzle_28 #060

        " (p27_366)":
            $ log_answer("puzzle_27", "time", False)

            scene turret #BG-22
            with fade_slow
            "You reach step 366 and stop. There is a door on the right. This must be it! You listen for a moment."
            play sound "mumblling.mp3" volume 1 #SFX-41
            "There are voices inside! Taking a deep breath you open the door and step through. Barkimedes is with you."
            jump empty_room_with_fire #061
    
    #060
    label puzzle_28:
        scene secret_chamber #BG-24
        with fade_slow

        "There are three people in the room. A man and woman are standing. A second man is tied up in a chair."
        "The two men look identical! At first the standing man and woman look shocked. Then the man tries to smile."
        c "Thank goodness you're here!"
        c "I am the owner of the Mansion and this is my cook. We caught the burglar and tied him up. He is my butler. He has disguised himself to look like me."
        "The woman smiles, she has a gap in her teeth!"
        w "That's right,"
        w "He was about to get away. If you guard him, we'll fetch the police!"
        "Then the man in the chair speaks."
        t "Don't listen to them,"
        t "I'm the owner of the Mansion. I've been leaving you notes. These criminals are my butler and cook!"
        "Who should you believe?"
        "Then you remember the clues you have collected along the way. You ask the two men to hold out a hand and to take off a shoe. This is what you see…"

    $ menu_question = _("Who is the real owner of the Mansion?")
    menu:
        "Standing Man (p28_standingman)":
            jump wrong_man #062
        "Sitting Man (p28_sittingman)":
            scene buglar_catched #BG-25
            with fade_slow

            "The clues confirm the truth!"
            "The burglars have captured the owner and tied him up! As Barkimedes stands guard over the two criminals you untie the prisoner."
            "The owner explains the burglars' plot."
            "The butler and the cook were going to keep him prisoner in the cellar. The butler would pretend to be him when the police came."
            "After the police had failed to solve the crime, the criminals would take the paintings and jewellery from their hiding places, and make their getaway!"
            jump criminals_catched #063
    
    #061
    label empty_room_with_fire:
        scene blackscreen #BG-27
        play sound "door_slam.mp3" volume 1 #SFX-20
        "The room is empty! The sound of voices is coming through an air vent. The door slams behind you."
        
        play sound "rumble.mp3" volume 1 #SFX-42
        scene blackscreen #BG-27
        show fire_pit at truecenter #SP-77
        with shake
        "Then you hear a rumble. The stone floor is sliding to one side. There is a pit of fire below. Soon you will fall into it!"
        "Quickly you take the pyramid from your bag. You jam one edge into the crack between the floor and the wall perhaps it will work as a wedge?"
        "With a groan and a creak the floor stops moving. Now you must escape."
        "Barkimedes spots a way out. He grabs a loose plank in the door with his jaws and pulls it free. You both crawl through the gap."
        hide fire_pit #SP-77

        "There are 366 days in a leap year. How many days in a normal year?"
        jump puzzle_27 #059
    
    #062
    label wrong_man:
        scene secret_chamber #BG-24
        with fade_slow

        play sound "loud_bark.mp3" volume 1 #SFX-15
        "You start to tell the man and woman to call the police, but Barkimedes barks fiercely. The man and the woman back into a corner."

        "Look again at the clues. The man who is standing has a missing button and a scar on his hand."
        "The pattern on his shoe matches the one in the flour. His accomplice, the cook, has a gap in her teeth!"

        jump puzzle_28 #060
    
    #063
    label criminals_catched:
        scene buglar_catched #BG-25

        "Now it is the criminals' turn to be tied up."
        "While you phone the police station and gather the stolen goods as evidence, the owner leads the butler and the cook into the Grand Hall and ties them to two chairs."
        play sound "dog_growl.mp3" volume 1 #SFX-46
        "Barkimedes growls at them angrily, they are too scared of him to try and escape!"
        "The owner smiles when he sees his belongings safe and sound."
        o "I can't thank you enough,"
        o "Some of these things have been in my family for generations, they are priceless to me."
        play sound "dog_woof.mp3" volume 1 #SFX-5
        "Barkimedes barks happily and wags his tail. You crouch down to pat him on the head."
        "You are not the only one to thank you couldn't have done it without Barkimedes."
        y "You may need a new butler and cook,"
        y "But you'll never need another dog!"
        $ end_session()
        $ renpy.notify("Uploading logs...")
        $ send_logs()
        "- The End -"

    call screen results
    stop music fadeout 0.5

    return