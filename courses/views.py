from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django .contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from .models import Course

# Create your views here.
class OwnerMixin:
    # Override the get_queryset() method to return only objects created by the current user.
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
    
class OwnerEditMixin:
    # Override the form_valid() method to set the current user as the owner of the object.
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')
    
    
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'
    
   
# The following views are used to manage courses. They are all subclasses of OwnerCourseMixin.
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'
    
    # # Override the get_queryset() method to return only courses created by the current user.
    # # this prevents users from editing courses they didn't create.
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(owner=self.request.user)  
    
    
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
    
 
