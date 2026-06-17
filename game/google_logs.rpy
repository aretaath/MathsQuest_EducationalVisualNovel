init python:

    import json

    google_script = ("https://script.google.com/macros/s/AKfycbzMMpOoQORMRMQjyHLtpYAz9AQ1jjGOKhEwFS5XAD6ZVfFWbvi3cfOMme1uFBG-2tn1BA/exec")

    def send_logs():
        update_js_logs("Completed")
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

        payload = {
            "player_name": store.player_name,
            "player_age": store.player_age,
            "player_gender": store.player_gender,
            "correct": store.correct_count,
            "wrong": store.wrong_count,
            "accuracy": accuracy,
            "duration": store.session_duration,
            "inventory_open_count": store.inventory_open_count,
            "notebook_open_count": store.notebook_open_count,
            "item_use_logs": store.item_use_logs,
            "state_history": store.state_history,
            "language_history": store.language_history,
            "status": "Completed",
            "logs": logs
        }

        payload_json = json.dumps(payload)

        if renpy.emscripten:
            renpy.emscripten.run_script("""
                fetch("%s", {
                    method: "POST",
                    headers: {"Content-Type": "text/plain"},
                    body: '%s'
                });
            """ % (
                google_script,
                payload_json.replace("'", "\\'")
            ))