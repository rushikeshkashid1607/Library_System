from django.db import models

class Book(models.Model):
    # Define the available categories
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Fantasy', 'Fantasy'),
        ('Thriller', 'Thriller'),
        ('Glamour', 'Glamour'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  # Use choices here
    book_id = models.CharField(max_length=50, unique=True)
    pdf = models.FileField(upload_to='books/')

    def __str__(self):
        return self.name
