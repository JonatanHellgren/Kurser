from subjects import subject
"""
Here is the digital assistant class, most of the program in implemented here.
It is used by first initalizing a digital assistant, then adding subject and
then it is ready to initalize an dialogue
"""


class digital_assistant():
    def __init__(self, name):
        self.name = name
        self.subjects = []
        self.replies = []
        self.current_place = None
        self.current_subject = None

    def add_subject(self, subject):
        self.subjects.append(subject)

    def initalize_dialogue(self):
        self.print_start_message()
        self.get_subject()
        self.validate_subject()
        self.get_place()
        self.validate_place()
        self.conversate()
        self.goodbye()

    """
    All relies are appended in a function to so that it is possible to add
    trigger as soon as a reply is saved, aswell as all the replies gets stored
    in the assistans memory. 
    """

    def append_reply(self, reply):
        self.replies.append(reply)
        if is_greeting(reply):
            print('Nice to meet you!')

        if self.current_place != None:
            # get answers about time
            if is_price_question(reply):
                priceclass = ['cheap', 'affordable', 'moderate', 'expensive']
                print(
                    f'{self.current_place.name} is in the {priceclass[self.current_place.price]} priceclass'
                )
            # get price class
            if is_time_question(reply):
                print(
                    f'{self.current_place.name} is open from {self.current_place.opening_time} until {self.current_place.closing_time}'
                )

    def print_start_message(self):
        print(f'Hi my name is {self.name}!')
        reply = input('What can I help you with?\n')
        self.append_reply(reply.split())

    def get_subject(self):
        possible_subjects, matching_words = self.find_subject()

        while possible_subjects == []:
            reply = self.get_new_reply()
            possible_subjects, matching_words = self.find_subject()

        while len(possible_subjects) > 1:
            possible_subjects = self.get_specification(possible_subjects,
                                                       matching_words)
        self.current_subject = possible_subjects[0]

    def find_subject(self):
        possible_subjects = []
        matching_words = []
        for subject in self.subjects:
            for tag in subject.tags:
                if tag in self.replies[-1]:
                    possible_subjects.append(subject)
                    matching_words.append(tag)
        return possible_subjects, matching_words

    def get_new_reply(self):
        reply = input(
            'Could you try that again and be a bit more specific, what can I help you with?\n'
        )
        self.append_reply(reply)

    def get_specification(self, possible_outcomes, matching_words):
        if len(matching_words) == 1:
            reply = input(f'Can you be more specific, what do you want to do\
            besides {matching_words}')
            self.append_reply(reply)

    def validate_subject(self):
        reply = input(f'So you are looking for {self.current_subject.name}?\n')
        self.replies.append(reply.split())
        if is_ending(self.replies[-1]):
            self.get_new_reply()
            self.get_subject()
            self.validate_subject()
        elif not is_affirmative(self.replies[-1]):
            print("Sorry, I didn't get that")
            self.validate_subject()

    def get_place(self):
        self.search_for_place()
        while self.current_place == None:
            self.specify_place()
            self.get_place()

    def search_for_place(self):
        for reply in self.replies[::-1]:
            for place in self.current_subject.places:
                for tag in place.tags:
                    if tag in reply:
                        self.tag = tag
                        self.current_place = place
                        break
                else:
                    continue
                break
            else:
                continue
            break

    def specify_place(self):
        reply = input(
            f'What kind of {self.current_subject.name} are you looking for?\n')
        self.append_reply(reply)

    def validate_place(self):
        self.describe_place()
        reply = input('Does that sound good?\n')
        self.append_reply(reply.split())
        if is_ending(self.replies[-1]):
            reply = input(
                f'What is it you are looking for besides {self.tag}?\n')
            self.append_reply(reply.split())
            self.get_place()
            self.validate_place()
        elif not is_affirmative(self.replies[-1]):
            print("Sorry I didn't get that.")
            self.validate_place()

    def describe_place(self):
        print(
            f'{self.current_place.name} is a {self.current_place.tags[0]} and {self.current_place.tags[1]} place'
        )

    def conversate(self):
        reply = input(
            f'Do you have any more questions about {self.current_place.name}?\n'
        )
        self.append_reply(reply.split())
        if not is_ending(self.replies[-1]):
            self.conversate()

    def goodbye(self):
        print('Have a nice day, thanks for the chat')


"""
Function used to look for certain tags i responses when the assistant is not
looking for tags that fill up frames. 
"""


def general_is(reply, tags):
    for word in reply:
        if word in tags:
            return True
    return False


def is_affirmative(reply):
    affirmative = [
        'Yes,', 'Yes', 'yes,', 'yes', 'correct', 'yeah', 'ok', 'sure'
    ]
    return general_is(reply, affirmative)


def is_ending(reply):
    tags = ['No', 'no', 'goodbye', 'Goodbye', 'bye', 'Bye']
    return general_is(reply, tags)


def is_greeting(reply):
    greetings = ['Hi', 'Hello', 'Howdy']
    return general_is(reply, greetings)


def is_price_question(reply):
    tags = ['cost', 'price', 'expensive', 'cheap']
    return general_is(reply, tags)


def is_time_question(reply):
    tags = ['open', 'close', 'time']
    return general_is(reply, tags)
