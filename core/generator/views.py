from django.shortcuts import render
from django.http import HttpResponse
from user_data.models import UserData
import http.client
import json
# Create your views here.
def generate_resume(request):
    
    conn = http.client.HTTPSConnection("infinite-gpt.p.rapidapi.com")

    # Prepare input data from UserData model
    user_data = UserData.objects.get(pk=request.session.get('user_id'))  # Retrieve user data from database

    # Education 
    education_input_data = {
        "university": user_data.university_name,
        "major_field": user_data.major_field,
        "graduation_year": user_data.graduation_year, 
        "course_name": user_data.course_name,
        "gpa out of 5": user_data.gpa_out_of_5,
        "courses" : user_data.courses,
        "projects": user_data.projects,
        "achivements": user_data.educational_achivements,
    }

    # Compose prompt
    prompt = f"""Generate an education section of resume based on the following user data in 60 words or more:\n\n{education_input_data}\n"""

    edu_data = send_query_to_bot(conn, prompt)
   
    # skills set & expertise 
    skills_and_expertise_input = {
        "programming_languages": user_data.programming_languages,
        "frameworks": user_data.frameworks,
        "non-tech skills": user_data.non_tech_skills,
    }
    prompt = f"""Generate skills set & experties section of resume based on the following user data in 60 words or more:\n\n{skills_and_expertise_input}\n"""
    skill_data = send_query_to_bot(conn, prompt)

    work_data = None
    #work experience 
    if user_data.have_work_experience:
        work_experience_input = {
            "company name": user_data.company_name,
            "job title" : user_data.job_title,
            "number of months worked": user_data.months_worked,
            "achivements": user_data.achievements,
            "responsibilities": user_data.responsibilities,
            "skills utilizied": user_data.skills_utilized,
            "company location": user_data.location,
            "reason for leaving": user_data.reason_for_leaving,
        }
        if user_data.supervisor_name:
            work_experience_input["supervisor name"] = user_data.supervisor_name
            work_experience_input["supervisor contact"] = user_data.supervisor_contact
        prompt = f"""Generate work experience section of resume based on following user data in 60 words or more:\n\n{work_experience_input}"""
        work_data = send_query_to_bot(conn, prompt)
    try: 
        print(edu_data["msg"])
        print(skill_data["msg"])
        if work_data:
            print(work_data["msg"])
        
    except Exception as e:
        return HttpResponse("something went wrong :/ ")


    personal_details = {
        "full_name": user_data.full_name,
        "email_address": user_data.email_address,
        "phone_number": user_data.phone_number,
        "city": user_data.city,
        "state": user_data.state,
        "linkedin_link": user_data.linkedin_link
    }


    context = {
        "personal_details": personal_details,
        "edu_section": edu_data["msg"],
        "skills_section": skill_data["msg"],
    }
    
    if work_data:
        context["work_exp_section"] = work_data["msg"]


    
   

    return render(request, "generator/cv.html", context=context)


def send_query_to_bot(conn, prompt):
    
    # Define the dictionary
    payload_dict = {
        "query": prompt,
        "sysMsg": """You are an expert resume builder \n Guidelines:\n
    1. Use only the details provided.
    2. Do not add any new information or invent details.
    3. Do not include other sections like Certifications or Professional Development if its not provided.
    4. Keep the tone professional and suitable for a resume.
    5. try to extend on provided info without naming something irrelevent.
    6. Consider emphasizing how the courses and projects have contributed to the development of skills and why the individual would be a valuable asset to an organization. """
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
    return data