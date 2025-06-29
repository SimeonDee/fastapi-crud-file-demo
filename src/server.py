import os
from typing import List
from models import Student, StudentCreate, StudentGet, StudentUpdate
from fastapi import (
    FastAPI,
    Path,
    Form,
    UploadFile,
    File,
    HTTPException,
    status,
)

from fastapi.responses import FileResponse


# utility func to find a student location
def get_student_index(matric):
    found_student = None
    for student in students:
        if student.matric == matric:
            found_student = student
            break
    return students.index(found_student) if found_student else None


def get_student_by_username(username):
    found_student = None
    for student in students:
        if student.username == username:
            found_student = student
            break
    return found_student


students = []
PROFILE_PIX_DIR = os.path.join(os.path.dirname(__file__), "profile_pics")
ALLOWED_FILE_EXTENSIONS = ["jpg", "png", "jpeg"]

app = FastAPI()


# Health check
@app.get("/")
async def index():
    """API health check."""
    return {"health": "ok"}


# Create new student
@app.post("/students")
async def create_student(student: StudentCreate) -> StudentGet:
    """Create new student."""
    if student in students:
        return {"error": "404 - Not found"}
    existing_student = get_student_index(student.matric)
    if existing_student:
        return {
            "error": (
                "400 - Student with the matric "
                f"'{student.matric}' already exists"  # no-qa
            )
        }

    new_student = Student(
        username=student.username,
        password=student.password,
        matric=student.matric,
        name=student.name,
        age=student.age,
    )
    students.append(new_student)
    return new_student


# Get all  students
@app.get("/students", response_model=List[StudentGet])
async def get_students():
    """Get all  students."""
    return students


# Get a student
@app.get("/students/{id}")
async def get_student(
    id: str = Path(
        description="Student matric number or any identification number used.",
    ),
):
    """Get a student."""
    found_index = get_student_index(id)
    if not found_index:
        return {
            "error": f"404 - Not found. No student found with matric '{id}'",
        }
    return {"data": students[found_index]}


# Update a student record
@app.patch("/students/{id}")
async def update_student(id: str, student: StudentUpdate):
    """Update a student record."""
    found_index = get_student_index(id)
    if not found_index:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404 - Not found. No student found with matric '{id}'",
        )

    found_student = students[found_index]
    found_student.name = student.name if student.name else found_student.name
    found_student.matric = (
        student.matric if student.matric else found_student.matric
    )  # no-qa
    found_student.age = student.age if student.age else found_student.age

    students[found_index] = found_student

    return {"data": found_student}


# Delete a student
@app.delete("/students/{id}")
async def delete_student(id: str):
    """Delete a student."""
    found_index = get_student_index(id)
    if not found_index:
        return HTTPException
    del students[found_index]
    return {"data": f"Student '{id}' deleted."}


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    logged_in_user = get_student_by_username(username)
    print(logged_in_user)
    if not logged_in_user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    if logged_in_user.password == password:
        logged_in_user.password = None  # do not send password
        return logged_in_user
    else:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
        )


@app.post("/profile_pix/upload/{username}")
async def upload_profile_pix(username: str, file: UploadFile = File(...)):

    # retrieve student record
    found_student = get_student_by_username(username)
    if not found_student:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Username '{username}' not found.",
        )

    [filename, ext] = file.filename.split(".")

    # validate uploaded file is a supported type
    if ext not in ALLOWED_FILE_EXTENSIONS:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid File Type: "
                f"File must be any of {ALLOWED_FILE_EXTENSIONS}"  # no-qa
            ),
        )

    modified_filename = f"{filename}.jpg"
    save_path = os.path.join(PROFILE_PIX_DIR, modified_filename)

    try:
        with open(save_path, "wb") as f:
            f.write(await file.read())

        student_idx = students.index(found_student)
        students[student_idx].profile_pix = modified_filename
        return {"message": "Profile picture saved successfully."}

    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.__str__(),
        )


@app.get("/profile_pix/download/{username}")
async def download_profile_pix(username: str):
    # retrieve student record
    found_student = get_student_by_username(username)
    if not found_student:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Username '{username}' not found.",
        )

    if found_student.profile_pix:
        pics_path = os.path.join(PROFILE_PIX_DIR, found_student.profile_pix)
        if os.path.exists(pics_path):
            return FileResponse(
                path=pics_path,
                media_type="image/jpeg",
                filename=found_student.profile_pix,
            )
        else:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    f"File '{found_student.profile_pix}' "
                    "no longer on server."  # no-qa
                ),
            )
    else:
        return {"message": "sorry, No profile picture for this user yet."}
