import datetime
from django.shortcuts import render, redirect,get_object_or_404
# Create your views here.
from .models import DailySavingPlan, DailyTrack, Report, SchoolBudget, SchoolForm, DailySaving
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import uuid
from django.http import JsonResponse
from django.db.models import Sum
from frontend.models import School

@login_required(login_url="/login/")
def school_form(request):
    if request.method == 'POST':

        # Get data from the form
        schoolname = request.POST.get('schoolname')
        username = request.POST.get('username')
        if SchoolForm.objects.filter(username=username).exists():
            print("already submitted")
            return redirect('/success?message=form already submitted!')
        
        email = request.POST.get('email')
        district = request.POST.get('district')
        state = request.POST.get('state')
        classrooms = request.POST.get('classrooms')
        laboratories = request.POST.get('laboratories')
        library = request.POST.get('library')
        computer_labs = request.POST.get('computer_labs')
        staff_rooms = request.POST.get('staff_rooms')
        students = request.POST.get('students')
        teachers = request.POST.get('teachers')
        administrative_staffs = request.POST.get('administrative_staffs')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pan=request.POST.get('pan')
        image_file=request.FILES['image_file']
        educational_background=request.POST.get('educational_background')
        years_of_experience=request.POST.get('years_of_experience')
        vision_for_school=request.POST.get('vision_for_school')

        if image_file:
            # generate unique filename using uuid and file extension
            unique_filename = str(uuid.uuid4()) + '.' + image_file.name.split('.')[-1]
            # save image to media folder with unique filename
            with open('media/images/' + unique_filename, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            # create ImageModel instance with the unique filename
            image_file='images/'+unique_filename

        contact_email = request.POST.get('contact_email')

        form_data = SchoolForm(
            schoolname=schoolname,
            image_file=image_file,
            username=username,
            email=email,
            pan=pan,
            district=district,
            state=state,
            classrooms=classrooms,
            laboratories=laboratories,
            library=library,
            computer_labs=computer_labs,
            staff_rooms=staff_rooms,
            students=students,
            teachers=teachers,
            administrative_staffs=administrative_staffs,
            name=name,
            address=address,
            phone=phone,
            contact_email=contact_email,
            status=0,
            educational_background=educational_background,
            years_of_experience=years_of_experience,
            vision_for_school=vision_for_school
        )
        form_data.save()

        return redirect('/success?message=form submitted successfully!')
    curr_username = request.user.username
    if SchoolForm.objects.filter(username=curr_username).exists():
            return redirect('/success?message=form already submitted! You will get Dashboard after verification')
    return render(request, 'school/school_form.html',{'data':curr_username})


def success(request):
    data = request.GET.get('data', None)
    return render(request, 'school/success.html',{'data':data})


def school_details(request, username):
    school = get_object_or_404(SchoolForm, username=username)
    return render(request, 'school/school_details.html', {'school': school})

def school_dashboard(request):
     if School.objects.filter(user=request.user).exists():
        return render(request,'school/index.html')

     return redirect("/admin-dashboard")
    













def view_image(request,username):
    school_data = SchoolForm.objects.get(username=username)
    return render(request, 'school/view_image.html', {'data': school_data})



def school_form_list(request):
     # Filter rows based on status value
    school_forms = SchoolForm.objects.filter(status=0)

    # Convert QuerySet to list of dictionaries
    data = {'schools': list(school_forms.values())}

    # Return JSON response
    return JsonResponse(data)

def daily_track(request):
    if not MonthlySavingPlan.objects.filter(school_username=request.user.username).exists():
        return redirect("/school-dashboard")
    if request.method == 'POST':
        school_username = request.POST.get('school_username')
        school_data = SchoolForm.objects.get(username=school_username)
        food = request.POST.get('food')
        school_items = request.POST.get('school_items')
        health = request.POST.get('health')
        transportation = request.POST.get('transportation')
        clothes = request.POST.get('clothes')
        bills = request.POST.get('bills')
        sports = request.POST.get('sports')
        extra_curricular = request.POST.get('extra_curricular')
        notes = request.POST.get('notes')
        current_date = request.POST.get('current_date')
        current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").strftime("%Y-%b-%d")
        existing_record = DailyTrack.objects.filter(current_date=current_date,school_username=school_username).first()
        if existing_record:
        # A record already exists on this day, so you can show an error message to the user
            message = "A record already exists for this day"
            return render(request,'school/daily_track.html',{'username':school_username,'img':str(school_data.image_file),'message':message})

        daily_track = DailyTrack(school_username=school_username, food=food, school_items=school_items, health=health, transportation=transportation, clothes=clothes, bills=bills, sports=sports, extra_curricular=extra_curricular, notes=notes, current_date=current_date)
        school_budget = get_object_or_404(SchoolBudget, school_username=school_username)

    # Modify the relevant fields
        school_budget.food -= int(food)
        school_budget.school_items -= int(school_items)
        school_budget.health -= int(health)
        school_budget.transportation -= int(transportation)
        school_budget.clothes -= int(clothes)
        school_budget.bills -= int(bills)
        school_budget.sports -= int(sports)
        school_budget.extra_curricular -= int(extra_curricular)

    # Save the changes
        school_budget.save()
        daily_track.save()


        #saving how much money has to be spent in that day (without saving)
        def expected_spending_data(request):
            budget = SchoolBudget.objects.filter(school_username=request.user.username).first()
            daily_saving_plan = DailySavingPlan.objects.filter(school_username=request.user.username).first()
            
            days_passed = (timezone.now().date() - budget.curr_date).days
            if days_passed==365:
                days_passed=1
            else:
                days_passed=365-days_passed    
            school_items = int(budget.school_items / days_passed)
            food = int(budget.food / days_passed)
            health = int(budget.health / days_passed)
            transportation = int(budget.transportation / days_passed)
            clothes = int(budget.clothes / days_passed)
            bills = int(budget.bills / days_passed)
            sports = int(budget.sports / days_passed)
            extra_curricular = int(budget.extra_curricular / days_passed)
            data={
                'school_username': budget.school_username,
                'school_items': school_items,
                'food': food,
                'health': health,
                'transportation': transportation,
                'clothes': clothes,
                'bills': bills,
                'sports': sports,
                'extra_curricular': extra_curricular,
                'distributed': budget.distributed,
                'curr_date': budget.curr_date
            }
            return data

        expected_data = expected_spending_data(request)
        saved_data = {
    'school_username': expected_data['school_username'],
    'school_items': int(expected_data['school_items']) - int(school_items),
    'food': int(expected_data['food']) - int(food),
    'health': int(expected_data['health']) - int(health),
    'transportation': int(expected_data['transportation']) - int(transportation),
    'clothes': int(expected_data['clothes']) - int(clothes),
    'bills': int(expected_data['bills']) - int(bills),
    'sports': int(expected_data['sports']) - int(sports),
    'extra_curricular': int(expected_data['extra_curricular']) - int(extra_curricular),
    'distributed': expected_data['distributed'],
    'curr_date': expected_data['curr_date']
}


        daily_saving = DailySaving.objects.create(
        school_username=saved_data['school_username'],
        school_items=saved_data['school_items'],
        food=saved_data['food'],
        health=saved_data['health'],
        transportation=saved_data['transportation'],
        clothes=saved_data['clothes'],
        bills=saved_data['bills'],
        sports=saved_data['sports'],
        extra_curricular=saved_data['extra_curricular']
    )
        daily_saving.save()

        message='Daily Data Saved Successfully'
        return render(request,'school/daily_track.html',{'username':request.user.username,'img':str(school_data.image_file),'message':message})
    





    school_data = SchoolForm.objects.get(username=request.user.username)
    return render(request,'school/daily_track.html',{'username':request.user.username,'img':str(school_data.image_file),'message':''})



def statistics(request,username):
    try:
        school_budget_data = SchoolBudget.objects.get(school_username=username)

        # Create a dictionary to store the data
        data = {
            'school_username': school_budget_data.school_username,
            'school_items': school_budget_data.school_items,
            'food': school_budget_data.food,
            'health': school_budget_data.health,
            'transportation': school_budget_data.transportation,
            'clothes': school_budget_data.clothes,
            'bills': school_budget_data.bills,
            'sports': school_budget_data.sports,
            'extra_curricular': school_budget_data.extra_curricular,
            'distributed': school_budget_data.distributed
        }

        data2 = {
            'school_items': school_budget_data.school_items,
            'food': school_budget_data.food,
            'health': school_budget_data.health,
            'transportation': school_budget_data.transportation,
            'clothes': school_budget_data.clothes,
            'bills': school_budget_data.bills,
            'sports': school_budget_data.sports,
            'extra_curricular': school_budget_data.extra_curricular
        }

        # Calculate the total budget
        total_budget = sum(data2.values())
        data['total']=total_budget
        data['data']=data
        # Pass the dictionary to the template

        return render(request,'school/stats.html',data)
    except:
        return redirect('/school-dashboard')
    
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MonthlySavingPlan

@csrf_exempt
def save_daily_saving_plan(request):
    if request.method == 'POST':
        data = request.POST.getlist('data[]')  # Get data from the POST request
        # Convert the data into the appropriate types
        print("lol",data)
        school_username = data[0]
        school_items = int(data[1])
        food = int(data[2])
        health = int(data[3])
        transportation = int(data[4])
        clothes = int(data[5])
        bills = int(data[6])
        sports = int(data[7])
        extra_curricular = int(data[8])
        status = bool(data[9])

        # Check if there is already data for the school_username
        if MonthlySavingPlan.objects.filter(school_username=school_username).exists():
            # Remove the previous data for the school_username
            MonthlySavingPlan.objects.filter(school_username=school_username).delete()
        if DailySavingPlan.objects.filter(school_username=school_username).exists():
            # Remove the previous data for the school_username
            DailySavingPlan.objects.filter(school_username=school_username).delete()
        # Create a new MonthlySavingPlan instance with the received data
        monthly_saving_plan = MonthlySavingPlan(school_username=school_username,
                                             school_items=school_items,
                                             food=food,
                                             health=health,
                                             transportation=transportation,
                                             clothes=clothes,
                                             bills=bills,
                                             sports=sports,
                                             extra_curricular=extra_curricular,
                                             status=status)
        daily_saving_plan = DailySavingPlan(school_username=school_username,
                                             school_items=school_items/30,
                                             food=food/30,
                                             health=health/30,
                                             transportation=transportation/30,
                                             clothes=clothes/30,
                                             bills=bills/30,
                                             sports=sports/30,
                                             extra_curricular=extra_curricular/30,
                                             )
        
        monthly_saving_plan.save()  # Save the instance to the database
        daily_saving_plan.save()
        return JsonResponse({'success': True})  # Return a success response
    else:
        return JsonResponse({'success': False})  # Return an error response
    

def spendings(request):
    return render(request, "school/spending.html")


def get_school_expenses(request):
    # Retrieve the DailyTrack instances for the specified school
    daily_tracks = DailyTrack.objects.filter(school_username=request.user.username)

    # Calculate the total expenses for each category
    total_food = sum(track.food for track in daily_tracks)
    total_school_items = sum(track.school_items for track in daily_tracks)
    total_health = sum(track.health for track in daily_tracks)
    total_transportation = sum(track.transportation for track in daily_tracks)
    total_clothes = sum(track.clothes for track in daily_tracks)
    total_bills = sum(track.bills for track in daily_tracks)
    total_sports = sum(track.sports for track in daily_tracks)
    total_extra_curricular = sum(track.extra_curricular for track in daily_tracks)

    # Create a JavaScript object with the category expenses
    expenses_obj = {
        "food": total_food,
        "school_items": total_school_items,
        "health": total_health,
        "transportation": total_transportation,
        "clothes": total_clothes,
        "bills": total_bills,
        "sports": total_sports,
        "extra_curricular": total_extra_curricular,
    }

    # Calculate the average expenses for each category
    num_tracks = len(daily_tracks)
    avg_food = total_food / num_tracks if num_tracks else 0
    avg_school_items = total_school_items / num_tracks if num_tracks else 0
    avg_health = total_health / num_tracks if num_tracks else 0
    avg_transportation = total_transportation / num_tracks if num_tracks else 0
    avg_clothes = total_clothes / num_tracks if num_tracks else 0
    avg_bills = total_bills / num_tracks if num_tracks else 0
    avg_sports = total_sports / num_tracks if num_tracks else 0
    avg_extra_curricular = total_extra_curricular / num_tracks if num_tracks else 0

    # Create a dictionary with the category average expenses
    expenses_dict = {
        "food": int(avg_food),
        "school_items": int(avg_school_items),
        "health": int(avg_health),
        "transportation": int(avg_transportation),
        "clothes": int(avg_clothes),
        "bills": int(avg_bills),
        "sports": int(avg_sports),
        "extra_curricular": int(avg_extra_curricular),
    }

    # Render the expenses data as a JSON response
    return JsonResponse(expenses_dict)

def get_school_saving_expenses(request):
    # Get the DailySavingPlan object(s) for the given school_username
    plans = DailySaving.objects.filter(school_username=request.user.username)
    
    # Calculate the averages for each field
    fields = ['school_items', 'food', 'health', 'transportation', 'clothes', 'bills', 'sports', 'extra_curricular']
    averages = {field: sum(getattr(plan, field) for plan in plans) / len(plans) for field in fields}
    
    # Create a dictionary with the desired keys and values
    expenses_dict = {
        "food": int(averages['food']),
        "school_items": int(averages['school_items']),
        "health": int(averages['health']),
        "transportation": int(averages['transportation']),
        "clothes": int(averages['clothes']),
        "bills": int(averages['bills']),
        "sports": int(averages['sports']),
        "extra_curricular": int(averages['extra_curricular']),
    }
    
    # Return the dictionary as a JSON response
    return JsonResponse(expenses_dict)


def expected_saving_api(request):
    # Get the DailySavingPlan object for the given school_username
    plan = get_object_or_404(DailySavingPlan, school_username=request.user.username)
    
    # Calculate the averages for each field
    fields = ['school_items', 'food', 'health', 'transportation', 'clothes', 'bills', 'sports', 'extra_curricular']
    averages = {field: getattr(plan, field) / 1 for field in fields}
    # averages = {field: getattr(plan, field) / len(fields) for field in fields}
    data=[]
    # Create a dictionary with the desired keys and values
    expenses_dict = {
        "food": int(averages['food']),
        "school_items": int(averages['school_items']),
        "health": int(averages['health']),
        "transportation": int(averages['transportation']),
        "clothes": int(averages['clothes']),
        "bills": int(averages['bills']),
        "sports": int(averages['sports']),
        "extra_curricular": int(averages['extra_curricular']),
    }
    data.append(expenses_dict)
    # Return the dictionary as a JSON response
    return JsonResponse(data,safe=False)


from django.utils import timezone
from django.http import JsonResponse
from .models import SchoolBudget

def expected_spending_api(request):
    data = []
    budget = SchoolBudget.objects.filter(school_username=request.user.username).first()
    daily_saving_plan = DailySavingPlan.objects.filter(school_username=request.user.username).first()

    # Extract the values for each category and store them in respective variables
    school_items_school=daily_saving_plan.school_items
    food_school = daily_saving_plan.food
    health_school = daily_saving_plan.health
    transportation_school = daily_saving_plan.transportation
    clothes_school = daily_saving_plan.clothes
    bills_school = daily_saving_plan.bills
    sports_school = daily_saving_plan.sports
    extra_curricular_school = daily_saving_plan.extra_curricular
    
    days_passed = (timezone.now().date() - budget.curr_date).days
    if days_passed==365:
        days_passed=1
    else:
        days_passed=365-days_passed    
    school_items = int(budget.school_items / days_passed)
    food = int(budget.food / days_passed)
    health = int(budget.health / days_passed)
    transportation = int(budget.transportation / days_passed)
    clothes = int(budget.clothes / days_passed)
    bills = int(budget.bills / days_passed)
    sports = int(budget.sports / days_passed)
    extra_curricular = int(budget.extra_curricular / days_passed)
    data.append({
        'school_username': budget.school_username,
        'school_items': school_items-school_items_school,
        'food': food-food_school,
        'health': health-health_school,
        'transportation': transportation-transportation_school,
        'clothes': clothes-clothes_school,
        'bills': bills-bills_school,
        'sports': sports-sports_school,
        'extra_curricular': extra_curricular-extra_curricular_school,
        'distributed': budget.distributed,
        'curr_date': budget.curr_date
    })
    
    return JsonResponse(data, safe=False)


def savings(request):
    return render(request, 'school/saving.html')

def reports(request):
    if request.method == 'POST':
        print("hello")
        school_username = request.user.username
        message = request.POST.get('message')
        message = message.replace('\n', '<br>')
        type_of_letter = request.POST.get('type_of_letter')
        report = Report(school_username=school_username, message=message, type_of_letter=type_of_letter)
        report.save()
        return render(request, 'school/reports.html',{"message":'Report Sent!'})
    return render(request, 'school/reports.html',{'message':''})

def automate(request):
    
    return render(request,'school/automate.html')


def dummy_letter(request):
    letter = (
        "Dear John,\n\n"
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Nulla efficitur volutpat ultrices. Maecenas ut felis at nisi sodales rutrum. "
        "Morbi imperdiet nulla eu lectus maximus, eget tincidunt dolor pharetra. "
        "In hac habitasse platea dictumst. Donec rutrum urna libero, ac euismod neque mollis a. "
        "Donec et mauris lobortis, sodales augue id, sagittis enim. "
        "Duis faucibus risus eu odio dictum, vel consequat dolor fermentum. "
        "Sed vestibulum scelerisque tortor, a vehicula lectus. Sed quis hendrerit arcu.\n\n"
        "Sincerely,\nJane Smith"
    )
    return JsonResponse({'letter': letter})

def dummy_letter2(request):
    letter = (
        "Dear Dilip,\n\n"
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Nulla efficitur volutpat ultrices. Maecenas ut felis at nisi sodales rutrum. "
        "Morbi imperdiet nulla eu lectus maximus, eget tincidunt dolor pharetra. "
        "In hac habitasse platea dictumst. Donec rutrum urna libero, ac euismod neque mollis a. "
        "Donec et mauris lobortis, sodales augue id, sagittis enim. "
        "Duis faucibus risus eu odio dictum, vel consequat dolor fermentum. "
        "Sed vestibulum scelerisque tortor, a vehicula lectus. Sed quis hendrerit arcu.\n\n"
        "Sincerely,\nJane Smith"
    )
    return JsonResponse({'letter': letter})



