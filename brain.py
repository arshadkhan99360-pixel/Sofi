import json
import os
import datetime
import ast
import operator


class SofiBrain:

    def __init__(self):
        self.memory_file = "memory.json"
        self.memory = self.load_memory()


    # ---------------- MEMORY SYSTEM ----------------

    def load_memory(self):

        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except:
                data = {}
        else:
            data = {}

        data.setdefault("name", "")
        data.setdefault("facts", {})
        data.setdefault("notes", [])
        data.setdefault("todo", [])

        self.save_memory(data)

        return data


    def save_memory(self, data=None):

        if data:
            self.memory = data

        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(
                self.memory,
                file,
                indent=4,
                ensure_ascii=False
            )


    # ---------------- SOFI BRAIN ----------------

    def think(self, command):

        text = command.lower().strip()


        # Greetings
        if text in ["hi", "hello", "hey"]:

            if self.memory["name"]:
                return f"Hello {self.memory['name']} 😊 How can I assist you?"

            return "Hello 😊 How can I assist you?"


        # Remember name
        if "my name is" in text:

            name = command.split("is", 1)[1].strip()

            self.memory["name"] = name

            self.save_memory()

            return f"Nice to meet you {name}. I will remember your name."


        # Learn facts
        if text.startswith("remember that"):

            fact = command.replace(
                "Remember that",
                ""
            ).replace(
                "remember that",
                ""
            ).strip()


            if " is " in fact.lower():

                parts = fact.split(" is ", 1)

                key = parts[0].strip().lower()
                value = parts[1].strip()

                self.memory["facts"][key] = value

            else:

                self.memory["facts"][
                    f"fact_{len(self.memory['facts'])+1}"
                ] = fact


            self.save_memory()

            return "Got it. I will remember that."


        # Search memory

        if "what is my" in text:

            question = text.replace(
                "what is my",
                ""
            ).strip()


            for key, value in self.memory["facts"].items():

                if question in key:

                    return f"Your {key} is {value}."


            return "I don't remember that yet."


        # Time

        if "time" in text:

            now = datetime.datetime.now()

            return now.strftime(
                "The time is %I:%M %p"
            )


        # Date

        if "date" in text:

            today = datetime.datetime.now()

            return today.strftime(
                "Today's date is %d %B %Y"
            )


        # Todo list

        if text.startswith("add") and "todo" in text:

            task = command.lower()

            task = task.replace(
                "add",
                ""
            )

            task = task.replace(
                "to my todo list",
                ""
            )

            task = task.strip()


            self.memory["todo"].append(task)

            self.save_memory()

            return f"I added {task} to your todo list."


        if "show my todo" in text:

            if len(self.memory["todo"]) == 0:

                return "Your todo list is empty."

            return "Your tasks: " + ", ".join(
                self.memory["todo"]
            )


        # Notes

        if text.startswith("take a note"):

            note = command.replace(
                "Take a note",
                ""
            ).replace(
                "take a note",
                ""
            ).strip(": ")


            self.memory["notes"].append(note)

            self.save_memory()

            return "Note saved."


        if "show my notes" in text:

            if not self.memory["notes"]:

                return "You have no notes."

            return "Your notes: " + ", ".join(
                self.memory["notes"]
            )


        # Calculator

        try:

            result = self.calculate(command)

            if result is not None:

                return f"The answer is {result}"

        except:

            pass


        # Teaching

        if text.startswith("teach:"):

            lesson = command.split(
                ":",
                1
            )[1].strip()


            self.memory["facts"][
                f"lesson_{len(self.memory['facts'])+1}"
            ] = lesson


            self.save_memory()

            return "Thank you. I learned something new."


        return "I am still learning."


    # ---------------- SAFE CALCULATOR ----------------

    def calculate(self, expression):

        operators = {

            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod

        }


        def solve(node):

            if isinstance(node, ast.Constant):

                return node.value


            if isinstance(node, ast.BinOp):

                return operators[type(node.op)](
                    solve(node.left),
                    solve(node.right)
                )


            raise ValueError


        tree = ast.parse(
            expression,
            mode="eval"
        )

        return solve(tree.body)



# ---------------- TEST MODE ----------------

if __name__ == "__main__":

    sofi = SofiBrain()

    print("🤖 Sofi v2.0 Brain Online")
    print("Type exit to close")

    while True:

        user = input("You: ")

        if user.lower() == "exit":

            print("Sofi: Goodbye Arshad 💙")
            break


        answer = sofi.think(user)

        print("Sofi:", answer)