from django.db import models
from django.contrib.auth import get_user_model
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

User = get_user_model()

class Book(models.Model):
    owner = models.ForeignKey(User, 
                              on_delete=models.CASCADE,
                              related_name='book',
                              verbose_name='владелец')
    title = models.CharField(max_length=80, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    
    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name_plural = 'Книги'
        verbose_name = 'книгу'