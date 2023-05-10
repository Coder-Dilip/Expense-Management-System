import datetime
from django.shortcuts import render, redirect,get_object_or_404
# Create your views here.
from .models import DailySavingPlan, DailyTrack, Report, SchoolBudget, SchoolForm, DailySaving,Automate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import uuid
from django.http import JsonResponse
from django.db.models import Sum
from frontend.models import School
import random

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
        bank_name=request.POST.get('bank_name')
        account_number=request.POST.get('account_number')

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
            vision_for_school=vision_for_school,
            bank_name=bank_name,
            account_number=account_number
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
     try:
        if School.objects.filter(user=request.user).exists():
            return render(request,'school/index.html')
        else:
            return redirect('/admin-dashboard')
     except:
        return redirect("/login")
     

def analytics(request):
    return render(request,'school/analytics.html')
    













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
    food_track=0
    if Automate.objects.filter(school_username=request.user.username).exists():
        sheet_obj=Automate.objects.get(school_username=request.user.username)
        food_track=10*random.randint(170, 220)
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
            return render(request,'school/daily_track.html',{'username':school_username,'img':str(school_data.image_file),'message':message,'food_track':food_track})

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
        return render(request,'school/daily_track.html',{'username':request.user.username,'img':str(school_data.image_file),'message':message,'food_track':food_track})
    





    school_data = SchoolForm.objects.get(username=request.user.username)
    return render(request,'school/daily_track.html',{'username':request.user.username,'img':str(school_data.image_file),'message':'','food_track':food_track})



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
    key_param = request.GET.get('key')  # Retrieve the value of the 'key' parameter
    current_user=request.user.username
    if key_param:
        current_user=key_param
    else:print("lol")
    # Retrieve the DailyTrack instances for the specified school
    daily_tracks = DailyTrack.objects.filter(school_username=current_user)

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

    letterss=['''Dear Ministry of Education of Nepal,

I hope this letter finds you well. As a representative of [School Name], I would like to bring to your attention the need for a change in the distribution of expenses for our school's budget.

Currently, the expenses are distributed among various categories, including food, health, school items, transportation, bills, clothes, sports, and extra-curricular activities. However, we have noticed that the current distribution is not serving our students' needs adequately.

We kindly request that the budget for each category be distributed as follows:

Food: 30%
Health: 10%
School Items: 10%
Transportation: 10%
Bills: 10%
Clothes: 10%
Sports: 10%
Extra-curricular: 10%
We believe that this revised distribution will enable us to better cater to our students' needs, ultimately leading to a more conducive learning environment. Additionally, we assure you that we will be diligent in managing these funds to ensure that they are allocated appropriately.

Thank you for considering our request. We appreciate your continued support in our efforts to provide quality education to our students.

Sincerely,

[Your Name]
[School Name]''','''Dear [Recipient],

I am writing to you today to request a change in the distribution of expenses for our school's budget. As you may know, [School Name] is one of the leading educational institutions in our region, and we are committed to providing the best possible education to our students.

Currently, the expenses in our budget are divided into several categories, including food, health, school items, transportation, bills, clothes, sports, and extra-curricular activities. While we appreciate the support provided by the Ministry of Education of Nepal, we have noticed that the current distribution of funds is not meeting the needs of our students.

Therefore, we would like to request that the budget for each category be distributed as follows:

Food: 35%
Health: 15%
School Items: 10%
Transportation: 10%
Bills: 10%
Clothes: 5%
Sports: 10%
Extra-curricular: 5%
We believe that this revised distribution will allow us to better serve our students and provide them with a more holistic education. We are committed to using these funds responsibly and ensuring that they are allocated appropriately.

Thank you for considering our request. We appreciate your support and partnership as we strive to provide the best possible education to our students.

Sincerely,

[Your Name]
[School Name]''','''Dear [Recipient],

I am writing to you on behalf of [School Name] to express our gratitude for the support that the Ministry of Education of Nepal has provided us in the past. We are grateful for the opportunity to provide quality education to our students, and we would like to propose some changes in the distribution of the budget for the upcoming academic year.

Currently, our budget is divided into several categories, including food, health, school items, transportation, bills, clothes, sports, and extra-curricular activities. We have identified some areas that need more attention, and we would like to request a revised budget allocation.

Our proposed revised allocation is as follows:

Food: 35%
Health: 15%
School Items: 10%
Transportation: 10%
Bills: 5%
Clothes: 5%
Sports: 15%
Extra-curricular: 15%
We believe that this revised allocation will help us to provide better facilities and programs to our students. With this allocation, we can increase the quality and quantity of food provided to our students, enhance health services in school, improve transportation, and support more extra-curricular activities.

We assure you that we will use the funds responsibly and ensure that they are allocated appropriately. We are committed to providing the best possible education to our students, and we believe that this revised budget allocation will help us achieve our goals.

Thank you for considering our proposal. We appreciate your continued support and partnership in our efforts to provide the best possible education to our students.

Sincerely,

[Your Name]
[School Name]''']





    letter = random.choice(letterss)
    return JsonResponse({'letter': letter})

def dummy_letter2(request):
    letters=['''Dear [Recipient],

I hope this letter finds you well. On behalf of [School Name], I am pleased to provide you with a report on the budget allocation for the past academic year.

We are grateful for the support that the Ministry of Education of Nepal has provided us in the past year. With your assistance, we were able to provide quality education and facilities to our students. We take great pride in informing you that we have been able to allocate the funds efficiently, and as a result, have made significant savings in each category.

Here is a breakdown of the savings made in each category:

Food: Rs. [Food Savings]
Health: Rs. [Health Savings]
School Items: Rs. [School Items Savings]
Transportation: Rs. [Transportation Savings]
Bills: Rs. [Bills Savings]
Clothes: Rs. [Clothes Savings]
Sports: Rs. [Sports Savings]
Extra-curricular: Rs. [Extra-curricular Savings]
We are pleased to inform you that we have been able to make savings of Rs. [Total Savings] in the past academic year. These savings will help us allocate the funds more efficiently and provide better facilities to our students in the upcoming academic year.

We would like to thank you once again for your support and look forward to continuing our partnership with the Ministry of Education of Nepal in providing quality education to our students.

Sincerely,

[Your Name]
[School Name]''','''Dear [Recipient],

I hope this letter finds you well. As the representative of [School Name], I am writing to provide you with a report on the school's budget allocation for the past academic year.

Firstly, I would like to thank the Ministry of Education of Nepal for their support in helping us provide quality education and facilities to our students. We have managed to allocate the funds efficiently and have made significant progress in our goal of providing the best possible education to our students.

Below is a breakdown of the spending and savings made in each category:

Food:
Total spending: Rs. [Food Spending]
Savings: Rs. [Food Savings]
Health:
Total spending: Rs. [Health Spending]
Savings: Rs. [Health Savings]
School Items:
Total spending: Rs. [School Items Spending]
Savings: Rs. [School Items Savings]
Transportation:
Total spending: Rs. [Transportation Spending]
Savings: Rs. [Transportation Savings]
Bills:
Total spending: Rs. [Bills Spending]
Savings: Rs. [Bills Savings]
Clothes:
Total spending: Rs. [Clothes Spending]
Savings: Rs. [Clothes Savings]
Sports:
Total spending: Rs. [Sports Spending]
Savings: Rs. [Sports Savings]
Extra-curricular:
Total spending: Rs. [Extra-curricular Spending]
Savings: Rs. [Extra-curricular Savings]
As you can see, we have managed to save Rs. [Total Savings] across all categories. These savings will allow us to allocate the funds more efficiently and provide better facilities to our students in the upcoming academic year.

We take great pride in our commitment to transparency and accountability, and we hope that this report provides you with an accurate and detailed overview of our budget allocation and spending. Thank you for your continued support, and we look forward to working with you to ensure that every student receives the best possible education.

Sincerely,

[Your Name]
[School Name]''','''Dear [Recipient],

I hope this letter finds you well. As the representative of [School Name], I am writing to provide you with an update on the school's budget allocation for the past academic year.

With the support of the Ministry of Education of Nepal, we have managed to allocate the funds efficiently and have made significant progress in our goal of providing the best possible education to our students. Below is a breakdown of what has been accomplished in each category:

Food:
We have ensured that all students receive nutritious meals during the school day, and we have also initiated a food waste reduction program to minimize food wastage.
Health:
We have invested in the health and wellbeing of our students by providing regular health checkups, health education programs, and first aid training for our staff.
School Items:
We have provided all necessary school items to our students, including books, stationery, and other educational resources. We have also upgraded our library and computer lab facilities to enhance our students' learning experience.
Transportation:
We have improved our transportation services by upgrading our school buses and hiring trained drivers to ensure the safety and comfort of our students during their daily commute.
Bills:
We have managed to reduce our bills by investing in energy-efficient appliances and implementing measures to conserve water and electricity.
Clothes:
We have provided uniforms to all students, and we have also launched a clothes donation drive to ensure that all students have access to clean and comfortable clothing.
Sports:
We have encouraged our students to participate in sports activities by organizing regular sports events and investing in sports equipment and facilities.
Extra-curricular:
We have provided our students with a wide range of extracurricular activities, including music, dance, and drama programs. We have also organized field trips and other outdoor activities to promote learning and personal growth.
We take great pride in our commitment to transparency and accountability, and we hope that this report provides you with an accurate and detailed overview of what we have accomplished with the allocated funds. Thank you for your continued support, and we look forward to working with you to ensure that every student receives the best possible education.

Sincerely,

[Your Name]
[School Name]''']
    letter = random.choice(letters)
    return JsonResponse({'letter': letter})






# i want you to write letter like this format: "Dear John,\n\n"
#         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
#         "Nulla efficitur volutpat ultrices. Maecenas ut felis at nisi sodales rutrum. "
#         "Morbi imperdiet nulla eu lectus maximus, eget tincidunt dolor pharetra. "
#         "In hac habitasse platea dictumst. Donec rutrum urna libero, ac euismod neque mollis a. "
#         "Donec et mauris lobortis, sodales augue id, sagittis enim. "
#         "Duis faucibus risus eu odio dictum, vel consequat dolor fermentum. "
#         "Sed vestibulum scelerisque tortor, a vehicula lectus. Sed quis hendrerit arcu.\n\n"
#         "Sincerely,\nJane Smith"
#     The letter should be about requesting for change in distribution of the expenses on food, health, school items, transportation, bills, clothes, sports, extra-curricular. letter is going to be written by school and going to be received by ministry of education of nepal. I am making school expense management system in which ministry of education of nepal is going to distribute budget to the schools. for each school it will divide  the budget into the above mentioned categories such as food, health in percentage. please write one letter template same as i give you. it should include those "\n" new line characters same way i have given you


from .models import Automate
import json
@csrf_exempt
def automate_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        school_username = data["school_username"]
        sheet_url = data["sheet_url"]

        # check if the Automate object already exists
        automate = Automate.objects.filter(school_username=school_username).first()

        if automate:
            # update the existing object
            automate.sheet_url = sheet_url
            automate.save()
        else:
            # create a new Automate object
            Automate.objects.create(school_username=school_username, sheet_url=sheet_url)

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method. Only POST requests are allowed."})



from decouple import config
def openAiLetter(request):
    import openai

    # Set up OpenAI API credentials
    openai.api_key =config('openapi')

    # Set up the GPT-3 model
    model_engine = "text-davinci-003"
    prompt = request.GET.get('message')
    temperature = 0.5
    max_tokens = 2000  # Increase this value to generate longer text
    # Generate text
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Display the generated text
    reply=response.choices[0].text
    dat={"reply":reply}
    return JsonResponse(dat)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def analytics_spending(request):
    import pandas as pd
    daily_tracks = DailyTrack.objects.filter(school_username=request.user.username)
    data = [{"food": daily_track.food,
             "school_items": daily_track.school_items,
             "health": daily_track.health,
             "transportation": daily_track.transportation,
             "clothes": daily_track.clothes,
             "bills": daily_track.bills,
             "sports": daily_track.sports,
             "extra_curricular": daily_track.extra_curricular,
             "notes": daily_track.notes,
             "current_date": daily_track.current_date,
             "school_username":daily_track.school_username
             } for daily_track in daily_tracks]
    data_values = [[daily_track[key] for key in daily_track] for daily_track in data]
    num_list = [[int(x) if isinstance(x, (float, int)) else 0 for x in sublist] for sublist in data_values]
    print(num_list)
    sum_averages=[]
    for el in num_list:
        sum_averages.append(sum(el))

    lst=sum_averages
    # find the maximum difference
    max_diff = max(lst) - min(lst)

    # predict 7 values
    for i in range(15):
        # get the last value of the original list
        last_val = lst[-1]
        
        # check if the last value is greater than the first value
        if last_val < lst[0]:
            # predict an increase in value
            predicted_val = last_val/2 + random.uniform(0, 1.5*max_diff)
        else:
            # predict a decrease in value
            predicted_val = abs(last_val/2 - random.uniform(0, 1.5*max_diff))
        
        # append the predicted value to the original list
        lst.append(predicted_val)
    print(str(lst))
    return JsonResponse({"data":str(lst)})
    
    # return JsonResponse(data, safe=False)





def api_message(request):
    daily_tracks = DailyTrack.objects.filter(school_username=request.user.username)
    data = [{"food": daily_track.food,
             "school_items": daily_track.school_items,
             "health": daily_track.health,
             "transportation": daily_track.transportation,
             "clothes": daily_track.clothes,
             "bills": daily_track.bills,
             "sports": daily_track.sports,
             "extra_curricular": daily_track.extra_curricular,
             "notes": daily_track.notes,
             "current_date": daily_track.current_date,
             "school_username":daily_track.school_username
             } for daily_track in daily_tracks]
    data_values = [[daily_track[key] for key in daily_track] for daily_track in data]
    num_list = [[int(x) if isinstance(x, (float, int)) else 0 for x in sublist] for sublist in data_values]
    query= '''the each element in this array is expenses on that day of a school In rupees.  The expenses is done in 8 different categories food, health, transportation, sports, extra curricular, school items, bills, uniform on each day. There are past three data and future 7 data in this array. What do you think how can we improve the savings by minimizing the spendings. The array looks like this:''' +str(num_list)+'''Please write shortly based on above data for each day corresponding to each category, Which categories are spending more and how can spending be minimized in those categories. Write as if you are a person who is guiding a school. write very very shortly  in bullet points by giving analytics and numeric data'''
    import openai

    # Set up OpenAI API credentials
    openai.api_key =config('openapi')

    # Set up the GPT-3 model
    model_engine = "text-davinci-003"
    prompt = query
    temperature = 0.5
    max_tokens = 2000  # Increase this value to generate longer text
    # Generate text
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Display the generated text
    reply=response.choices[0].text
    dat={"reply":reply}
    return JsonResponse(dat)


from django.db.models import Sum

def top_three_schools(request):
    schools = DailySaving.objects.values('school_username').annotate(total_savings=Sum('school_items') + Sum('food') + Sum('health') + Sum('transportation') + Sum('clothes') + Sum('bills') + Sum('sports') + Sum('extra_curricular')).order_by('-total_savings')[:5]

    school_data = []
    for school in schools:
        school_details = SchoolForm.objects.get(username=school['school_username'])
        school_data.append({
            'school_username': school['school_username'],
            'total_savings': school['total_savings'],
            'image_url': school_details.image_file.url,
            'schoolname': school_details.schoolname,
            'address': school_details.address,
        })

    return JsonResponse(school_data, safe=False)



def dashboard_api(request):
        daily_savings = DailySaving.objects.filter(school_username=request.user.username)
        daily_spendings=DailyTrack.objects.filter(school_username=request.user.username)
        budget=SchoolBudget.objects.get(school_username=request.user.username)
        school_form=SchoolForm.objects.get(username=request.user.username)
    
        total_spendings={
           'school_items': 0,
            'food': 0,
            'health': 0,
            'transportation': 0,
            'clothes': 0,
            'bills': 0,
            'sports': 0,
            'extra_curricular': 0 
        }
        budgets={
           'school_items': budget.school_items,
            'food': budget.food,
            'health':  budget.health,
            'transportation': budget.transportation,
            'clothes': budget.clothes,
            'bills': budget.bills,
            'sports': budget.sports,
            'extra_curricular': budget.extra_curricular 
        }
        total_savings = {
            'school_items': 0,
            'food': 0,
            'health': 0,
            'transportation': 0,
            'clothes': 0,
            'bills': 0,
            'sports': 0,
            'extra_curricular': 0,
        }
        for daily_saving in daily_savings:
            total_savings['school_items'] += daily_saving.school_items
            total_savings['food'] += daily_saving.food
            total_savings['health'] += daily_saving.health
            total_savings['transportation'] += daily_saving.transportation
            total_savings['clothes'] += daily_saving.clothes
            total_savings['bills'] += daily_saving.bills
            total_savings['sports'] += daily_saving.sports
            total_savings['extra_curricular'] += daily_saving.extra_curricular

        for daily_spending in daily_spendings:
            total_spendings['school_items'] += daily_spending.school_items
            total_spendings['food'] += daily_spending.food
            total_spendings['health'] += daily_spending.health
            total_spendings['transportation'] += daily_spending.transportation
            total_spendings['clothes'] += daily_spending.clothes
            total_spendings['bills'] += daily_spending.bills
            total_spendings['sports'] += daily_spending.sports
            total_spendings['extra_curricular'] += daily_spending.extra_curricular
        
        total_saving=sum(total_savings.values())
        total_savings['total_saving']=total_saving
        total_spending=sum(total_spendings.values())
        total_spendings['total_spending']=total_spending
        total_savings['spendings']=total_spendings
        budgets['total_budget']=sum(budgets.values())
        total_savings['budget']=budgets
        total_savings['image']=school_form.image_file.url
        return JsonResponse(total_savings, status=200)



def view_school(request, schoolusername):
    return render(request, 'school/view_school.html',{'school':schoolusername})