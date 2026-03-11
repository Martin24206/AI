class SceneAwarenessEngine:

    def describe_scene(self, scene):

        location = scene.get("location", "unknown place")

        descriptions = {
            "school_road": "a quiet road leading to school",
            "classroom": "a classroom filled with desks",
            "park": "a peaceful park with trees"
        }

        return descriptions.get(location, location)

    def characters_here(self, scene):

        return scene.get("characters_present", [])