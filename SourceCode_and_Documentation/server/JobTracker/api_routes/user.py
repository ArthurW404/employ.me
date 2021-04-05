"""
Routes for fetching job postings
"""
from os.path import isfile
import requests
import json
from JobTracker.utils.debug import pretty_print_dict
from flask import (
    send_file,
    Blueprint,
    render_template,
    request,
    jsonify
)
from JobTracker.database_ops import (
    get_boards,
    create_board,
    set_user_resume_fields,
    get_board
)
from JobTracker.exceptions import InvalidUserInput
from JobTracker.utils.colourisation import printColoured
from flask_restx import Resource, Api, fields

RESUME_DIR_PATH = "JobTracker/static/resumes"

user_router = Blueprint("user", __name__)
user_api = Api(
    user_router, 
    doc="/doc",
    title="User Job Profile",
    description="Routes for managing the user's job profile and settings",
    default="/api/user",
    default_label="User job profile management",
)

# Data model definitions
user_fields = user_api.model("User", {
    "username": fields.String(description="Username"),
})

# RESTful route handlers:
@user_api.route('/')
class UserJobProfile(Resource):
    # @user_api.doc(
    #     description="Get a user's profile information",
    #     params={
    #         "id": "User's ID",
    #         "token": "JWT token"
    #     }
    # )
    # @user_api.marshal_with(user_fields)
    def get(self):
        """
            TODO
        """

@user_api.route('/boards')
class UserBoardManagement(Resource):
    def get(self):
        """
            Retrieves a list of the user's boards        
            Parameters:
                - user_id
        """
        printColoured(" * Retrieving all boards for a user", colour="yellow")
        user_id = request.args.get("user_id")
        boards = get_boards(user_id)
        return boards
    
    def post(self):
        """
            Parameters:
                - user_id
                - name
                - description
        """
        printColoured(" * Creating a new board", colour="yellow")
        request_params = dict(request.form)
        user_id = request_params["user_id"]
        name = request_params["name"]
        description = request_params["description"]
        board_id = create_board(user_id, name, description)
        return {
            "board_id": board_id
        }

@user_api.route("/board")
class UserBoard(Resource):
    def get(self):
        """
            Retrieves a specific board
            Parameters: 
                - user_id
                - board_id
        """
        printColoured(" * Retrieving specific board", colour="yellow")
        request_params = dict(request.args)
        user_id = request_params["user_id"]
        board_id = request_params["board_id"]
        board = get_board(user_id, board_id)
        return board

@user_api.route("/resume")
class UserResume(Resource):
    def get(self):
        """
            Retrieves the user's resume, if it exists, and sends it back
        """        
        printColoured(" * Retrieving resume pdf", colour="yellow")
        request_params = dict(request.args)
        try:
            user_id = request_params["user_id"]
            resume = send_file("static/resumes/{}.pdf".format(user_id))
            return resume
        except Exception as err:
            raise InvalidUserInput(description="Failed to send resume: {}".format(err))

    def post(self):
        """
            Receives the user's uploaded pdf and stores it locally on the file system
        """
        request_params = dict(request.form)
        # return user_id
        printColoured(" * Uploading resume pdf", colour="yellow")
        pretty_print_dict(request_params)
        # user_id = json.loads(request_params["data"])["user_id"]
        user_id = request_params["user_id"]
        # printColoured(request_params["resume"], colour="yellow")
        printColoured(request.files["resume"], colour="yellow")
        # path = "{}/{}.pdf".format(RESUME_DIR_PATH, user_id)
        # file = open(path, "wb")
        # file.write(bytearray(request_params["resume"], "utf-8"))
        # file.close()
        # request_params["resume"].save()
        request.files["resume"].save("{}/{}.pdf".format(RESUME_DIR_PATH, user_id))
        return "Saved"

@user_api.route("/parse_resume")
class UserResumeParser(Resource):
    def post(self):
        """
            Parses the resume of the user with the given ID. Stores the extracted fields 
            under the user document
        """
        printColoured(" * Parsing resume")
        request_params = dict(request.form)
        user_id = request_params["user_id"]

        path_to_resume = "{}/{}.pdf".format(RESUME_DIR_PATH, user_id)
        
        # If the file exists, proceed with resume parser API call
        if isfile(path_to_resume):
            BASE_URL = "https://seng2021-at3k.netlify.app"    # TODO: Shouldn't be hardcoded. 
            try:
                resume_url = "{}/api/user/resume?user_id={}".format(BASE_URL, user_id)
                return jsonify(parse_resume(user_id, resume_url))
            except Exception as err:
                raise err
        else:
            raise InvalidUserInput(description="You have not uploaded a resume to be parsed yet")

def parse_resume(user_id: str, resume_url: str) -> dict:
    """

    """
    url = "https://api.promptapi.com/resume_parser/url?url={}".format(resume_url)
    payload = {}
    headers= {
        "apikey": "F3RgNKjRAEXU1LoJh574J2RPwtxVKIrn"
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    # status_code = response.status_code
    result = response.text
    set_user_resume_fields(user_id, result)
    return result


"""
TODO: Delete this. This is just for reference:
Return value:
{
  "education": [
    {
      "dates": "2020",
      "name": "School of Engineering"
    },
    {
      "name": "University of New South Wales"
    },
    {
      "dates": "2019",
      "name": "Faculty of Engineering Dean\u2019s Award"
    }
  ],
  "email": "admin@timz.dev",
  "experience": [
    {
      "organization": "University of New South Wales",
      "title": "Academic Tutor"
    },
    {
      "organization": "Computer Science & Engineering Society",
      "title": "Team Lead"
    }
  ],
  "name": "Tim Zhang",
  "phone": "493-045-119",
  "skills": [
    "Shell",
    "Api",
    "Github",
    "Python",
    "Javascript",
    "C",
    "Postgresql",
    "Ui",
    "Pytorch",
    "Engineering",
    "Scripting",
    "Apis",
    "Algorithms",
    "Perl",
    "Flask",
    "C++",
    "Java",
    "Ruby",
    "C#"
  ]
}

"""

