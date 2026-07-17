"""
Seed database with initial data matching the frontend mock data.

Usage:
    python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.learning.models import (
    Category, Module, Lesson, InterviewQuestion,
    Quiz, QuizQuestion,
)
from apps.coding.models import Challenge, TestCase
from apps.dashboard.models import UserProgress, Activity, Roadmap

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with InterviewPrep data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # ── Create admin user ──
        admin, _ = User.objects.get_or_create(
            email="admin@interviewprep.com",
            defaults={
                "username": "admin",
                "first_name": "Alex",
                "last_name": "Chen",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("admin123")
        admin.save()
        self.stdout.write(f"  Admin: admin@interviewprep.com / admin123")

        # ── Create demo user ──
        demo, _ = User.objects.get_or_create(
            email="demo@interviewprep.com",
            defaults={
                "username": "demo",
                "first_name": "Demo",
                "last_name": "User",
                "role": "student",
            },
        )
        demo.set_password("demo123")
        demo.save()
        self.stdout.write(f"  Demo: demo@interviewprep.com / demo123")

        # ── Categories ──
        categories_data = [
            {"name": "Python Core", "slug": "python-core", "description": "Master the fundamental principles of Python, from basic syntax and data types to advanced decorators and memory management.", "icon": "code", "order": 1},
            {"name": "OOP", "slug": "oop", "description": "Object-Oriented Programming in Python.", "icon": "account_tree", "order": 2},
            {"name": "Django", "slug": "django", "description": "Django web framework mastery.", "icon": "layers", "order": 3},
            {"name": "DRF", "slug": "drf", "description": "Django REST Framework for APIs.", "icon": "api", "order": 4},
            {"name": "SQL", "slug": "sql", "description": "Structured Query Language fundamentals.", "icon": "database", "order": 5},
            {"name": "PostgreSQL", "slug": "postgresql", "description": "Advanced PostgreSQL features.", "icon": "storage", "order": 6},
            {"name": "FastAPI", "slug": "fastapi", "description": "FastAPI modern Python web framework.", "icon": "bolt", "order": 7},
            {"name": "Git", "slug": "git", "description": "Version control with Git.", "icon": "terminal", "order": 8},
            {"name": "Linux", "slug": "linux", "description": "Linux system administration.", "icon": "laptop_chromebook", "order": 9},
            {"name": "Docker", "slug": "docker", "description": "Containerization with Docker.", "icon": "dock", "order": 10},
            {"name": "Algorithms", "slug": "algorithms", "description": "Data structures and algorithms.", "icon": "architecture", "order": 11},
        ]
        cats = {}
        for c in categories_data:
            cat, _ = Category.objects.get_or_create(slug=c["slug"], defaults=c)
            cats[c["slug"]] = cat
        self.stdout.write(f"  Categories: {len(cats)}")

        # ── Python Core Modules ──
        pc = cats["python-core"]
        modules_data = [
            {"name": "Variables & Data Types", "description": "Mutables vs Immutables, Type Hinting, Scope", "order": 1},
            {"name": "Control Flow", "description": "Iterators, Generators, Context Managers", "order": 2},
            {"name": "Functions", "description": "Args & Kwargs, Lambda, First-class objects", "order": 3},
            {"name": "Decorators", "description": "Wrappers, Closure, Memoization", "order": 4},
            {"name": "List Comprehensions", "description": "Efficiency, Dictionary Comprehension, Nested loops", "order": 5},
        ]
        modules = {}
        for m in modules_data:
            mod, _ = Module.objects.get_or_create(
                category=pc, name=m["name"], defaults=m
            )
            modules[m["name"]] = mod
        self.stdout.write(f"  Modules: {len(modules)}")

        # ── Lessons ──
        lessons_data = [
            ("Variables & Data Types", "Memory Management", "beginner", 12, 1),
            ("Variables & Data Types", "Python Data Model", "beginner", 15, 2),
            ("Control Flow", "Iterators & Generators", "intermediate", 18, 1),
            ("Control Flow", "Context Managers", "intermediate", 15, 2),
            ("Functions", "Understanding Decorators", "intermediate", 15, 1),
            ("Functions", "First-Class Functions", "intermediate", 12, 2),
            ("Decorators", "Class-Based Decorators", "advanced", 20, 1),
            ("Decorators", "Decorator Patterns", "advanced", 25, 2),
            ("List Comprehensions", "List Comprehension Basics", "intermediate", 10, 1),
            ("List Comprehensions", "Dictionary Comprehension", "intermediate", 15, 2),
        ]
        for mod_name, lesson_title, diff, read_time, order in lessons_data:
            Lesson.objects.get_or_create(
                module=modules[mod_name],
                title=lesson_title,
                defaults={
                    "difficulty": diff,
                    "read_time_minutes": read_time,
                    "order": order,
                    "content": f"# {lesson_title}\n\nThis is the lesson content for {lesson_title}.",
                    "code_blocks": [
                        {"filename": "example.py", "code": "# Example code", "language": "python"}
                    ],
                },
            )
        self.stdout.write(f"  Lessons: {Lesson.objects.count()}")

        # ── Interview Questions ──
        questions_data = [
            (pc, "What are Python decorators?", "medium", ["decorators", "functions"]),
            (pc, "Explain Python GIL", "hard", ["threading", "concurrency"]),
            (pc, "What is the difference between a list and a tuple?", "easy", ["data-structures"]),
        ]
        for cat, title, diff, tags in questions_data:
            InterviewQuestion.objects.get_or_create(
                category=cat, title=title,
                defaults={
                    "difficulty": diff,
                    "tags": tags,
                    "description": f"Explain: {title}",
                    "sample_answer": f"Answer for: {title}",
                },
            )
        self.stdout.write(f"  Questions: {InterviewQuestion.objects.count()}")

        # ── Quiz ──
        quiz, _ = Quiz.objects.get_or_create(
            category=pc,
            title="Python Core Fundamentals Quiz",
            defaults={
                "description": "Test your Python fundamentals",
                "time_limit_minutes": 30,
                "passing_score": 70,
            },
        )
        QuizQuestion.objects.get_or_create(
            quiz=quiz, order=0,
            defaults={
                "question_text": "What is a decorator in Python?",
                "options": [
                    "A function that modifies another function",
                    "A class method",
                    "A variable type",
                    "A loop construct",
                ],
                "correct_option_index": 0,
                "explanation": "A decorator is a function that takes a function and returns a modified version of it.",
            },
        )
        self.stdout.write(f"  Quizzes: {Quiz.objects.count()}")

        # ── Challenge: Two Sum ──
        challenge, _ = Challenge.objects.get_or_create(
            slug="two-sum",
            defaults={
                "category": pc,
                "title": "1. Two Sum",
                "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have **exactly one solution**, and you may not use the same element twice.\n\nYou can return the answer in any order.",
                "difficulty": "easy",
                "tags": ["ARRAY", "HASH TABLE"],
                "starter_code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        # Your code here\n        pass",
                "language": "python3",
                "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists.",
                "examples": [
                    {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
                    {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": ""},
                ],
                "points": 100,
                "order": 1,
            },
        )
        TestCase.objects.get_or_create(
            challenge=challenge, order=0,
            defaults={"input_data": "[2,7,11,15]\n9", "expected_output": "[0,1]", "is_hidden": False},
        )
        TestCase.objects.get_or_create(
            challenge=challenge, order=1,
            defaults={"input_data": "[3,2,4]\n6", "expected_output": "[1,2]", "is_hidden": False},
        )
        TestCase.objects.get_or_create(
            challenge=challenge, order=2,
            defaults={"input_data": "[3,3]\n6", "expected_output": "[0,1]", "is_hidden": True},
        )

        # ── More Challenges ──
        more_challenges = [
            ("LRU Cache", "lru-cache", "medium", ["DESIGN", "HASH TABLE"], 350, 2),
            ("Dijkstra's Algorithm", "dijkstras-shortest-path", "hard", ["GRAPH", "SHORTEST PATH"], 500, 3),
        ]
        for title, slug, diff, tags, pts, order in more_challenges:
            ch, _ = Challenge.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": cats["algorithms"],
                    "title": title,
                    "description": f"Implement {title}.",
                    "difficulty": diff,
                    "tags": tags,
                    "starter_code": f"# {title}\npass",
                    "points": pts,
                    "order": order,
                },
            )
            TestCase.objects.get_or_create(
                challenge=ch, order=0,
                defaults={"input_data": "test", "expected_output": "test", "is_hidden": False},
            )
        self.stdout.write(f"  Challenges: {Challenge.objects.count()}")

        # ── User Progress ──
        lessons = Lesson.objects.all()
        for i, lesson in enumerate(lessons):
            if i < 2:
                UserProgress.objects.get_or_create(
                    user=demo, lesson=lesson,
                    defaults={"status": "completed", "percentage": 100},
                )
            elif i == 4:
                UserProgress.objects.get_or_create(
                    user=demo, lesson=lesson,
                    defaults={"status": "in_progress", "percentage": 50},
                )
        self.stdout.write(f"  Progress records: {UserProgress.objects.count()}")

        # ── Activities ──
        Activity.objects.get_or_create(
            user=demo, activity_type="lesson_completed",
            title="Asynchronous Tasks in Python",
            defaults={"description": "Lesson Completed • 45m ago", "metadata": {"tags": ["COROUTINES", "ASYNCIO"]}},
        )
        Activity.objects.get_or_create(
            user=demo, activity_type="challenge_solved",
            title="Dijkstra's Shortest Path",
            defaults={"description": "Algorithm Problem • 2h ago", "metadata": {"difficulty": "HARD"}},
        )
        self.stdout.write(f"  Activities: {Activity.objects.count()}")

        # ── Roadmap ──
        Roadmap.objects.get_or_create(
            user=demo, title="Basics & Syntax",
            defaults={"description": "Completed on Oct 12", "status": "completed", "order": 1},
        )
        Roadmap.objects.get_or_create(
            user=demo, title="Core Fundamentals",
            defaults={"description": "Module 3 of 8 active", "status": "active", "order": 2},
        )
        Roadmap.objects.get_or_create(
            user=demo, title="Advanced Concepts",
            defaults={"description": "Pending prerequisite", "status": "pending", "order": 3},
        )
        self.stdout.write(f"  Roadmap items: {Roadmap.objects.count()}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
