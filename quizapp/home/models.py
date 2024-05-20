from django.db import models
from django.contrib.auth.models import User
import uuid
import random

#creating basemodel class
class BaseModel(models.Model):
    uid= models.UUIDField(primary_key=True,default=uuid.uuid4)
    created_at= models.DateField(auto_now_add= True)
    updated_at= models.DateField(auto_now= True)

    #registering basemodel as base class
    class Meta:
        abstract= True

#creating categories of questions inharriting from basemodel
    
class Category(BaseModel):
    category_name= models.CharField(max_length= 100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    def __str__(self) -> str:
        return self.category_name
    

#creating questions model inharriting from basemodel
    
class Question(BaseModel):
    category= models.ForeignKey(Category ,related_name= 'category', on_delete= models.CASCADE)
    questions= models.CharField(max_length= 500)
    marks= models.IntegerField(default= 5)
    def __str__(self) -> str:
        return self.questions
    
    def get_answer(self):
         answer_objs= list(Answer.objects.filter(question= self))
         random.shuffle(answer_objs)
         data= []
         for answer_obj in answer_objs:
            data.append({
                 "answer": answer_obj.answer,
                 "is_correct": answer_obj.is_correct
             })
         return data
    
class Answer(BaseModel):
    question= models.ForeignKey(Question ,related_name= 'question_answer', on_delete= models.CASCADE)
    answer= models.CharField(max_length= 500)
    is_correct= models.BooleanField(default= False)
    def __str__(self) -> str:
        return self.answer
        

class UserQuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category= models.ForeignKey(Category , on_delete= models.CASCADE)  # storing the category name
    score = models.IntegerField(default=0)
    total_possible_score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def get_percentage(self):
        if self.total_possible_score != 0:
            return (self.score / self.total_possible_score) * 100
        else:
            return 0

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.score}/{self.total_possible_score}"
    
class UserSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.category_name} - {self.score}"

    

