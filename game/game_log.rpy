define topic_names = {
    "cardinal_directions": _("Cardinal Directions"),
    "2d_shapes": _("2D Shapes"),
    "3d_shapes": _("3D Shapes"),
    "lines": _("Lines"),
    "nets": _("Nets"),
    "coordinates": _("Coordinates"),
    "circles": _("Circles"),
    "perimeter_area": _("Perimeter and Area"),
    "measurement": _("Measurement"),
    "angles": _("Angles"),
    "time": _("Time"),
}

default correct_count = 0
default wrong_count = 0
default puzzle_stats = {}
default quiz_log = []
default session_start = 0
default session_end = 0
default session_duration = 0
default puzzle_start_time = 0
default puzzle_log_page = 0
default inventory_open_count = 0
default notebook_open_count = 0
default item_use_logs = []
default state_history = []
default language_history = []

init python:
    import time

    def update_js_logs(status="In Progress"):
        import json
        
        current_language = _preferences.language or "default"
        if not store.language_history or store.language_history[-1]["language"] != current_language:
            current_duration = 0
            if store.session_start > 0:
                current_duration = round(time.time() - store.session_start, 2)
            store.language_history.append({
                "language": current_language,
                "timestamp": current_duration
            })

        total = store.correct_count + store.wrong_count
        accuracy = 0
        if total > 0:
            accuracy = round((store.correct_count / total) * 100)

        logs = []
        for puzzle_id, data in store.puzzle_stats.items():
            for entry in data["history"]:
                logs.append({
                    "puzzle": puzzle_id,
                    "topic": data["topic"],
                    "attempt": entry["attempt"],
                    "result": entry["result"],
                    "duration": entry["duration"]
                })

        current_duration = 0
        if store.session_start > 0:
            current_duration = round(time.time() - store.session_start, 2)

        payload = {
            "player_name": store.player_name,
            "player_age": store.player_age,
            "player_gender": store.player_gender,
            "correct": store.correct_count,
            "wrong": store.wrong_count,
            "accuracy": accuracy,
            "duration": current_duration,
            "inventory_open_count": store.inventory_open_count,
            "notebook_open_count": store.notebook_open_count,
            "item_use_logs": store.item_use_logs,
            "state_history": store.state_history,
            "language_history": store.language_history,
            "logs": logs,
            "status": status
        }

        payload_json = json.dumps(payload)
        
        if renpy.emscripten:
            try:
                renpy.emscripten.run_script("""
                    window.renpyGameLogs = JSON.parse('%s');
                """ % payload_json.replace("'", "\\'").replace("\n", "\\n").replace("\r", ""))
            except:
                pass

    def label_tracker(name, is_jump):
        if not name.startswith('_'):
            if not hasattr(store, 'state_history'):
                store.state_history = []
            store.state_history.append(name)
            update_js_logs("In Progress")

    config.label_callbacks.append(label_tracker)

    def start_session():
        store.session_start = time.time()
        store.correct_count = 0
        store.wrong_count = 0
        store.puzzle_stats = {}
        store.quiz_log = []
        store.session_end = 0
        store.session_duration = 0
        store.inventory_open_count = 0
        store.notebook_open_count = 0
        store.item_use_logs = []
        store.state_history = []
        store.language_history = []
        initial_lang = _preferences.language or "default"
        store.language_history.append({
            "language": initial_lang,
            "timestamp": 0.0
        })

        if renpy.emscripten:
            try:
                renpy.emscripten.run_script("""
                    if (!window.renpyUnloadListenerAdded) {
                        window.renpyUnloadListenerAdded = true;
                        window.addEventListener('pagehide', function() {
                            if (window.renpyGameLogs && window.renpyGameLogs.status === "In Progress") {
                                window.renpyGameLogs.status = "Dropped Off";
                                navigator.sendBeacon("%s", JSON.stringify(window.renpyGameLogs));
                            }
                        });
                    }
                """ % store.google_script)
            except:
                pass

        update_js_logs("In Progress")

    def end_session():
        store.session_end = time.time()
        store.session_duration = (store.session_end - store.session_start)
    
    def start_puzzle_timer():
        store.puzzle_start_time = time.time()

    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        minute_text = renpy.translate_string("minutes")
        second_text = renpy.translate_string("seconds")
        return "{} {} {} {}".format(
            minutes,
            minute_text,
            seconds,
            second_text
        )

    def log_item_use(clicked_item, needed_item):
        is_correct = (clicked_item == needed_item)
        store.item_use_logs.append({
            "needed": needed_item,
            "clicked": clicked_item,
            "result": "Correct" if is_correct else "Incorrect"
        })
        update_js_logs("In Progress")

    def log_answer(puzzle_id, topic_tag, is_correct):

        if store.puzzle_start_time <= 0:
            duration = 0.0
        else:
            duration = round(
                time.time() - store.puzzle_start_time,
                2
            )
            
            if duration < 0 or duration > 3600:
                duration = 0.0

        if puzzle_id not in store.puzzle_stats:
            store.puzzle_stats[puzzle_id] = {
                "topic": topic_tag,
                "correct": 0,
                "wrong": 0,
                "attempts": 0,
                "history": []
            }

        data = store.puzzle_stats[puzzle_id]
        data["attempts"] += 1

        if is_correct:
            store.correct_count += 1
            data["correct"] += 1
            result = "Correct"

        else:
            store.wrong_count += 1
            data["wrong"] += 1
            result = "Wrong"

        data["history"].append({
            "attempt": data["attempts"],
            "result": result,
            "duration": duration
        })
        update_js_logs("In Progress")

    def analyze_topics():
        topic_summary = {}

        # recap per topic
        for puzzle_id, data in store.puzzle_stats.items():
            topic = data["topic"]
            if topic not in topic_summary:
                topic_summary[topic] = {
                    "correct" : 0,
                    "wrong"   : 0,
                    "attempts": 0
                }
            topic_summary[topic]["correct"] += data["correct"]
            topic_summary[topic]["wrong"] += data["wrong"]
            topic_summary[topic]["attempts"] += data["attempts"]

        # default
        most_understood = "-"
        hardest_topic = "-"
        best_accuracy = -1
        best_correct = -1
        worst_accuracy = float("inf")
        worst_wrong = -1

        # analyze
        for topic, data in topic_summary.items():
            correct = data["correct"]
            wrong = data["wrong"]
            total = correct + wrong
            if total <= 0: continue
            accuracy = correct / float(total)

            # strongest topic
            if (
                accuracy > best_accuracy
                or (
                    accuracy == best_accuracy
                    and correct > best_correct
                )
            ):
                best_accuracy = accuracy
                best_correct = correct
                most_understood = topic

            # weakest topic
            if wrong > 0:

                if (accuracy < worst_accuracy
                    or (
                        accuracy == worst_accuracy and wrong > worst_wrong
                    )
                ):
                    worst_accuracy = accuracy
                    worst_wrong = wrong
                    hardest_topic = topic

        return (
            topic_summary,
            most_understood,
            hardest_topic
        )

screen results():
    
    on "show" action Function(renpy.force_autosave)

    zorder 500
    modal True
    add "#000000cc"

    $ summary, best_topic, hardest_topic = analyze_topics()
    $ total = correct_count + wrong_count

    if total > 0:
        $ accuracy = round((correct_count / total) * 100)
    else:
        $ accuracy = 0

    add "result_report":
        xalign 0.5
        yalign 0.5

    ## left page

    # player name
    text "[player_name]":
        xpos 340
        ypos 255
        size 32
        color "#222"
        font "fonts/SpecialElite.ttf"

    # player gender
    if player_gender == "boy":
        add "images/show/boy.png":
            xpos 620
            ypos 250
            xsize 40
            ysize 40

    elif player_gender == "girl":
        add "images/show/girl.png":
            xpos 620
            ypos 250
            xsize 40
            ysize 40

    # player age
    text "[player_age]":
        xpos 820
        ypos 255
        size 32
        color "#222"
        font "fonts/SpecialElite.ttf"

    # correct
    text "[correct_count]":
        xpos 300
        ypos 452
        size 55
        color "#222"
        font "fonts/SpecialElite.ttf"


    # wrong
    text "[wrong_count]":
        xpos 535
        ypos 452
        size 55
        color "#222"
        font "fonts/SpecialElite.ttf"


    # accuracy
    text "[accuracy]%":
        xpos 740
        ypos 452
        size 55
        color "#222"
        font "fonts/SpecialElite.ttf"

    # strongest topic
    text (topic_names[best_topic]
        if best_topic in topic_names
        else "-"):
        xpos 265
        ypos 644
        size 30
        color "#222"
        font "fonts/SpecialElite.ttf"

    # weakest topic
    text (topic_names[hardest_topic]
    if hardest_topic in topic_names
    else "-"):
        xpos 265
        ypos 800
        size 30
        color "#222"
        font "fonts/SpecialElite.ttf"

    # session time
    text "[format_time(session_duration)]":
        xpos 265
        ypos 953
        size 30
        color "#222"
        font "fonts/SpecialElite.ttf"


    ## right page breakdown

    $ start_y = 335
    $ line_height = 59

    $ topic_order = [
        "cardinal_directions",
        "2d_shapes",
        "3d_shapes",
        "lines",
        "nets",
        "coordinates",
        "circles",
        "perimeter_area",
        "measurement",
        "angles",
        "time"
    ]

    for material in topic_order:
        if material in summary:
            $ data = summary[material]
        else:
            $ data = {
                "correct": "-",
                "wrong": "-",
            }

        if data["correct"] != "-":
            $ total_material = (data["correct"] + data["wrong"])

            if total_material > 0:
                $ material_accuracy = str(
                    round((data["correct"] / total_material) * 100)
                ) + "%"

            else:
                $ material_accuracy = "-"

        else:
            $ material_accuracy = "-"

        # correct
        text "[data['correct']]":
            xpos 1350
            ypos start_y
            size 24
            color "#222"
            font "fonts/SpecialElite.ttf"

        # wrong
        text "[data['wrong']]":
            xpos 1470
            ypos start_y
            size 24
            color "#222"
            font "fonts/SpecialElite.ttf"

        # rate
        text "[material_accuracy]":
            xpos 1580
            ypos start_y
            size 24
            color "#222"
            font "fonts/SpecialElite.ttf"

        $ start_y += line_height

    # continue
    textbutton _("Continue"):
        xpos 1275
        ypos 980
        xsize 200
        ysize 50
        text_size 32
        text_xalign 0.5
        text_yalign 0.5
        background "#000000"
        hover_background "#474747"
        text_color "#f5e6c8"
        action Return()