from fastapi import APIRouter

from routers.students import router as students_router
from routers.courses import router as courses_router
from routers.enrollments import router as enrollments_router
from routers.lessons import router as lessons_router

router = APIRouter(prefix='/v1')

router.include_router(students_router)
router.include_router(courses_router)
router.include_router(lessons_router)
router.include_router(enrollments_router)
