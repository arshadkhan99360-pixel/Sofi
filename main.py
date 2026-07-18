print("1. Main started")

from kivymd.app import MDApp
print("2. KivyMD loaded")

from kivy.clock import Clock
print("3. Clock loaded")

from kivy.utils import platform
print("4. Platform loaded")

from brain import SofiBrain
print("5. Brain loaded")

from gui import SofiGUI
print("6. GUI loaded")


class SofiApp(MDApp):

    def build(self):

        print("7. Building Sofi...")

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"


        self.brain = SofiBrain()

        print("8. Brain created")


        self.gui = SofiGUI(
            brain=self.brain
        )

        print("9. GUI created")


        # Connect app reference
        self.gui.app = self


        # Start services after loading
        Clock.schedule_once(
            self.start_services,
            1
        )


        return self.gui



    def start_services(self, dt):

        print("10. Sofi services started")



    def on_activity_result(
        self,
        requestCode,
        resultCode,
        data
    ):

        if requestCode == 101:

            try:

                results = data.getStringArrayListExtra(
                    "android.speech.extra.RESULTS"
                )


                if results:

                    text = results.get(0)

                    print(
                        "Heard:",
                        text
                    )


                    self.gui.process_voice(
                        text
                    )


            except Exception as e:

                print(
                    "Speech result error:",
                    e
                )



if __name__ == "__main__":

    print("11. Starting app...")

    SofiApp().run()