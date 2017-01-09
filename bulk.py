#The function accepts an ajax request(an array including assigned tasks). It the uses viewflow built in functions get_activation_from_task_id to activate the particular tasks sent through ajax and assign_form_activation function to activate the particular tasks

def bulk_task_assignment_view(request):
    taskArr = []
    if request.method == 'POST':
        for obj in request.POST.getlist('assigned_tasks[]'):
            entry = EntryTable.objects.get(reference=obj)
            process = ProcessTable.objects.get(application=entry)
            try:
                #If one task fails all are not assigned
                task = Task.objects.filter(process=process).get(status="NEW")
                taskArr.append(task)
            except:
                del taskArr[:]

        if len(taskArr) == 0:
            return HttpResponse(json.dumps({'msg': "Task(s) have already been assigned. Select appropriate tasks to assign"}), content_type="application/json")
        else:
            for task in taskArr:
                activation = get_activation_from_task_id(task.id)
                assign_form_activation(request, activation, entry, request.POST.get('assigned_to'), 
                    request.POST.get('supervisor'))
            return HttpResponse(json.dumps({'msg': "Tasks assigned successfully"}), content_type="application/json")
