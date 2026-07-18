from kivy.utils import platform
from kivy.clock import Clock


if platform == "android":

    from jnius import autoclass, PythonJavaClass, java_method


    class ActivityCallback(PythonJavaClass):

        __javainterfaces__ = [
            "android/app/Activity"
        ]

        def __init__(self, owner):
            super().__init__()
            self.owner = owner


        @java_method(
            "(IILandroid/content/Intent;)V"
        )
        def onActivityResult(
            self,
            requestCode,
            resultCode,
            intent
        ):

            if requestCode == 101:

                try:

                    results = intent.getStringArrayListExtra(
                        "android.speech.extra.RESULTS"
                    )

                    if results:

                        text = results.get(0)

                        Clock.schedule_once(
                            lambda dt:
                            self.owner.callback(text)
                        )

                except Exception as e:

                    print(
                        "Result error:",
                        e
                    )



class SofiSpeech:


    def __init__(self):

        self.callback = None
        self.ready = False
        self.listener = None


        try:

            if platform == "android":

                self.Intent = autoclass(
                    "android.content.Intent"
                )

                self.PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )

                self.listener = ActivityCallback(
                    self
                )

                self.ready = True

                print(
                    "Sofi Speech Bridge Ready"
                )


        except Exception as e:

            print(
                "Speech setup error:",
                e
            )



    def listen(self, callback):

        self.callback = callback


        if not self.ready:
            print("Speech unavailable")
            return


        try:

            intent = self.Intent(
                "android.speech.action.RECOGNIZE_SPEECH"
            )


            intent.putExtra(
                self.Intent.EXTRA_LANGUAGE_MODEL,
                "free_form"
            )


            intent.putExtra(
                self.Intent.EXTRA_PROMPT,
                "Speak to Sofi"
            )


            self.PythonActivity.mActivity.startActivityForResult(
                intent,
                101
            )


            print(
                "Listening..."
            )


        except Exception as e:

            print(
                "Listen error:",
                e
            )