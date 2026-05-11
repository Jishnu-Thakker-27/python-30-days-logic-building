# Work In Progress!!!

count_name=0
count_department=0
count_batch=0
count_roll=0
count_city=0
index=empty

for row in data:
    row_items=row.strip().split(",")
    for index,item in enumerate(row_items):
        if len(item.strip())==0:
            if index==0:
                count_name+=1
            elif index==1:
                count_roll+=1
            elif index==2:
                count_department+=1
            elif index==3:
                count_batch+=1
            elif index==4:
                count_city+=1
                
print("Missing indexs: \n")
print("Total: ",total_count)
print()
if count_name!=0:
    print("Name: ",count_name)
    print()
else:
    pass
if count_roll!=0:
    print("Roll Number: ",count_roll)
    print()
else:
    pass
if count_department!=0:
    print("Department: ",count_department)
    print()
else:
    pass
if count_batch!=0:
    print("Batch: ",count_batch)
    print()
else:
    pass
if count_city!=0:
    print("City: ",count_city)
    print()
else:
    pass
