# Sofi v2.0 Android Voice Bridge
# Microphone test module


from kivy.utils import platform


class AndroidVoice:

    def __init__(self):

        self.ready = False

        try:

            if platform == "android":

                from jnius import autoclass

                self.Intent = autoclass(
                    "android.content.Intent"
                )

                self.PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )

                self.ready = True

                print("Android Voice Bridge Ready")

            else:

                print("Not running on Android")

        except Exception as e:

            print("Bridge Error:", e)



    def test(self):

        if self.ready:

            print(
                "Android microphone bridge loaded"
            )

        else:

            print(
                "Android voice bridge unavailable"
            )