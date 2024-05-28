from django.shortcuts import render
from django.http import HttpResponse
from user_data.models import UserData
import http.client
import json
# Create your views here.
def generate_resume(request):
    
    conn = http.client.HTTPSConnection("infinite-gpt.p.rapidapi.com")

    # Prepare input data from UserData model
    user_data = UserData.objects.get(pk=1)  # Retrieve user data from database

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
    try: 
        print(edu_data["msg"])
        print(skill_data["msg"])
        
    except Exception as e:
        return HttpResponse("something went wrong :/ ")
    context = {
        "edu_section": edu_data["msg"],
        "skills_section": skill_data["msg"],
    }


    
   

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
    'X-RapidAPI-Key': "683286cb91msh20a74ff72f0bfe3p115e79jsnd8ecb7821a08",
    'X-RapidAPI-Host': "infinite-gpt.p.rapidapi.com"
    }

    # Send request 
    conn.request("POST", "/infinite-gpt", payload, headers)

    # Process response
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    return data