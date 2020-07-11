from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    Product_TYPES = [
        ('E', 'Electric'),  # Wert und lesbare Form
        ('G', 'Games'),
        ('B', 'books'),
        ('O', 'Other'),
    ]

    title = models.CharField(max_length=100)
    Desc = models.CharField(max_length=100,
                            blank=True)

    date_published = models.DateField(blank=True,
                                      default=date.today,
                                      )
    type = models.CharField(max_length=1,
                            choices=Product_TYPES,
                            )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='users',
                             related_query_name='user',
                             )
    Img = models.ImageField(upload_to='products/', blank=True)

    document = models.FileField(upload_to='documents/' ,blank=True)

    class Meta:
        ordering = ['title', '-type']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_full_title(self):
        return_string = self.title
        if self.Desc:  # if subtitle is not empty
            return_string = self.title + ': ' + self.Desc
        return return_string

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='up',
                                      product=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='down',
                                        product=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, user, up_or_down):
        vote = Vote.objects.create(up_or_down=up_or_down,
                                   user=user,
                                   product=self
                                   )

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.get_full_title() + ' / ' + self.type


class Comment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.FloatField(max_length=500, null=True)


    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ' / ' + str(self.timestamp) + ')'

    def get_upvotes(self):
        like = Like.objects.filter(Like_or_not='LIKe',
                                      commnet=self)
        return like

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        dislike = Like.objects.filter(Like_or_not='Dislike',
                                        commnet=self)
        return dislike

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def like(self, user, Like_or_not):
        vote = Like.objects.create(Like_or_not=Like_or_not,
                                   user=user,
                                   commnet=self
                                   )

    def get_report(self):
        report = Report.objects.filter(report='REPORT',
                                        commnet=self)
        return report

    def get_report_count(self):
        return len(self.get_report())

    def report(self, user, report):
        vote = Report.objects.create(report=report,
                                   user=user,
                                   commnet=self
                                   )


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.up_or_down + ' on ' + self.product.title + ' by ' + self.user.username


class Like(models.Model):
    Like_TYPES = [
        ('L', 'LIKe'),
        ('D', 'Dislike'),
    ]

    Like_or_not = models.CharField(max_length=1,
                                  choices=Like_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    commnet = models.ForeignKey(Comment,on_delete=models.CASCADE)

    def __str__(self):
        return self.Like_or_not + ' on ' + self.commnet.text + ' by ' + self.user.username


class Report(models.Model):
    REPORT_TYPES = [
        ('R', 'REPORT'),

    ]

    report = models.CharField(max_length=1,
                                  choices=REPORT_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commnet = models.ForeignKey(Comment,on_delete=models.CASCADE)

    def __str__(self):
        return self.report + ' on ' + self.commnet.text
