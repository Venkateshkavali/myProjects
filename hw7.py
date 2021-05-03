    sql_statement = "select distinct Degree from Students ;"
    degrees=[]
    degrees=execute_sql_statement(sql_statement, conn)
    with conn1:
        for values in degrees:
            print(values)
            insert_degree(conn1, values)
    sql_statement = "select Exams from Students ;"
    
    exams=[]
    exams=execute_sql_statement(sql_statement, conn)
    list1=[]
    list2=[]
    list3=[]
    for i in exams:
        i=list(i)
        for j in i: 
            list1= j.split(',')
            list2.append(list1)
    for k in list2:
        for j in k:
            j=j.strip()
            if j not in list3:
                list3.append(j)
    exam=[]
    year=[]
    for v in list3:
        exam.append(v.split()[0])
        year.append(v.split()[1][1:5])
    for i in range(len(exam)):
        exam[i]=(exam[i],year[i])
#    print(exam)
    with conn1:
        for values in exam:
            insert_exams(conn1, values)
    sql_statement = "select StudentID,Name,Degree from Students ;"    
    students=[]
    list_id =[]
    list_names=[]
    first_name=[]
    last_name=[]
    degree=[]
    stu=[]
    students=execute_sql_statement(sql_statement, conn)
    for i in students:
        list_names.append(i[1])
        list_id.append(i[0])
        degree.append(i[2])
    #print(list_names)
    for i in list_names:
        first_name.append(i.split(',')[0])
        last_name.append(i.split(',')[1][1:])
    for i in range(len(list_id)):
        k=(list_id[i],first_name[i],last_name[i],degree[i])
        stu.append(k)
    with conn1:
        for values in stu:
            insert_students(conn1, values)
            
                conntest = create_connection('non_normalized.db')
    sql_statement = "select Scores from Students ;"
    scores=[]
    scores=execute_sql_statement(sql_statement, conntest)
    conn2 = create_connection('normalized.db')
    sql_statement = "select Exams from Students ;"
    exams=[]
    exam1=[]
    exams=execute_sql_statement(sql_statement, conntest)
    sql_statement = "select StudentID from Students ;"
    std_id=[]
    std_id=execute_sql_statement(sql_statement, conn2)
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    for i in exams:
        i=list(i)
        list1.append(i)
    ln = len(list1)
    for i in range(len(list1)):
        j=list1[i]
        for v in range(len(j)):
            k=(j[v].split()[0])
            list2.append(k)
    for i in scores:
        i=list(i)        
        k=i[0].split(',')
        list3.append(k)
    k=1;
    for i in list3:
        for j in range(len(i)):
            i[j]=i[j].strip()
            v = (k,list2[j],int(i[j]))
            list4.append(v)
        k=k+1
    #print(list4)
    with conn1:
        for values in exam:
            insert_studentexamscore(conn1, values)

    


    
