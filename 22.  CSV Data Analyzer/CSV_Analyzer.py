print("CSV Analyzer")

with open("file.csv") as f:
    data=f.readlines()
print(data)
rows=len(data)-1
columns=len(data[0].strip().split(","))

print("Rows: ",rows)
print("Columns: ",columns)

total_count=0

for row in data[1:]:
    row_item=row.strip().split(",")
    for empty in row_item:
        if len(empty.strip())==0:
            total_count+=1


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
                
print("Missing values: ")
if count_name!=0:
    print(" Name: ",count_name)
    
else:
    pass
if count_roll!=0:
    print(" Roll Number: ",count_roll)
    
else:
    pass
if count_department!=0:
    print(" Department: ",count_department)

else:
    pass
if count_batch!=0:
    print(" Batch: ",count_batch)

else:
    pass
if count_city!=0:
    print(" City: ",count_city)

else:
    pass

print(" Total: ",total_count)

        
e=set()

for info in data[1:]:
    e.add(info.strip())
    
    
duplicate_rows=len(data[1:])-len(e)
print("Duplicate Rows: ",duplicate_rows)
