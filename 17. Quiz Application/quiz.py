class quiz:
    question=""
    option_A=""
    option_B=""
    option_C=""
    option_D=""
    answer=""
    score=0

    def MCQ(self):
        ans=input("Enter Your Answer...").lower()
        if ans==self.option_A or ans==self.option_B or ans==self.option_C or ans==self.option_D:
            if ans==self.answer:
                quiz.score+=1
                print(f"Correct Answer!!! Your Current Score:- {quiz.score}/5")
            else:
                print(f"Wrong Answer!!! Your Current Score:- {quiz.score}/5")
        else:
            print("Invalid Answer..Type Your Transer Answer again")
            return self.MCQ()

    def oneword(self):
        ans=input("Enter Your Answer...").lower()
        if ans==self.answer:
            quiz.score+=1
            print(f"Correct Answer!!! Your Current Score:- {quiz.score}/5")
        else:
            print(f"Wrong Answer!!! Your Current Score:- {quiz.score}/5")

q1=quiz()
q1.question="What is the capital of India?"
q1.option_A="Gujarat"
q1.option_B="Bihar"
q1.option_C="Delhi"
q1.option_D="Mumbai"
q1.answer="Delhi".lower()

print(q1.question)
print(q1.option_A)
print(q1.option_B)
print(q1.option_C)
print(q1.option_D)

q1.MCQ()


q2=quiz()
q2.question="Who is the Prime Minister of India?"
q2.answer="Narendra Modi".lower()
print(q2.question)

q2.oneword()
q3=quiz()
q3.question="What is the capital of Gujarat?"
q3.option_A="Gandhinagar"
q3.option_B="Junagadh"
q3.option_C="Rajkot"
q3.option_D="Bhuj"
q3.answer="Gandhinagar".lower()
print(q3.question)
print(q3.option_A)
print(q3.option_B)
print(q3.option_C)
print(q3.option_D)

q3.MCQ()

q4=quiz()
q4.question="Which is national bird of India?"
q4.answer="Peacock".lower()
print(q4.question)
q4.oneword()

q5=quiz()
q5.question="Which is national animal of India?"
q5.answer="Lion".lower()
print(q5.question)
q5.oneword()

print(f"\nFinal Score: {quiz.score}/5")

