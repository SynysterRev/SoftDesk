from django.urls import reverse_lazy
from rest_framework import status

from projects.models import Project
from users.tests import UserAPITestCase


class ProjectAPITestCase(UserAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.project = Project.objects.create(title="Test Project", description="Test "
                                                                               "description",
                                             author=cls.user, type=1)

    def get_project_no_title(self):
        return {
            'description': 'Test description',
            'author': self.user,
            'type': 2
        }

class TestProject(ProjectAPITestCase):
    url = reverse_lazy('project-list')

    def test_create(self):
        response = self.client.post(self.url, self.get_project_no_title())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
