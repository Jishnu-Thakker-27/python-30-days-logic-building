while True:
    paragraph=input("Write A Paragraph.")
    words=paragraph.split()
    print(len(words))
    Next=int(input("Want To Write another paragraph?\nType 1 for Yes and 0 for No." ))
    if Next==1:
        continue
    elif Next==0:
        break
    if not(Next==1) and not(Next==0):
        print("Invalid Input.")
