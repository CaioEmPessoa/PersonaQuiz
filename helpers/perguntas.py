import random
from helpers import last_user

class Questions():

    def favorite(self, topic):

        # What is your favorite xxx?
        print(f"What is {last_user.UserInfo.info_dict['nome']}'s favorite {topic}?")


        # Gets the first item of the list, it assumes that is the right answer
        right_answer = last_user.UserInfo.info_dict[topic][0]

        # Create a question list with the itens of the topic and shufles it
        question_list = last_user.UserInfo.info_dict[topic]
        random.shuffle(question_list)

        # Loops around the rnd list to print the possible answers
        # The first item is the location of the item in the rnd list +1 (to do not apper the 0)
        # The second item is just the name of the topic.
        # Couldn't print just the topic beacause it would show the answer
        for item in question_list:
            print(question_list.index(item)+1, item[1])

        while True:
            try:
                print("")
                answer = int(input(">> "))
                break
            except:
                print("Not valid answer. Please respond only with numbers!")


        # Checks if the answer is right
        if question_list[answer-1][0] == right_answer[0]:
            print("parabains")
        else:
            print("imbecil")

    def __init__(self):

        self.question_list = []
