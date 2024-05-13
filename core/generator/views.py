from django.shortcuts import render
from user_data.models import UserData
import http.client
import json
# Create your views here.
def generate_resume(request):
    
    conn = http.client.HTTPSConnection("infinite-gpt.p.rapidapi.com")

    # Prepare input data from UserData model
    user_data = UserData.objects.get(pk=1)  # Retrieve user data from database
    input_data = {
    "full_name": user_data.full_name,
    "email_address": user_data.email_address,
    "phone_number": user_data.phone_number,
    "city": user_data.city,
    "state": user_data.state,
    "linkedin_link": user_data.linkedin_link,
    "highest_education_lvl": user_data.highest_education_lvl,
    "major_field": user_data.major_field,
    "graduation_year": user_data.graduation_year,
    "achievements": user_data.achivements,
    "programming_languages": user_data.programming_languages,
    "frameworks": user_data.frameworks,
    "non_tech_skills": user_data.non_tech_skills,
    "professional_qualifications": user_data.professional_qualifications,
    "target_role": user_data.target_role,
    "career_goals": user_data.carrer_goals,
    }

    if user_data.have_work_experience:
        input_data["company_name"] = user_data.company_name
        input_data["job_title"] = user_data.job_title
        input_data["date_joined"] = user_data.date_joined
        input_data["date_quit"] = user_data.date_quit


    
    
    
    # Compose prompt
    prompt = f"Generate a resume based on the following user data:\n\n{input_data}\n"

    # Define the dictionary
    payload_dict = {
        "query": prompt,
        "sysMsg": "You are an expert resume builder."
    }

    # Convert the dictionary to a JSON string
    payload = json.dumps(payload_dict)
    
    headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "3b4b1ebc4bmsh15df51970321d69p1a6d26jsnefe9b5671e2c",
    'X-RapidAPI-Host': "infinite-gpt.p.rapidapi.com"
    }

    # Send request 
    conn.request("POST", "/infinite-gpt", payload, headers)
    # Process response
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    print(data)
    return render(request, "generator/cv.html", {"cv" : data})

