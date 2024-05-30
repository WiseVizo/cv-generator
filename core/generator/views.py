from django.shortcuts import render
from django.http import HttpResponse
from user_data.models import UserData
import http.client
import json
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
def generate_resume(request):
    
    conn = http.client.HTTPSConnection("infinite-gpt.p.rapidapi.com")

    # Prepare input data from UserData model
    user_data = UserData.objects.get(pk=1)  # Retrieve user data from database
    #request.session.get('user_id')
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

    request.session['resume_context'] = context  # Save context in session
    
   

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
    
    
    # headers = {
    # 'content-type': "application/json",
    # 'X-RapidAPI-Key': "3b4b1ebc4bmsh15df51970321d69p1a6d26jsnefe9b5671e2c",
    # 'X-RapidAPI-Host': "infinite-gpt.p.rapidapi.com"
    # }
    # headers = {
    # 'content-type': "application/json",
    # 'X-RapidAPI-Key': "683286cb91msh20a74ff72f0bfe3p115e79jsnd8ecb7821a08",
    # 'X-RapidAPI-Host': "infinite-gpt.p.rapidapi.com"
    # }
    headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "71ecdfa449msh04dab0161cf281fp169d2cjsncf6653b932a9",
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

def download_resume_as_pdf(request):
    context = request.session.get('resume_context')  # Load context from session
    if not context:
        return HttpResponse("Context not found in session", status=404)

    template = get_template('generator/cv.html')
    html_content = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume1.pdf"'

    # HTML(string=html_content).write_pdf(response)
    # config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    # pdfkit.from_string(html_content, response.content, configuration=config)
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF: %s' % pisa_status.err)
    return response